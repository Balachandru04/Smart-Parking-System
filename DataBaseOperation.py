
import json
from datetime import datetime
import pymysql
class DBOperation():
    def __init__(self):
        file = open("./config.json", "r")
        datadic = json.loads(file.read())
        file.close()
        self.mydb = pymysql.connect(
            host="localhost",
            user=datadic['username'],
            password=datadic['password'],  # notice: not `passwd`
            database=datadic['database']
        )


    def CreateTables(self):
        cursor = self.mydb.cursor()
        cursor.execute("DROP TABLE IF EXISTS add_vehicle")
        cursor.execute("DROP TABLE IF EXISTS manage_vehicle")
        cursor.execute("DROP TABLE IF EXISTS history")
        cursor.execute("DROP TABLE IF EXISTS slots")
        cursor.execute("DROP TABLE IF EXISTS vehicles")
        cursor.execute("DROP TABLE IF EXISTS admin")

        cursor.execute("""
            CREATE TABLE add_vehicle (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_no VARCHAR(30),
                date DATE,
                entry_time TIME
            )
        """)

        cursor.execute("""
            CREATE TABLE manage_vehicle (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_no VARCHAR(30),
                date DATE,
                entry_time TIME
            )
        """)

        cursor.execute("""
            CREATE TABLE history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_no VARCHAR(30),
                date DATE,
                entry_time TIME,
                exit_time TIME
            )
        """)

        cursor.execute("""
            CREATE TABLE slots (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT,
                is_empty INT,
                space_for VARCHAR(10)
            )
        """)

        cursor.execute("""
            CREATE TABLE vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                mobile VARCHAR(20),
                entry_time DATETIME,
                is_exit TINYINT DEFAULT 0,
                exit_time DATETIME,
                vehicle_no VARCHAR(20),
                vehicle_type VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                password VARCHAR(50)
            )
        """)

        # Add default admin
        cursor.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin123')")
        self.mydb.commit()
        print("✅ Tables created successfully.")

    def getCurrentVehicle(self):
        cursor=self.mydb.cursor()
        cursor.execute("select * from vehicles where is_exit='0'")
        data=cursor.fetchall()
        cursor.close()
        return data
    def getAllVehicle(self):
        cursor=self.mydb.cursor()
        cursor.execute("select * from vehicles where is_exit='1'")
        data=cursor.fetchall()
        cursor.close()
        return data
    

    def AddVehicles(self, name, vehicleno, mobile, vehicle_type):
        spacid = self.spaceAvailable(vehicle_type)
        if spacid:
            current_time = datetime.now()
            data = (
                name,
                mobile,
                current_time,       # entry_time
                None,               # exit_time set as NULL
                0,                  # is_exit (int, not string)
                vehicleno,
                current_time,       # created_at
                current_time,       # updated_at
                vehicle_type
            )
            cursor = self.mydb.cursor()
            cursor.execute("""
                INSERT INTO vehicles 
                (name, mobile, entry_time, exit_time, is_exit, vehicle_no, created_at, updated_at, vehicle_type) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
            self.mydb.commit()

            lastid = cursor.lastrowid
            cursor.execute("""
                UPDATE slots 
                SET vehicle_id = %s, is_empty = 0 
                WHERE id = %s
            """, (lastid, spacid))
            self.mydb.commit()

            cursor.close()
            return True
        else:
            return "No Space Available for Parking"

    def spaceAvailable(self,v_type):
        cursor=self.mydb.cursor()
        cursor.execute("select * from slots where is_empty='1' ")
        data=cursor.fetchall()
        cursor.close()

        if len(data)>0:
            return data[0][0]
        else:
            return False
    def getSlotSpace(self):
        cursor=self.mydb.cursor()
        cursor.execute("select * from slots")
        data=cursor.fetchall()
        cursor.close()
        return data
    def InsertSlotData(self, num_slots=50):
        cursor = self.mydb.cursor()
        # Insert generic parking slots (same for all vehicle types)
        for _ in range(num_slots):
            # cursor.execute("INSERT INTO slots (is_empty) VALUES (1)")  # 1 indicates the slot is empty
            cursor.execute("INSERT INTO slots (vehicle_id, is_empty) VALUES (%s, %s)", (None, 1))
            self.mydb.commit()

        cursor.close()

    def AddVehicle(self, vehicle_no):
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        cursor = self.mydb.cursor()

        # Check if there is an available slot
        space_id = self.getAvailableSlot()  # Get available slot for any vehicle type
        if space_id:
            cursor.execute("""
                INSERT INTO add_vehicle (vehicle_no, date, entry_time)
                VALUES (%s, %s, %s)
            """, (vehicle_no, current_date, current_time))

            self.mydb.commit()

            # Update the slot to be occupied
            cursor.execute("""
                UPDATE slots SET vehicle_id = (SELECT id FROM add_vehicle WHERE vehicle_no = %s ORDER BY id DESC LIMIT 1), is_empty = 0
                WHERE id = %s
            """, (vehicle_no, space_id))

            self.mydb.commit()
            cursor.close()
            return "Vehicle Added Successfully"
        else:
            return "No Available Slot"

    def getAvailableSlot(self):
        cursor = self.mydb.cursor()
        cursor.execute("""
            SELECT id FROM slots WHERE is_empty = 1 LIMIT 1
        """)
        data = cursor.fetchone()
        cursor.close()
        if data:
            return data[0]
        return None

    def ManageVehicle(self, vehicle_no):
        cursor = self.mydb.cursor()
        cursor.execute("""
            SELECT * FROM add_vehicle WHERE vehicle_no = %s ORDER BY id DESC LIMIT 1
        """, (vehicle_no,))
        vehicle_data = cursor.fetchone()

        if vehicle_data:
            current_date = vehicle_data[2]
            current_time = datetime.now().strftime("%H:%M:%S")

            cursor.execute("""
                INSERT INTO manage_vehicle (vehicle_no, date, entry_time)
                VALUES (%s, %s, %s)
            """, (vehicle_no, current_date, current_time))
            self.mydb.commit()
        else:
            print("Vehicle not found in the 'add_vehicle' table.")

        cursor.close()

    def ExitVehicle(self, vehicle_no):
        cursor = self.mydb.cursor()
        cursor.execute("""
            SELECT * FROM manage_vehicle WHERE vehicle_no = %s ORDER BY id DESC LIMIT 1
        """, (vehicle_no,))
        vehicle_data = cursor.fetchone()

        if vehicle_data:
            current_time = datetime.now().strftime("%H:%M:%S")

            # Insert exit record into history
            cursor.execute("""
                INSERT INTO history (vehicle_no, date, entry_time, exit_time)
                VALUES (%s, %s, %s, %s)
            """, (vehicle_no, vehicle_data[2], vehicle_data[3], current_time))
            self.mydb.commit()

            # Remove from manage_vehicle table as the vehicle has exited
            cursor.execute("DELETE FROM manage_vehicle WHERE vehicle_no = %s", (vehicle_no,))
            self.mydb.commit()

            # Remove the vehicle from add_vehicle table as it is no longer a parked entry
            cursor.execute("DELETE FROM add_vehicle WHERE vehicle_no = %s", (vehicle_no,))
            self.mydb.commit()

            # Update the slot to be empty again
            cursor.execute("""
                UPDATE slots SET is_empty = 1, vehicle_id = NULL WHERE vehicle_id = (SELECT id FROM manage_vehicle WHERE vehicle_no = %s ORDER BY id DESC LIMIT 1)
            """, (vehicle_no,))
            self.mydb.commit()

            print(f"Vehicle {vehicle_no} exited and slot has been marked as available.")
        else:
            print("Vehicle not found in the 'manage_vehicle' table.")

        cursor.close()

    def GetManagedVehicles(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM manage_vehicle")
        data = cursor.fetchall()
        cursor.close()

        formatted_data = []
        for row in data:
            entry_time_str = str(row[3]) if row[3] else "N/A"
            formatted_data.append({
                'vehicle_no': row[1],
                'date': row[2].strftime("%d-%m-%Y"),
                'entry_time': entry_time_str
            })

        return formatted_data

    def GetVehicleHistory(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM history")
        data = cursor.fetchall()
        cursor.close()

        formatted_data = []
        for row in data:
            entry_time_str = str(row[3]) if row[3] else "N/A"
            exit_time_str = str(row[4]) if row[4] else "N/A"
            formatted_data.append({
                'vehicle_no': row[1],
                'date': row[2].strftime("%d-%m-%Y"),
                'entry_time': entry_time_str,
                'exit_time': exit_time_str
            })

        return formatted_data

    def doAdminLogin(self, username, password):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    
    def exitVehicle(self,id):
        cursor=self.mydb.cursor()
        currentdata = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # cursor.execute("UPDATE slots set is_empty='1',vehicle_id='' where vehicle_id='"+id+"'")
        cursor.execute("UPDATE slots SET is_empty='1', vehicle_id=NULL WHERE vehicle_id=%s", (id,))
        self.mydb.commit()
        cursor.execute("UPDATE vehicles set is_exit='1',exit_time='"+currentdata+"' where id='" + id + "'")
        self.mydb.commit()


# Example usage
if __name__ == "__main__":
    db = DBOperation()

    # Create tables in the database
    db.CreateTables()

    # Insert 10 generic parking slots
    db.InsertSlotData(50)

    # Add a vehicle
    print(db.AddVehicle("KA-01-H1234"))

    # Manage a vehicle (place it in the management system)
    db.ManageVehicle("KA-01-H1234")

    # Exit a vehicle (record its exit and free up the slot)
    db.ExitVehicle("KA-01-H1234")

    # Get the list of managed vehicles
    print(db.GetManagedVehicles())

    # Get the vehicle history
    print(db.GetVehicleHistory())
