import mysql.connector

def get_connection(): 
    return mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password", 
    database = "myDB" 

)


def get_rooms():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT room_id, room_status
    FROM rooms
    ORDER BY room_id
    """)
    rooms = cursor.fetchall()

    cursor.close()
    db.close()

    return rooms

# id int 
# guest_name varchar(50) 
# qr_code_id varchar(50) 
# room_id int 
# check_in_time datetime 
# check_out_time datetime 
# guest_status enum('Pending','Checked In','Checked Out')

def get_guest():
    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
    SELECT id, guest_name, qr_code_id, room_id, check_in_time, check_out_time, guest_status
    FROM guest_records
    ORDER BY id
""")
    guest_info = cur.fetchall()

    cur.close()
    db.close()

    return guest_info



