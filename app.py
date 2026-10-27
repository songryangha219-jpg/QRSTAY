import streamlit as st
import pandas as pd
from datetime import datetime 
from main import get_rooms
from main import get_guest
from main import get_connection


# Page configuration must come before other Streamlit commands
st.set_page_config(
    page_title="QRStay",
    layout="wide"
)

rooms = get_rooms()
guest = get_guest()
conn = get_connection()

st.title("QRStay")


# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Check-In / Check-Out"

if "guest_found" not in st.session_state:
    st.session_state.guest_found = False

if "qr_data" not in st.session_state:
    st.session_state.qr_data = None

if "action_message" not in st.session_state:
    st.session_state.action_message = None

#Check check in time and check out time

def can_check_in(scheduled_check_in, scheduled_check_out):
    current_time = datetime.now()

    if scheduled_check_in is None:
        return False, "No check-in schedule found."

    # Convert MySQL datetime to Python datetime if necessary
    if isinstance(scheduled_check_in, str):
        scheduled_check_in = datetime.strptime(
            scheduled_check_in,
            "%Y-%m-%d %H:%M:%S"
        )
    if isinstance(scheduled_check_out, str):
            scheduled_check_out = datetime.strptime(
                scheduled_check_out,
                "%Y-%m-%d %H:%M:%S"
            )

    if current_time >= scheduled_check_in and current_time < scheduled_check_out:
        return True
        

    return False



# Navigation buttons
nav1, nav2, nav3 = st.columns(3)

with nav1:
    if st.button("Check-In / Check-Out", use_container_width=True):
        st.session_state.page = "Check-In / Check-Out"

with nav2:
    if st.button("Room Management", use_container_width=True):
        st.session_state.page = "Room Management"

with nav3:
    if st.button("Guest Records", use_container_width=True):
        st.session_state.page = "Guest Records"

st.divider()


# Check in and check out tab

if st.session_state.page == "Check-In / Check-Out":

    st.header("Guest Check-In / Check-Out")

    # Display messages after database updates
    if st.session_state.action_message:
        st.success(st.session_state.action_message)
        st.session_state.action_message = None

    qr_data = st.text_input("Scan or enter guest QR code")

    # Find Guest button
    if st.button("Find Guest"):

        st.session_state.qr_data = str(qr_data).strip()

        df = pd.DataFrame(guest)

        result = df[
            df["qr_code_id"].astype(str).str.strip()
            == st.session_state.qr_data
        ]

        if not result.empty:
            st.session_state.guest_found = True
        else:
            st.session_state.guest_found = False
            st.session_state.qr_data = None
            st.error("Guest not found.")

    # Selected guest
    if (
        st.session_state.guest_found
        and st.session_state.qr_data is not None
    ):

        df = pd.DataFrame(guest)

        result = df[
            df["qr_code_id"].astype(str).str.strip()
            == st.session_state.qr_data
        ]

        if not result.empty:

            guest_name = result.iloc[0]["guest_name"]
            room_id = result.iloc[0]["room_id"]
            status = result.iloc[0]["guest_status"]

            st.write("Guest Name:", guest_name)
            st.write("Room ID:", room_id)
            st.write("Status:", status)

            # Check in btn
            if status != "Checked In":

                if st.button("Check In"):
                    #using this I'm gonna be able to get the time and date
                    check_in_time = result.iloc[0]["check_in_time"]
                    check_out_time = result.iloc[0]["check_out_time"]
                    can = can_check_in(check_in_time, check_out_time)
                    # print(can)

                    if can == True:
                        
                        cursor = conn.cursor()
                        
                        cursor.execute("""
                            UPDATE guest_records
                            SET guest_status = %s,
                            check_in_time = NOW()
                            WHERE qr_code_id = %s
                            """, (
                            "Checked In",
                            st.session_state.qr_data
                            ))
                        
                        cursor.execute("""
                        UPDATE rooms
                        SET room_status = %s
                        WHERE room_id = %s
                        """, (
                            "Occupied",
                            str(room_id)
                        ))
                        
                        conn.commit()
                        cursor.close()
                        
                        st.session_state.action_message = (
                            "Guest checked in successfully!"
                        )
                        
                        st.rerun()
                    elif can == False:
                        st.error("Check in is not allowed")
                    

            else:
                st.info("Guest is already checked in.")




            # check out btn
            if status == "Checked In":

                if st.button("Check Out"):

                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE guest_records
                        SET guest_status = %s,
                            check_out_time = NOW()
                        WHERE qr_code_id = %s
                    """, (
                        "Checked Out",
                        st.session_state.qr_data
                    ))

                    cursor.execute("""
                        UPDATE rooms
                        SET room_status = %s
                        WHERE room_id = %s
                    """, (
                        "Available",
                        str(room_id)
                    ))
                    res = result.iloc[0]["qr_code_id"]
                    cursor.execute("""
                        INSERT INTO history_transactions (id, guest_name, qr_code_id, room_id, check_in_time, check_out_time, guest_status)
                        SELECT id, guest_name, qr_code_id, room_id, check_in_time, check_out_time, guest_status
                        FROM guest_records
                        WHERE qr_code_id = %s
                    """, (res,))

                    cursor.execute("""
                        DELETE FROM guest_records
                        WHERE qr_code_id = %s
                    """, (res,))
                    

                    conn.commit()
                    cursor.close()

                    st.session_state.action_message = (
                        "Guest checked out successfully!"
                    )

                    st.rerun()

        else:
            st.warning(
                "Guest record not found. Please search again."
            )
            st.session_state.guest_found = False


# Room Management tab

elif st.session_state.page == "Room Management":

    st.header("Room Management")

    if rooms:

        df = pd.DataFrame(rooms)

        total_rooms = len(df)
        available = (df["room_status"] == "Available").sum()
        reserved = (df["room_status"] == "Reserved").sum()
        occupied = (df["room_status"] == "Occupied").sum()
        maintenance = (df["room_status"] == "Maintenance").sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rooms", total_rooms)
        col2.metric("Available", int(available))
        col3.metric("Reserved", int(reserved))

        col4, col5 = st.columns(2)

        col4.metric("Occupied", int(occupied))
        col5.metric("Maintenance", int(maintenance))

        st.subheader("Room Records")

        st.dataframe(
            df[["room_id", "room_status"]],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No room records found.")


# Guest records tab

elif st.session_state.page == "Guest Records":

    st.header("Guest Records")
    st.write("Guest information and transaction history")

    if guest:

        df = pd.DataFrame(guest)

        st.subheader("Guest Records")

        st.dataframe(
            df[
                [
                    "id",
                    "guest_name",
                    "qr_code_id",
                    "room_id",
                    "check_in_time",
                    "check_out_time",
                    "guest_status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No guest records found.")