#writing a binary file
import os
import pickle

screen = ["resony","khatija","grahan","juve","aura"]
cinemas = ["ponniyin selvan 2","Jailer","Varisu","Oppenheimer","Adipurush"]
timing = ["10:00 AM","1:00 PM","05:00 PM","09:00 PM"]

#user should be stored [name,password]
def read_user():
    try:
        with open('user.dat', 'rb') as f:
            user = []
            try:
                while True:
                    user.append(pickle.load(f))
            except EOFError:
                pass
            return user
    except FileNotFoundError:
        return []

def write_user(name, password):
    with open('user.dat', 'ab') as f:
        user = [name, password]
        pickle.dump(user, f)

#To read and write the cinemas
def write_cinema(language,screen,cinema,timings,price):
    d = read_cinema()
    with open('cinema.dat',"ab") as f:
        x = [language,screen,cinema,timings,price]
        g = False
        for i in d:
            if x == i:
                g = True
                break
        if not g:
            pickle.dump(x,f)
    
def get_price(screen,cinema,timings):
    with open('cinema.dat',"rb") as f:
        try:
            while True:
                data = pickle.load(f)
                if data[1].lower()==screen.lower() and data[2].lower()==cinema.lower() and data[3]==timings:
                    return data[4]
        except EOFError:
            return 299

def read_cinema():
    try:
        with open('cinema.dat',"rb") as f:
            cinema = []
            try:
                while True:
                    cinema.append(pickle.load(f))
            except EOFError:
                pass
            return cinema
    except FileNotFoundError:
        return []

def delete_cinema(screen,cinema,timings):
    with open('cinema.dat','rb') as f, open('temp.dat','wb') as f1:
        try:
            while True:
                data = pickle.load(f)
                if data[1].lower()!=screen.lower() or data[2].lower()!=cinema.lower() or data[3]!=timings:
                    pickle.dump(data,f1)
        except EOFError:
            pass
    os.remove('cinema.dat')
    os.rename('temp.dat','cinema.dat')

#To read, write and modify the seats
def write_seats(screen,cinema,timings,booked_seats):
    with open('seats.dat',"ab") as f:
        pickle.dump([screen,cinema,timings,booked_seats],f)
    
def read_seats(screen,cinema,timings):
    try:
        with open('seats.dat',"rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    if data[0].lower()==screen.lower() and data[1].lower()==cinema.lower() and data[2].lower()==timings.lower():
                        return data[3]
            except EOFError:
                return []
    except FileNotFoundError:
        return []

def modify_seats(screen,cinema,timings,booked_seats):
    with open('seats.dat','rb') as f, open('temp.dat','wb') as f1:
        try:
            while True:
                data = pickle.load(f)
                if data[0].lower()==screen.lower() and data[1].lower()==cinema.lower() and data[2]==timings:
                    data[3] = booked_seats
                    pickle.dump(data,f1)
                else:
                    pickle.dump(data,f1)
        except EOFError:
            pass
    os.remove('seats.dat')
    os.rename('temp.dat','seats.dat')


def write_booking(bill_no,user_name,screen,cinema,timings,booked_seats):
    with open('booking.dat',"ab") as f:
        pickle.dump([bill_no,user_name,screen,cinema,timings,booked_seats],f)

def read_booking(user_name):
    dat = []
    try:
        with open('booking.dat',"rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    if data[1].lower()==user_name:
                        dat.append([data[0],data[2],data[3],data[4]," ".join(data[5])])
            except EOFError:
                return dat
    except FileNotFoundError:
        return dat

def bill_no():
    bill = []
    try:
        with open('booking.dat',"rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    bill += [data[0]]
            except EOFError:
                return bill
    except FileNotFoundError:
        return bill

def cancel_ticket(bill_no):
    dat = []
    with open('booking.dat','rb') as f, open('temp.dat','wb') as f1:
        try:
            while True:
                data = pickle.load(f)
                if data[0]!=int(bill_no):
                    pickle.dump(data,f1)
                else:
                    dat = data
        except EOFError:
            pass
    os.remove('booking.dat')
    os.rename('temp.dat','booking.dat')
    #delete seats in seats.dat
    with open('seats.dat','rb') as f, open('temp.dat','wb') as f1:
        try:
            while True:
                data = pickle.load(f)
                if data[0].lower()==dat[2].lower() and data[1].lower()==dat[3].lower() and data[2]==dat[4]:
                    for i in dat[-1]:
                        data[3].remove(i)
                pickle.dump(data,f1)
        except EOFError:
            pass