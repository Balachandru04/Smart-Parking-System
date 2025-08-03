from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QComboBox, QTableWidget, QTableWidgetItem
from DataBaseOperation import DBOperation
from PyQt5.QtWidgets import QHeaderView
import cv2
import numpy as np
from datetime import datetime
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QSizePolicy

class InvoiceGenerator:
    def __init__(self, vehicle_data):
        self.vehicle_data = vehicle_data
        self.output_dir = "./invoices"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_invoice(self):
        name = self.vehicle_data["name"]
        vehicle_no = self.vehicle_data["vehicle_no"]
        vehicle_type = self.vehicle_data["vehicle_type"]
        entry_time = datetime.strptime(self.vehicle_data["entry_time"], "%Y-%m-%d %H:%M:%S")
        exit_time = datetime.strptime(self.vehicle_data["exit_time"], "%Y-%m-%d %H:%M:%S")

        duration = (exit_time - entry_time).total_seconds() / 3600
        charge_per_hour = 10 if vehicle_type == "2" else 20
        total_charge = round(duration * charge_per_hour, 2)

        # Create a blank white image
        width, height = 600, 400
        image = np.ones((height, width, 3), dtype=np.uint8) * 255

        # Set font
        font = cv2.FONT_HERSHEY_SIMPLEX
        title_font_scale = 1
        text_font_scale = 0.6
        title_thickness = 2
        text_thickness = 1

        # Draw the title
        cv2.putText(image, "Vehicle Parking Invoice", (150, 40), font, title_font_scale, (0, 0, 0), title_thickness, cv2.LINE_AA)

        # Prepare the invoice details
        lines = [
            f"Customer Name     : {name}",
            f"Vehicle Number    : {vehicle_no}",
            f"Vehicle Type      : {'Two Wheeler' if vehicle_type == '2' else 'Four Wheeler'}",
            f"Entry Time        : {entry_time}",
            f"Exit Time         : {exit_time}",
            f"Duration (hours)  : {duration:.2f}",
            f"Charge per Hour   : Rs. {charge_per_hour}",
            f"Total Amount      : Rs. {total_charge}"
        ]

        # Draw the invoice details
        y = 80
        for line in lines:
            cv2.putText(image, line, (20, y), font, text_font_scale, (0, 0, 0), text_thickness, cv2.LINE_AA)
            y += 20

        cv2.putText(image, "Thank you for using our parking service.", (20, y + 10), font, text_font_scale, (0, 0, 0), text_thickness, cv2.LINE_AA)

        # Save the image
        invoice_path = os.path.join(self.output_dir, f"invoice_{vehicle_no}_{int(datetime.now().timestamp())}.png")
        cv2.imwrite(invoice_path, image)

        return invoice_path

    def show_invoice(self, image_path):
        # Open and display the image
        img = cv2.imread(image_path)
        cv2.imshow("Invoice", img)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()

class HomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.dbOperation = DBOperation()
        widget = QWidget()
        widget.setStyleSheet("background:#000")
        layout_horizontal = QHBoxLayout()
        menu_vertical_layout = QVBoxLayout()

        self.btn_home = QPushButton("Home")
        self.btn_add = QPushButton("Add Vehicle")
        self.btn_manage = QPushButton("Manage Vehicle")
        self.btn_history = QPushButton("History")

        menu_vertical_layout.setContentsMargins(0, 0, 0, 0)
        menu_vertical_layout.setSpacing(0)
        self.btn_home.setStyleSheet("width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_add.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_manage.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_history.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")

        self.btn_home.clicked.connect(self.showHome)
        self.btn_add.clicked.connect(self.showAdd)
        self.btn_manage.clicked.connect(self.showManage)
        self.btn_history.clicked.connect(self.showHistory)

        menu_frame = QFrame()
        menu_vertical_layout.addWidget(self.btn_home)
        menu_vertical_layout.addWidget(self.btn_add)
        menu_vertical_layout.addWidget(self.btn_manage)
        menu_vertical_layout.addWidget(self.btn_history)
        menu_vertical_layout.addStretch()
        menu_frame.setLayout(menu_vertical_layout)

        parent_vertical = QVBoxLayout()
        parent_vertical.setContentsMargins(0, 0, 0, 0)
        self.vertical_1 = QVBoxLayout()
        self.addHomePageData()

        self.vertical_2 = QVBoxLayout()
        self.vertical_2.setContentsMargins(0, 0, 0, 0)
        self.addAddStudentPage()

        self.vertical_3 = QVBoxLayout()
        self.vertical_3.setContentsMargins(0, 0, 0, 0)
        self.addManagePage()

        self.vertical_4 = QVBoxLayout()
        self.addHistoryPage()

        self.frame_1 = QFrame()
        self.frame_1.setMinimumWidth(self.width())
        self.frame_1.setMaximumWidth(self.width())
        self.frame_1.setMaximumHeight(self.width())
        self.frame_1.setMaximumHeight(self.width())

        self.frame_1.setLayout(self.vertical_1)
        self.frame_2 = QFrame()
        self.frame_2.setLayout(self.vertical_2)
        self.frame_3 = QFrame()
        self.frame_3.setLayout(self.vertical_3)
        self.frame_4 = QFrame()
        self.frame_4.setLayout(self.vertical_4)

        parent_vertical.addWidget(self.frame_1)
        parent_vertical.addWidget(self.frame_2)
        parent_vertical.addWidget(self.frame_3)
        parent_vertical.addWidget(self.frame_4)

        layout_horizontal.addWidget(menu_frame)
        layout_horizontal.addLayout(parent_vertical)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        parent_vertical.setContentsMargins(0, 0, 0, 0)
        parent_vertical.addStretch()
        layout_horizontal.addStretch()
        widget.setLayout(layout_horizontal)

        self.frame_1.show()
        self.frame_2.hide()
        self.frame_3.hide()
        self.frame_4.hide()

        self.setCentralWidget(widget)

    def generateInvoice(self):
        # Gather vehicle data for the invoice
        vehicle_data = {
            "name": "John Doe",  # Replace with actual data
            "vehicle_no": "TN09AB1234",  # Replace with actual data
            "vehicle_type": "4",  # Replace with actual data
            "entry_time": "2025-04-20 10:00:00",  # Replace with actual data
            "exit_time": "2025-04-20 13:30:00"  # Replace with actual data
        }

        # Create an instance of InvoiceGenerator
        generator = InvoiceGenerator(vehicle_data)
        image_path = generator.generate_invoice()
        # print(f"Invoice saved at: {image_path}")
        generator.show_invoice(image_path)  # Show the generated invoice

    def showHistory(self):
        self.btn_home.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_add.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_manage.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_history.setStyleSheet("width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white")

        self.frame_1.hide()
        self.frame_2.hide()
        self.frame_3.hide()
        self.frame_4.show()

    def showManage(self):
        self.btn_home.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_add.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_manage.setStyleSheet("width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_history.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")

        self.frame_1.hide()
        self.frame_2.hide()
        self.frame_4.hide()
        self.frame_3.show()

    def showAdd(self):
        self.btn_home.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_add.setStyleSheet("width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_manage.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_history.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")

        self.frame_1.hide()
        self.frame_3.hide()
        self.frame_4.hide()
        self.frame_2.show()

    def showHome(self):
        self.btn_home.setStyleSheet("width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_add.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_manage.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")
        self.btn_history.setStyleSheet("width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white")

        self.frame_2.hide()
        self.frame_3.hide()
        self.frame_4.hide()
        self.frame_1.show()

    def refreshHome(self):
        while self.gridLayout.count():
            child = self.gridLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        row = 0
        i = 0
        alldata = self.dbOperation.getSlotSpace()
        for data in alldata:
            label = QPushButton("Slot " + str(data[0]) + " \n " + str(data[1]))

            if data[2] == 1:
                label.setStyleSheet("background-color:green;color:white;padding:5px;width:100px;height:100px;border:1px solid white;text-align:center;font-weight:bold")
            else:
                label.setStyleSheet("background-color:red;color:white;padding:5px;width:100px;height:100px;border:1px solid white;text-align:center;font-weight:bold")

            if i % 5 == 0:
                i = 0
                row = row + 1

            self.gridLayout.addWidget(label, row, i)
            i = i + 1


    def addHomePageData(self):
        self.vertical_1.setContentsMargins(0, 0, 0, 0)

        # Create and style the Refresh button
        button = QPushButton("Refresh")
        button.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px;background:purple;border:1px solid white")
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.clicked.connect(self.refreshHome)

        # Main vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Add Refresh button to layout (this is the correct place)
        vertical_layout.addWidget(button)

        # Create a frame to hold the layout
        frame = QFrame()

        # Grid layout for slot buttons
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(0)
        vertical_layout.addLayout(self.gridLayout)

        # Fetch slot data from database
        alldata = self.dbOperation.getSlotSpace()
        # print("alldata:", alldata)

        row = 0
        i = 0
        for data in alldata:
            # print("data tuple:", data)
            label = QPushButton("Slot " + str(data[0]) + " \n " + str(data[1]))

            # data[2] = is_empty; 1 means green (available), 0 = red (filled)
            if data[2] == 1:
                label.setStyleSheet("background-color:green;color:white;padding:5px;width:100px;height:100px;border:1px solid white;text-align:center;font-weight:bold")
            else:
                label.setStyleSheet("background-color:red;color:white;padding:5px;width:100px;height:100px;border:1px solid white;text-align:center;font-weight:bold")

            if i % 5 == 0:
                i = 0
                row += 1

            self.gridLayout.addWidget(label, row, i)
            i += 1

        frame.setLayout(vertical_layout)
        self.vertical_1.addWidget(frame)
        self.vertical_1.addStretch()

    def addAddStudentPage(self):
        layout = QVBoxLayout()
        frame = QFrame()

        name_label = QLabel("Name : ")
        name_label.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px")
        mobile_label = QLabel("Mobile : ")
        mobile_label.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px")
        vechicle_label = QLabel("Vehicle No : ")
        vechicle_label.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px")
        vechicle_type = QLabel("Vehicle Type : ")
        vechicle_type.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px")
        error_label = QLabel("")
        error_label.setStyleSheet("color:red;padding:8px 0px;font-size:20px")

        name_input = QLineEdit()
        name_input.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px")
        mobile_input = QLineEdit()
        mobile_input.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px")
        vehicle_input = QLineEdit()
        vehicle_input.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px")
        vtype = QComboBox()
        vtype.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px;border:1px solid white")
        vtype.addItem("2 Wheeler")
        vtype.addItem("4 Wheeler")

        button = QPushButton("Add Vehicle")
        button.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px;background:green;border:1px solid white")

        button.clicked.connect(lambda: self.addVehicles(
            name_input.text(), vehicle_input.text(), mobile_input.text(), vtype.currentIndex(),
            error_label, name_input, vehicle_input, mobile_input, vtype
        ))

        layout.addWidget(name_label)
        layout.addWidget(name_input)
        layout.addWidget(mobile_label)
        layout.addWidget(mobile_input)
        layout.addWidget(vechicle_label)
        layout.addWidget(vehicle_input)
        layout.addWidget(vechicle_type)
        layout.addWidget(vtype)
        layout.addWidget(button)
        layout.addWidget(error_label)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        frame.setMinimumHeight(self.height())
        frame.setMinimumWidth(self.width())
        frame.setMaximumHeight(self.width())
        frame.setMaximumWidth(self.width())

        frame.setLayout(layout)
        self.vertical_2.addWidget(frame)

    def addVehicles(self, name, vehicleno, mobile, index, error_label,
                    name_input, vehicle_input, mobile_input, vtype):
        vehicle_type = "2" if index == 0 else "4"

        data = self.dbOperation.AddVehicles(name, vehicleno, mobile, vehicle_type)

        if data is True:
            error_label.setText("Added Successfully")
            name_input.clear()
            vehicle_input.clear()
            mobile_input.clear()
            vtype.setCurrentIndex(0)  # Reset to "2 Wheeler"

        elif data is False:
            error_label.setText("Failed to Add Vehicle")
        else:
            error_label.setText(str(data))

    def addManagePage(self):
        data = self.dbOperation.getCurrentVehicle()  # Fetch current vehicle data from the database
        self.table = QTableWidget()
        self.table.setStyleSheet("background:#fff")
        self.table.resize(self.width(), self.height())
        self.table.setRowCount(len(data))
        self.table.setColumnCount(7)

        # Set up the table headers
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Vehicle No"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Mobile"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Vehicle Type"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Entry Time"))
        self.table.setHorizontalHeaderItem(6, QTableWidgetItem("Action"))

        # Populate the table with vehicle data
        for loop, smalldata in enumerate(data):
            self.table.setItem(loop, 0, QTableWidgetItem(str(smalldata[0])))  # ID
            self.table.setItem(loop, 1, QTableWidgetItem(str(smalldata[1])))  # Name
            self.table.setItem(loop, 2, QTableWidgetItem(str(smalldata[6])))  # Vehicle No
            self.table.setItem(loop, 3, QTableWidgetItem(str(smalldata[2])))  # Mobile
            self.table.setItem(loop, 4, QTableWidgetItem(str(smalldata[7])))  # Vehicle Type
            self.table.setItem(loop, 5, QTableWidgetItem(str(smalldata[3])))  # Entry Time

            # Create an "Exit" button for each vehicle
            self.button_exit = QPushButton("Exit")
            self.button_exit.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px;background:green;border:1px solid white")
            self.table.setCellWidget(loop, 6, self.button_exit)  # Add button to the table
            self.button_exit.clicked.connect(self.exitCall)  # Connect button to exitCall method

        # Create a frame to hold the table and refresh button
        frame = QFrame()
        layout = QVBoxLayout()
        button = QPushButton("Refresh")
        button.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px;background:green;border:1px solid white")
        button.clicked.connect(self.refreshManage)  # Connect refresh button to refreshManage method


        # Set layout for the frame
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(button)  # Add refresh button to layout
        layout.addWidget(self.table)  # Add table to layout
        frame.setLayout(layout)  # Set layout to the frame
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setMaximumWidth(self.width())
        frame.setMinimumWidth(self.width())
        frame.setMaximumHeight(self.height())
        frame.setMinimumHeight(self.height())
        
        # Add the frame to the vertical layout for the manage page
        self.vertical_3.addWidget(frame)
        self.vertical_3.addStretch()  # Add stretchable space at the end

    def refreshManage(self):
        data = self.dbOperation.getCurrentVehicle()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(7)
        loop = 0
        for smalldata in data:
            self.table.setItem(loop, 0, QTableWidgetItem(str(smalldata[0])))
            self.table.setItem(loop, 1, QTableWidgetItem(str(smalldata[1])))
            self.table.setItem(loop, 2, QTableWidgetItem(str(smalldata[6])))
            self.table.setItem(loop, 3, QTableWidgetItem(str(smalldata[2])))
            self.table.setItem(loop, 4, QTableWidgetItem(str(smalldata[7])))
            self.table.setItem(loop, 5, QTableWidgetItem(str(smalldata[3])))
            self.button_exit = QPushButton("Exit")
            self.table.setCellWidget(loop, 6, self.button_exit)
            self.button_exit.clicked.connect(self.exitCall)
            loop += 1

    def refreshHistory(self):
        self.table1.clearContents()
        data = self.dbOperation.getAllVehicle()
        loop = 0
        self.table1.setRowCount(len(data))
        self.table1.setColumnCount(7)
        for smalldata in data:
            self.table1.setItem(loop, 0, QTableWidgetItem(str(smalldata[0])))
            self.table1.setItem(loop, 1, QTableWidgetItem(str(smalldata[1])))
            self.table1.setItem(loop, 2, QTableWidgetItem(str(smalldata[6])))
            self.table1.setItem(loop, 3, QTableWidgetItem(str(smalldata[2])))
            self.table1.setItem(loop, 4, QTableWidgetItem(str(smalldata[7])))
            self.table1.setItem(loop, 5, QTableWidgetItem(str(smalldata[3])))
            self.table1.setItem(loop, 6, QTableWidgetItem(str(smalldata[5])))
            loop += 1

    def addHistoryPage(self):
        data = self.dbOperation.getAllVehicle()
        self.table1 = QTableWidget()
        self.table1.resize(self.width(), self.height())
        self.table1.setRowCount(len(data))
        self.table1.setStyleSheet("background:#fff")
        self.table1.setColumnCount(7)

        button = QPushButton("Refresh")
        button.setStyleSheet("color:#fff;padding:8px 0px;font-size:20px;background:green;border:1px solid white")
        button.clicked.connect(self.refreshHistory)

        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table1.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.table1.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.table1.setHorizontalHeaderItem(2, QTableWidgetItem("VEHICLE No"))
        self.table1.setHorizontalHeaderItem(3, QTableWidgetItem("MOBILE"))
        self.table1.setHorizontalHeaderItem(4, QTableWidgetItem("VEHICLE TYPE"))
        self.table1.setHorizontalHeaderItem(5, QTableWidgetItem("ENTRY TIME"))
        self.table1.setHorizontalHeaderItem(6, QTableWidgetItem("EXIT TIME"))

        loop = 0
        # for smalldata in data:
        #     self.table1.setItem(loop, 0, QTableWidgetItem(str(smalldata[0])))
        #     self.table1.setItem(loop, 1, QTableWidgetItem(str(smalldata[1])))
        #     self.table1.setItem(loop, 2, QTableWidgetItem(str(smalldata[6])))
        #     self.table1.setItem(loop, 3, QTableWidgetItem(str(smalldata[2])))
        #     self.table1.setItem(loop, 4, QTableWidgetItem(str(smalldata[7])))
        #     self.table1.setItem(loop, 5, QTableWidgetItem(str(smalldata[3])))
        #     self.table1.setItem(loop, 6, QTableWidgetItem(str(smalldata[5])))
        #     loop += 1

        for smalldata in data:
            self.table1.setItem(loop, 0, QTableWidgetItem(str(smalldata[0])))  # ID
            self.table1.setItem(loop, 1, QTableWidgetItem(str(smalldata[1])))  # Name
            self.table1.setItem(loop, 2, QTableWidgetItem(str(smalldata[6])))  # Vehicle No
            self.table1.setItem(loop, 3, QTableWidgetItem(str(smalldata[2])))  # Mobile
            self.table1.setItem(loop, 4, QTableWidgetItem(str(smalldata[7])))  # Vehicle Type
            self.table1.setItem(loop, 5, QTableWidgetItem(str(smalldata[3])))  # Entry Time

            # Show Exit Time
            exit_time = smalldata[5] if smalldata[5] else "--"
            self.table1.setItem(loop, 6, QTableWidgetItem(str(exit_time)))

            loop += 1

        self.frame5 = QFrame()
        self.layout1 = QVBoxLayout()
        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.layout1.setSpacing(0)
        self.layout1.addWidget(button)
        self.layout1.addWidget(self.table1)
        self.frame5.setLayout(self.layout1)
        self.frame5.setContentsMargins(0, 0, 0, 0)
        self.frame5.setMaximumWidth(self.width())
        self.frame5.setMinimumWidth(self.width())
        self.frame5.setMaximumHeight(self.height())
        self.frame5.setMinimumHeight(self.height())
        self.vertical_4.addWidget(self.frame5)
        self.vertical_4.addStretch()

    def exitCall(self):
        button = self.sender()
        if button:
            row = self.table.indexAt(button.pos()).row()
            if row >= 0:
                vehicle_id = str(self.table.item(row, 0).text())
                name = self.table.item(row, 1).text()
                vehicle_no = self.table.item(row, 2).text()
                vehicle_type = self.table.item(row, 4).text()
                entry_time_str = self.table.item(row, 5).text()

                try:
                    entry_time = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
                except ValueError as e:
                    print(f"Error parsing entry time: {e}")
                    return

                exit_time = datetime.now()
                duration = (exit_time - entry_time).total_seconds() / 3600
                charge_per_hour = 20
                total_charge = duration * charge_per_hour

                labels = [
                    "Customer Name",
                    "Vehicle Number",
                    "Vehicle Type",
                    "Entry Time",
                    "Exit Time",
                    "Duration (hours)",
                    "Charge per Hour",
                    "Total Amount"
                ]
                values = [
                    name,
                    vehicle_no,
                    "Two Wheeler" if vehicle_type == "2" else "Four Wheeler",
                    entry_time.strftime('%Y-%m-%d %H:%M:%S'),
                    exit_time.strftime('%Y-%m-%d %H:%M:%S'),
                    f"{duration:.2f}",
                    f"Rs. {charge_per_hour}",
                    f"Rs. {total_charge:.2f}"
                ]

                # Create dialog
                invoice_window = QDialog(self)
                invoice_window.setWindowTitle("Invoice")
                layout = QGridLayout()

                for i in range(len(labels)):
                    label_widget = QLabel(f"{labels[i]}:")
                    value_widget = QLabel(values[i])
                    label_widget.setStyleSheet("font-weight: bold; font-size: 14px;")
                    value_widget.setStyleSheet("font-size: 14px;")
                    layout.addWidget(label_widget, i, 0)
                    layout.addWidget(value_widget, i, 1)

                save_button = QPushButton("Save Invoice as JPG")
                save_button.setStyleSheet("font-size: 16px; padding: 8px; background-color: green; color: white;")
                layout.addWidget(save_button, len(labels), 0, 1, 2)

                invoice_window.setLayout(layout)

                # Safe file path
                invoice_folder = r"D:\Self_Learning\project\Data Analysics Projects\parking management system\invoices"
                os.makedirs(invoice_folder, exist_ok=True)
                safe_name = name.replace(" ", "_")
                safe_vehicle_no = vehicle_no.replace(" ", "").replace("-", "").upper()
                invoice_file_path = os.path.join(invoice_folder, f"invoice_{safe_name}_{safe_vehicle_no}.jpg")

                def save_and_close():
                    self.save_invoice_as_jpg(
                        [f"{labels[i]} : {values[i]}" for i in range(len(labels))],
                        invoice_file_path
                    )
                    invoice_window.accept()  # Close the dialog

                save_button.clicked.connect(save_and_close)
                invoice_window.exec_()

                # Final DB cleanup
                self.dbOperation.exitVehicle(vehicle_id)
                self.table.removeRow(row)

    def save_invoice_as_jpg(self, invoice_details, file_path):
        from PIL import Image, ImageDraw, ImageFont

        # Use a better TTF font and set larger font size
        try:
            font = ImageFont.truetype("arial.ttf", 20)  # Use system font
        except:
            font = ImageFont.load_default()  # Fallback

        # Prepare label and value lists
        labels, values = [], []
        for line in invoice_details:
            parts = line.split(":", 1)
            if len(parts) == 2:
                labels.append(parts[0].strip())
                values.append(parts[1].strip())
            else:
                labels.append(line.strip())
                values.append("")

        dummy_img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(dummy_img)

        line_height = 30
        padding = 40
        max_label_width = max([draw.textbbox((0, 0), label, font=font)[2] for label in labels]) + 20
        max_value_width = max([draw.textbbox((0, 0), val, font=font)[2] for val in values])
        width = max_label_width + max_value_width + padding * 2
        height = line_height * len(labels) + padding * 2

        # Create high-resolution image (increase size by scaling factor if needed)
        img = Image.new('RGB', (width, height), color='white')
        d = ImageDraw.Draw(img)

        y = padding
        for label, value in zip(labels, values):
            d.text((padding, y), f"{label}:", fill=(0, 0, 0), font=font)
            d.text((padding + max_label_width, y), value, fill=(0, 0, 0), font=font)
            y += line_height

        # Save with high DPI (300 is print-quality)
        img.save(file_path, dpi=(300, 300))
