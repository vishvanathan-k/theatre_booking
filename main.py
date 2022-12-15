#importing modules and libraries
import sys
import file
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import file
import random
import _var

def clear(widget):
    for i in range(widget.count()):
        widget.removeWidget(widget.currentWidget())

def back(widget):
    clear(widget)
    welcome = WelcomeScreen()
    widget.addWidget(welcome)
    widget.setCurrentIndex(widget.currentIndex()+1)


class PushButton(QPushButton):
    #Custom class for pushbutton
    def __init__(self, text, parent=None):
        super(PushButton, self).__init__(text, parent)

        self.setText(text)
        self.setMinimumSize(QSize(50, 50))
        self.setMaximumSize(QSize(50, 50))



class WelcomeScreen(QDialog):
    #class containing the welcome screen
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui",self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)

    #Navigate to login screen
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #Navigate to create account screen
    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class LoginScreen(QDialog):
    #class containing the login screen
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        self.login.clicked.connect(self.loginfunction)

    #Login function
    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        user_type = self.Usertype.currentText()

        if len(user)==0 or len(password)==0:
            self.error.setText("Please input all fields.")

        else:
            if user_type=="Admin":
                if user=="admin" and password=="admin":
                    self.error.setText("Login Successful.")
                    admin = Admin_Page()
                    widget.addWidget(admin)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                else:
                    self.error.setText("Invalid username or password.")
            else:
                usern = file.read_user()
                for i in usern:
                    if user == i[0] and password == i[1]:
                        _var.User_Logined = user
                        frontpage = Front_Page()
                        widget.addWidget(frontpage)
                        widget.setCurrentIndex(widget.currentIndex()+1)
                else:
                    self.error.setText("Incorrect username or password.")
                    pass



class CreateAccScreen(QDialog):
    #class containing the create account screen
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui",self)
        self.signup.clicked.connect(self.signupfunction)

    #Signup function
    def signupfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()
       
        if len(user)==0 or len(password)==0 or len(confirmpassword)==0:
            self.error.setText("Please fill in all inputs.")

        elif password!=confirmpassword:
            self.error.setText("Passwords do not match.")
        else:
            file.write_user(user,password)
            _var.User_Logined = user
            frontpage = Front_Page()
            widget.addWidget(frontpage)
            widget.setCurrentIndex(widget.currentIndex()+1)



class Front_Page(QDialog):
    #class containing the front page
    def __init__(self):
        super(Front_Page, self).__init__()
        loadUi("frontpage.ui",self)
        self.book.clicked.connect(self._func1_)
        self.view.clicked.connect(self._func2_)
        self.label.setText("Welcome!! "+_var.User_Logined+".")

    #Navigate to seat selection page
    def _func1_(self):
        clear(widget)
        username = Listing_UI()
        widget.addWidget(username)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def _func2_(self):
        clear(widget)
        booking = Booking_History()
        widget.addWidget(booking)
        widget.setCurrentIndex(widget.currentIndex()+1)



