import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QLineEdit, QMessageBox, QWidget, QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime
from PyQt5.QtWidgets import QInputDialog

# Room Data with Prices
rooms = {
    "101": {"type": "Single", "price_per_night": 5800, "available": True},
    "102": {"type": "Double", "price_per_night": 8700, "available": True},
    "103": {"type": "Suite", "price_per_night": 17400, "available": True},
    "104": {"type": "Single", "price_per_night": 6380, "available": True},
    "105": {"type": "Double", "price_per_night": 9280, "available": True},
    "106": {"type": "Suite", "price_per_night": 17980, "available": True},
    "107": {"type": "Single", "price_per_night": 6960, "available": True},
    "108": {"type": "Double", "price_per_night": 9860, "available": True},
    "109": {"type": "Suite", "price_per_night": 18580, "available": True},
}

# Customer data (mocked for loyalty points and reservations)
customers = {}

class HotelReservationSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel Reservation System")
        self.setGeometry(200, 200, 700, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # Header
        header_label = QLabel("HOTEL DE LUNA", self)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #444; padding-bottom: 20px;")
        layout.addWidget(header_label)

        # Room Availability Button
        availability_button = QPushButton("Check Room Availability", self)
        availability_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 15px;")
        availability_button.clicked.connect(self.check_availability)
        layout.addWidget(availability_button)

        # Booking Section
        booking_label = QLabel("Book a Room", self)
        booking_label.setStyleSheet("font-size: 20px; margin-top: 20px;")
        layout.addWidget(booking_label)

        # Name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name[Last Name, First Name]")
        self.name_input.setStyleSheet("font-size: 16px; height: 40px; padding: 10px;")
        layout.addWidget(self.name_input)

        # Room Selection Dropdown
        self.room_combo = QComboBox(self)
        self.room_combo.setStyleSheet("font-size: 16px; height: 40px; padding: 10px;")
        self.room_combo.addItem("Select a room")
        for room_number, room_info in rooms.items():
            self.room_combo.addItem(f"Room {room_number} - {room_info['type']} (₱{room_info['price_per_night']}/night)",
                                    room_number)
        layout.addWidget(self.room_combo)

        # Check-in Date
        self.check_in_date = QDateEdit(self)
        self.check_in_date.setCalendarPopup(True)
        self.check_in_date.setDate(QDate.currentDate())
        self.check_in_date.setDisplayFormat("yyyy-MM-dd")
        self.check_in_date.setStyleSheet("font-size: 16px; height: 40px; padding: 10px;")
        self.check_in_date.dateChanged.connect(self.update_check_out_date)
        layout.addWidget(QLabel("Check-in Date"))
        layout.addWidget(self.check_in_date)

        # Check-out Date
        self.check_out_date = QDateEdit(self)
        self.check_out_date.setCalendarPopup(True)
        self.check_out_date.setDate(QDate.currentDate().addDays(1))
        self.check_out_date.setDisplayFormat("yyyy-MM-dd")
        self.check_out_date.setStyleSheet("font-size: 16px; height: 40px; padding: 10px;")
        layout.addWidget(QLabel("Check-out Date"))
        layout.addWidget(self.check_out_date)

        # Book Room Button
        book_button = QPushButton("Book Room", self)
        book_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 15px;")
        book_button.clicked.connect(self.book_room)
        layout.addWidget(book_button)

        # View Bookings Button
        view_bookings_button = QPushButton("View Bookings", self)
        view_bookings_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 18px; padding: 15px;")
        view_bookings_button.clicked.connect(self.view_bookings)
        layout.addWidget(view_bookings_button)

        # View Loyalty Points Button
        view_points_button = QPushButton("View Loyalty Points", self)
        view_points_button.setStyleSheet("background-color: #FFC107; color: white; font-size: 18px; padding: 15px;")
        view_points_button.clicked.connect(self.view_loyalty_points)
        layout.addWidget(view_points_button)

        # Modify Booking Button
        modify_button = QPushButton("Modify Reservation", self)
        modify_button.setStyleSheet("background-color: #FF9800; color: white; font-size: 18px; padding: 15px;")
        modify_button.clicked.connect(self.modify_reservation)
        layout.addWidget(modify_button)

        # Cancel Booking Button
        cancel_button = QPushButton("Cancel Booking", self)
        cancel_button.setStyleSheet("background-color: #F44336; color: white; font-size: 18px; padding: 15px;")
        cancel_button.clicked.connect(self.cancel_booking)
        layout.addWidget(cancel_button)

        # Set the main layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_check_out_date(self):
        check_in_date = self.check_in_date.date()
        check_out_date = check_in_date.addDays(1)
        self.check_out_date.setDate(check_out_date)

    def check_availability(self):
        available_rooms = "\n".join(
            [f"Room {room}: {info['type']} - ₱{info['price_per_night']}/night" for room, info in rooms.items() if
             info['available']]
        )
        QMessageBox.information(self, "Available Rooms", available_rooms)

    def book_room(self):
        name = self.name_input.text().strip()
        room_selection = self.room_combo.currentData()

        # Validation
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter your name.")
            return
        if room_selection is None:
            QMessageBox.warning(self, "Input Error", "Please select a room.")
            return

        room_info = rooms[room_selection]
        check_in = self.check_in_date.date().toString("yyyy-MM-dd")
        check_out = self.check_out_date.date().toString("yyyy-MM-dd")

        # Calculate total nights and cost
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        total_nights = (check_out_date - check_in_date).days
        if total_nights <= 0:
            QMessageBox.warning(self, "Input Error", "Check-out date must be after check-in date.")
            return
        total_cost = total_nights * room_info['price_per_night']

        # Process booking
        self.process_payment(name, room_selection, total_cost, total_nights, check_in, check_out)

    def process_payment(self, name, room_number, total_cost, total_nights, check_in, check_out):
        payment_dialog = QMessageBox(self)
        payment_dialog.setWindowTitle("Payment Processing")
        payment_dialog.setText(f"Amount Due: ₱{total_cost}")
        payment_dialog.setDetailedText(f"Total Nights: {total_nights}\nTotal Cost: ₱{total_cost}")
        payment_dialog.addButton("Pay", QMessageBox.AcceptRole)
        payment_dialog.addButton(QMessageBox.Cancel)

        result = payment_dialog.exec_()

        if result == QMessageBox.AcceptRole:
            cash_amount, ok = QInputDialog.getDouble(self, "Cash Payment", "Enter cash amount:", min=0)

            if ok:
                if cash_amount < total_cost:
                    QMessageBox.warning(self, "Insufficient Cash",
                                        "The cash provided is not enough to cover the total cost.")
                    return
                change = cash_amount - total_cost  # Calculate change
                QMessageBox.information(self, "Payment Successful",
                                        f"Payment of ₱{total_cost} has been processed successfully!\nChange: ₱{change:.2f}")
                rooms[room_number]["available"] = False

                # Add to customer record
                if name not in customers:
                    customers[name] = {"room_number": room_number, "check_in": check_in, "check_out": check_out,
                                       "total_cost": total_cost, "loyalty_points": 0}
                else:
                    customers[name]["room_number"] = room_number
                    customers[name]["check_in"] = check_in
                    customers[name]["check_out"] = check_out
                    customers[name]["total_cost"] = total_cost

                # Add loyalty points (30 points per booking)
                loyalty_points_earned = 30
                customers[name]["loyalty_points"] += loyalty_points_earned

                QMessageBox.information(self, "Booking Confirmation",
                                        f"Guest: {name}\nRoom Number: {room_number}\nLoyalty Points Earned: {loyalty_points_earned}")

    def view_bookings(self):
        if not customers:
            QMessageBox.information(self, "Bookings", "No bookings available.")
            return

        sorted_bookings = sorted(customers.items(), key=lambda item: item[0])

        booking_details = "\n".join([f"Guest: {name}, Room: {data['room_number']}, Check-in: {data['check_in']}, "
                                     f"Check-out: {data['check_out']}, Total Cost: ₱{data['total_cost']} "
                                     f"Points: {data['loyalty_points']}"
                                     for name, data in sorted_bookings])

        booking_dialog = QMessageBox(self)
        booking_dialog.setWindowTitle("All Bookings")
        booking_dialog.setText(booking_details)
        booking_dialog.exec_()

    def view_loyalty_points(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter your name.")
            return

        if name not in customers:
            QMessageBox.information(self, "Loyalty Points", f"No loyalty points found for {name}.")
            return

        points = customers[name]["loyalty_points"]
        QMessageBox.information(self, "Loyalty Points", f"{name} has {points} loyalty points.")

    def modify_reservation(self):
        name = self.name_input.text().strip()
        if name not in customers:
            QMessageBox.warning(self, "Modification Error", f"No reservation found for {name}.")
            return

        room_selection = self.room_combo.currentData()
        if room_selection is None:
            QMessageBox.warning(self, "Input Error", "Please select a room.")
            return

        new_room_info = rooms[room_selection]
        check_in = self.check_in_date.date().toString("yyyy-MM-dd")
        check_out = self.check_out_date.date().toString("yyyy-MM-dd")

        # Calculate total nights and cost
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        total_nights = (check_out_date - check_in_date).days
        if total_nights <= 0:
            QMessageBox.warning(self, "Input Error", "Check-out date must be after check-in date.")
            return
        total_cost = total_nights * new_room_info['price_per_night']

        # Process payment for modification
        self.process_payment(name, room_selection, total_cost, total_nights, check_in, check_out)

    def cancel_booking(self):
        name = self.name_input.text().strip()
        if name not in customers:
            QMessageBox.warning(self, "Cancellation Error", f"No reservation found for {name}.")
            return

        del customers[name]
        QMessageBox.information(self, "Cancellation Successful", f"Reservation for {name} has been canceled.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HotelReservationSystem()
    window.show()
    sys.exit(app.exec_())
