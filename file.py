#writing a binary file
import os
import pickle
from encrypt import hash

#To read and write users as [username,password (hashed)] along with options to change password and check if user exists
#user.dat starts
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
        user = [name, hash(password)]
        pickle.dump(user, f)

def check_user(name):
    user = read_user()
    for i in user:
        if i[0] == name:
            return True
    return False

def change_password(name, password):
    with open('user.dat', 'rb') as f, open('temp.dat', 'wb') as f1:
        try:
            while True:
                user = pickle.load(f)
                if user[0] == name:
                    user[1] = password
                pickle.dump(user, f1)
        except EOFError:
            pass
    os.remove('user.dat')
    os.rename('temp.dat', 'user.dat')
#ends

#show.dat starts
#To read and write the shows
def write_show(language,screen,cinema,timings,price):
    d = read_show()
    with open('show.dat',"ab") as f:
        x = [language,screen,cinema,timings,price]
        g = False
        for i in d:
            if x == i:
                g = True
                break
        if not g:
            pickle.dump(x,f)
    
def get_price(screen,cinema,timings):
    with open('show.dat',"rb") as f:
        try:
            while True:
                data = pickle.load(f)
                if data[1].lower()==screen.lower() and data[2].lower()==cinema.lower() and data[3]==timings:
                    return data[4]
        except EOFError:
            return 299

def read_show():
    try:
        with open('show.dat',"rb") as f:
            cinema = []
            try:
                while True:
                    cinema.append(pickle.load(f))
            except EOFError:
                pass
            return cinema
    except FileNotFoundError:
        return []

def delete_show(screen,cinema,timings):
    with open('show.dat','rb') as f, open('temp.dat','wb') as f1:
        try:
            while True:
                data = pickle.load(f)
                if data[1].lower()!=screen.lower() or data[2].lower()!=cinema.lower() or data[3]!=timings:
                    pickle.dump(data,f1)
        except EOFError:
            pass
    os.remove('show.dat')
    os.rename('temp.dat','show.dat')
#ends

#seats.dat starts     
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
#ends

#booking.dat starts
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
                if data[0].lower()==dat[2].lower() and data[1].lower()==dat[3].lower() and data[2].lower()==dat[4].lower():
                    for i in dat[-1]:
                        data[3].remove(i)
                pickle.dump(data,f1)
        except EOFError:
            pass
    os.remove('seats.dat')
    os.rename('temp.dat','seats.dat')
#ends

#secques.dat starts
#Write and read security questions along with answers for each user
def write_secques(user_name,qno,ans):
    with open('secques.dat',"ab") as f:
        pickle.dump([user_name,qno,ans],f)

def read_secques(user_name):
    try:
        with open('secques.dat',"rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    if data[0].lower()==user_name.lower():
                        return data[1],data[2]
            except EOFError:
                return None,None
    except FileNotFoundError:
        return None,None
#ends

#movies.dat starts

def write_movie(language,movie_name):
    with open('movies.dat',"ab") as f:
        pickle.dump([language,movie_name],f)
    
def read_movie():
    try:
        with open('movies.dat',"rb") as f:
            movie = []
            try:
                while True:
                    movie.append(pickle.load(f))
            except EOFError:
                pass
            return movie
    except FileNotFoundError:
        return []

def remove_movie(language,movie_name):
    with open('movies.dat','rb') as f, open('temp.dat','wb') as f1:
        try:
            while True:
                data = pickle.load(f)
                if data[0].lower()!=language.lower() or data[1].lower()!=movie_name.lower():
                    pickle.dump(data,f1)
        except EOFError:
            pass
    os.remove('movies.dat')
    os.rename('temp.dat','movies.dat')
#ends