class Admin_Page(QDialog):
    #class containing the admin page
    def __init__(self):
        super(Admin_Page, self).__init__()
        loadUi("admin.ui",self)
        self.Add.clicked.connect(self.add)
        self.Remove.clicked.connect(self.remove)
        self.signout.clicked.connect(self.signoutfunc)
        self.AdminTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.AdminTable.setHorizontalHeaderLabels(["Movie Language","Movie Screen", "Movie Name","Movie Time","Movie Price(Rs.)","No of Seats booked","Movie Collection(Rs.)"])
        self.AdminTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view()

    def signoutfunc(self):
        back(widget)
    
    #Navigate to add movie page- screen, time, movie, price
    #Navigate to add movie page- screen, time, movie, price
    def add(self):
        self.dialog = QDialog()
        layout = QFormLayout()
        self.lang = QComboBox()
        self.lang.addItems(["English","Hindi","Tamil"])
        self.lang.currentIndexChanged.connect(self.langchange)
        self.movie = QComboBox()
        self.Screen = QComboBox()
        self.Screen.addItems(["resony","khatija","grahan","juve","aura"])
        self.timing = QComboBox()
        self.timing.addItems(["10:00 AM","1:00 PM","05:00 PM","09:00 PM"])
        self.price = QSpinBox()
        self.price.setRange(99,999)
        self.price.setSingleStep(10)
        self.price.setValue(99)
        self.Ok = QPushButton("Ok")
        self.Ok.clicked.connect(self.getAddDetails)
        layout.addRow("language",self.lang)
        layout.addRow("movie",self.movie)
        layout.addRow("screen",self.Screen)
        layout.addRow("timing",self.timing)
        layout.addRow("price",self.price)
        layout.addRow(self.Ok)
        self.langchange()
        self.dialog.setLayout(layout)
        self.dialog.exec_()
        self.dialog.show()
        
    
    def langchange(self):
        lang = self.lang.currentText()
        if lang.lower() == "tamil":
            self.movie.clear()
            self.movie.addItems(["ponniyin selvan 2","Jailer","Varisu"])
        elif lang.lower()=='hindi':
            self.movie.clear()
            self.movie.addItems(["Adipurush"])
        elif lang.lower()=='english':
            self.movie.clear()
            self.movie.addItems(["Oppenheimer"])

    def getAddDetails(self):
        lang = self.lang.currentText()
        screen= self.Screen.currentText()
        movie=self.movie.currentText()
        timing=self.timing.currentText()
        price = self.price.value()
        d = file.read_cinema()
        for i in d:
            if i[0]==lang and i[1]==screen and i[2]==movie and i[3]==timing:
                err = QMessageBox()
                err.setIcon(QMessageBox.Critical)
                err.setText("Show already exists.")
                err.setWindowTitle("Error")
                err.setEscapeButton(QMessageBox.Close)
                err.exec_()
                self.dialog.close()
                return    
        file.write_cinema(lang,screen,movie,timing,price)
        self.dialog.close()
        self.view()
    
    def remove(self):
        mov = []
        for i in file.read_cinema():
            mov.append(i[2] +"-"+ i[1])
        option, pressed = QInputDialog.getItem(self, "Cancel Movie", "Select the Movie:" , mov, 0, False)
        if pressed:
            y = []
            for i in file.read_cinema():
                x = option.split("-")
                if i[2] == x[0] and i[1] == x[-1]:
                    y = i
            file.delete_cinema(y[1],y[2],y[3])
            self.view()
        pass

    def view(self):
        self.AdminTable.setRowCount(0)
        for row_number, row_data in enumerate(file.read_cinema()):
            self.AdminTable.insertRow(row_number)
            self.seats = file.read_seats(row_data[1],row_data[2],row_data[3])
            for column_number, data in enumerate(row_data):
                self.AdminTable.setItem(row_number, column_number, QTableWidgetItem(str(data).capitalize()))
            self.AdminTable.setItem(row_number, 5, QTableWidgetItem(str(len(self.seats))))
            self.AdminTable.setItem(row_number, 6, QTableWidgetItem(str(len(self.seats)*int(row_data[4]))))
        self.AdminTable.resizeColumnsToContents()




class Booking_History(QDialog):
    #class containing the booking history page
    def __init__(self):
        super(Booking_History, self).__init__()
        loadUi("booking_history.ui",self)
        self.HistoryTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HistoryTable.setHorizontalHeaderLabels(["Bill No","Movie Screen", "Movie Name","Movie Time","Seats booked"])
        self.Cancel.clicked.connect(self.cancel)
        self.view()

    def view(self):
        self.HistoryTable.clearContents()
        self.HistoryTable.setRowCount(0)
        for row_number, row_data in enumerate(file.read_booking(_var.User_Logined)):
            self.HistoryTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 4:
                    self.HistoryTable.setItem(row_number, column_number, QTableWidgetItem(str(data).upper()))
                else:
                    self.HistoryTable.setItem(row_number, column_number, QTableWidgetItem(str(data).capitalize()))
        self.HistoryTable.resizeColumnsToContents()
    
    def cancel(self):
        option, pressed = QInputDialog.getItem(self, "Cancel Ticket", "Select the ticket:" , [str(i) for i in file.bill_no()], 0, False)
        if pressed:
            file.cancel_ticket(option)
            self.view()    




class Listing_UI(QDialog):
    def __init__(self):
        super(Listing_UI, self).__init__()
        loadUi("listing.ui",self)
        self.listing_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.listing_table.setRowCount(0)
        self.listing_table.setColumnCount(5)
        self.listing_table.setHorizontalHeaderLabels(["Language","Movie Screen","Movie Name", "Movie Time","Price(in Rs)"])
        self.listing_table.resizeColumnsToContents()
        self.listing_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.proceed.clicked.connect(self.proceed_func)
        self.view()
    
    def view(self):
        self.listing_table.clearContents()
        self.listing_table.setRowCount(0)
        for row_number, row_data in enumerate(file.read_cinema()):
            self.listing_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 3:
                    self.listing_table.setItem(row_number, column_number, QTableWidgetItem(str(data).upper()))
                else:
                    self.listing_table.setItem(row_number, column_number, QTableWidgetItem(str(data).capitalize()))
        self.listing_table.resizeColumnsToContents()
    
    def proceed_func(self):
        try:
            row = self.listing_table.currentRow()
            _var.Cinema = self.listing_table.item(row,2).text()
            _var.Screen = self.listing_table.item(row,1).text()
            _var.Timing = self.listing_table.item(row,3).text()
        except AttributeError:
            return None
        seat=Seat_Page()
        widget.addWidget(seat)
        widget.setCurrentIndex(widget.currentIndex()+1)




class Seat_Page(QDialog):
    #class containing the seat selection screen
    def __init__(self):
        super(QDialog, self).__init__()
        loadUi("seats.ui", self)

        self.seats_list = []
        self.seats = file.read_seats(_var.Screen,_var.Cinema,_var.Timing)
        self.rows = 10
        self.columns = 10
        self.label_2.setText("Cinema: "+_var.Cinema+" Screen: "+_var.Screen+" Timing: "+_var.Timing)
        
        _list = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9","A10",
                 "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9","B10",
                 "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9","C10",
                 "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9","D10",
                 "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9","E10",
                 "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9","F10",
                 "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9","G10",
                 "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9","H10",
                 "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9","I10",
                 "K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9","K10",
                 "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9","L10"]
        len_list = len(_list)

        i = 0
        for row in range(self.rows): 
           for column in range(self.columns): 
                button = PushButton(f'{_list[i]}', self)
                button.clicked.connect(partial(self.onClicked,button, _list[i]))
                if _list[i] in self.seats:
                    button.setStyleSheet("background-color: red")
                elif _list[i] in self.seats_list:
                    button.setStyleSheet("background-color: orange")
                else:
                    button.setStyleSheet("background-color: green")
                self.gridLayout.addWidget(button, row+1, column)
                i += 1
                if i == len_list: break
        self.Book.clicked.connect(self.book)

    def onClicked(self, button, i):
        if i in self.seats:
            return -1
        elif i not in self.seats_list:
            self.seats_list.append(i)
            self.label.setText("Selected:"+','.join(self.seats_list))
            button.setStyleSheet("background-color: orange")
        elif i in self.seats_list:
            self.seats_list.remove(i)
            self.label.setText("Selected:"+','.join(self.seats_list))
            button.setStyleSheet("background-color: green")

    def book(self):
        if len(self.seats_list) == 0:
            self.label.setText("Select atleast one seat")
            return None
        _var.Seats_Booked = self.seats_list
        self.seats_list = []
        self.seats = []
        payment = Payment_Page()
        widget.addWidget(payment)
        widget.setCurrentIndex(widget.currentIndex()+1)




class Payment_Page(QDialog):
    #class containing the payment page
    def __init__(self):
        super(Payment_Page, self).__init__()
        loadUi("payment.ui",self)
        _var.Price = file.get_price(_var.Screen,_var.Cinema,_var.Timing)
        self.seats = file.read_seats(_var.Screen,_var.Cinema,_var.Timing)
        self.label_2.setText("Seats booked:"+' '.join(_var.Seats_Booked))
        self.pay.clicked.connect(self.payfunction)
        self.checkBox_21.stateChanged.connect(self.food_amount)
        self.checkBox_22.stateChanged.connect(self.food_amount)
        self.checkBox_23.stateChanged.connect(self.food_amount)
        self.checkBox_24.stateChanged.connect(self.food_amount)
        self.checkBox_25.stateChanged.connect(self.food_amount)
        self.checkBox_26.stateChanged.connect(self.food_amount)
        self.checkBox_27.stateChanged.connect(self.food_amount)
        self.checkBox_28.stateChanged.connect(self.food_amount)
        self.checkBox_29.stateChanged.connect(self.food_amount)
        self.checkBox_30.stateChanged.connect(self.food_amount)
        self.label_3.setText("Total amount:"+str(int(_var.Price)*len(_var.Seats_Booked)))

    def payfunction(self):
        data = file.bill_no()
        bill = random.randint(100000,999999)
        while bill in data:
            bill = random.randint(100000,999999)
        
        if self.seats == []:
            self.seats += _var.Seats_Booked
            file.write_seats(_var.Screen,_var.Cinema,_var.Timing,self.seats)

        else:
            self.seats += _var.Seats_Booked

            file.modify_seats(_var.Screen,_var.Cinema,_var.Timing,self.seats)


        r = QMessageBox.question(self, 'Payment', f"Payment Successful\n Bill No:{bill}", QMessageBox.Ok)
        if r == QMessageBox.Ok:
            file.write_booking(bill,_var.User_Logined,_var.Screen,_var.Cinema,_var.Timing,_var.Seats_Booked)
            self.close()
            home = Front_Page()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        
    def food_amount(self):
        amt = 0

        if self.checkBox_21.isChecked():
            amt += 100
        if self.checkBox_22.isChecked():
            amt += 50
        if self.checkBox_23.isChecked():
            amt += 35
        if self.checkBox_24.isChecked():
            amt += 35
        if self.checkBox_25.isChecked():
            amt += 40
        if self.checkBox_26.isChecked():
            amt += 50
        if self.checkBox_27.isChecked():
            amt += 50
        if self.checkBox_28.isChecked():
            amt += 30
        if self.checkBox_29.isChecked():
            amt += 50
        if self.checkBox_30.isChecked():
            amt += 70

        self.label_3.setText("Total amount:"+str(int(_var.Price)*len(_var.Seats_Booked) + amt))



if __name__ == "__main__":
    # main
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QStackedWidget()
    app.setWindowIcon(QIcon('logo.jpg'))
    widget = QStackedWidget()
    app.setWindowIcon(QIcon('logo.jpg'))
    app.setStyle("Fusion")
    app.setApplicationDisplayName("Haran's Javiha")
    app.setStyleSheet("""
                QWidget#bgwidget{
                    background-image: url("bg1.jpg");
                    background-image: url("bg1.jpg");
                    }

                QLineEdit{
                    background-color:rgb(255,255,255);
                    border-radius:20px;
                    font: 14pt "MS Shell Dlg 2";
                }
                QComboBox{
                    font: 14pt "MS Shell Dlg 2";
                }

                .QPushButton{
                	border-style: none;
                    background-color:rgb(255,255,255);
                    border-radius:20px;
                    font: 14pt "MS Shell Dlg 2";
                    width: 150px;
                    height: 40px;
                	border: 0px;
                	color: #F0F0F0;
                	padding: 5px;	
                	min-height: 20px;
                	background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #4D4D4D, stop:1 #292929); 
                }

                .QPushButton:hover{ 
                	background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #636363, stop:1 #575757);
                }

                .QPushButton:pressed{ 
                	background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #4D4D4D, stop:1 #292929);
                }
                QLabel{
                    font: 14pt "MS Shell Dlg 2";
                    }
                QLabel#pic_label{
                    image: url("logo.png");
                }

    """)
    widget.addWidget(welcome)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    sys.exit(app.exec_())