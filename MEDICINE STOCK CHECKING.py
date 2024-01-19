import os
import random
import datetime
import mysql.connector
mycon=mysql.connector.connect(host='localhost',user='root',
                              password='root',database='medicine')
mycur=mycon.cursor()
q = "Create table stock(batch_no int primary key,name text,manuf text,date_man text,date_exp text,quantity int,sell int,balance int,cost_unit int)"
q2 = "Create table dispose(batch_no int primary key,name text,date_exp text,amount int)"
q3 = "Create table user(id int primary key AUTO_INCREMENT,name text,email text,password text)"

try:
    mycur.execute(q3)
    mycur.execute(q2)
    mycur.execute(q)
except:
    pass
def Store():
    sql="Insert into stock(batch_no,name,manuf,date_man,date_exp,quantity,sell,balance,cost_unit)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print('\nPLEASE PROVIDE THE REQUIRED INFORMATION\n')
    acc=int(input('\nENTER THE BATCH NUMBER:'))
    nm=input('\nENTER THE NAME OF THE MEDICINE WITH POWER:')
    addr=input('\nENTER THE NAME OF THE MANUFACTURER:')
    dbs=input('\nENTER THE DATE OF MANUFACTURE(YYYY-MM-DD):')
    dacc=input('\nENTER THE DATE OF EXPIRY(YYYY-MM-DD):')
    quan=int(input('\nENTER THE QUANTITY OF THE IMPORTED MEDICINE:'))
    sell=0
    balance=quan
    cost=int(input('\nENTER THE COST OF THE IMPORTED MEDICINE PER UNIT:'))
    value=(acc,nm,addr,dbs,dacc,quan,sell,balance,cost)
    try:
        mycur.execute(sql,value)
        print(nm,'ADDED TO THE STOCK')
        mycon.commit()
    except:
        print('UNABLE TO ADD MEDICINE!!!!!')



def Search_by_Name():
    ph=input('\nENTER THE MEDICINE NAME TO SEARCH:')
    sql="Select * from Stock where name=%s"
    value=(ph,)
    mycur.execute(sql,value)
    rec=mycur.fetchone()
    if(rec==None):
        print(ph,'IS NOT AVAILABLE')
    else:
        print('BATCH NUMBER:\t',rec[0])
        print('MEDICINE NAME:\t',rec[1])
        print('MANUFACTURER:\t',rec[2])
        print('DATE OF MANUFACTURE:\t',rec[3])
        print('DATE OF EXPIRY:\t',rec[4])
        print('QUANITTY STORED:\t',rec[5])
        print('INITIAL COST:\t',rec[8])
        


def Search_by_Manu():
    ph=input('\nENTER THE MANUFACTURER NAME TO SEARCH:')
    sql="Select name from Stock where manuf=%s"
    value=(ph,)
    mycur.execute(sql,value)
    rec=mycur.fetchall()
    if(rec==None):
        print(ph,'IS A WRONG MANUFACTURER')
    else:
        print('----------MEDICINES MANUFACTURED BY',ph,'--------------------')
        for nm in rec:
            print(nm[0])
    


def Cost_Update():
    sql="Update stock set cost_unit=%s where name=%s";
    ph=input('\nENTER THE MEDICINE NAME TO CHANGE COST:')
    addr=int(input('\nENTER THE NEW COST PER UNIT:'))
    value=(addr,ph)
    try:
        mycur.execute(sql,value)
        mycon.commit()
        print('NEW COST OF',ph,'IS=RS',addr)
    except:
        print('UNABLE TO CHANGE COST!!!!')



def Sell():
    sql="Update stock set sell=%s,balance=%s where name=%s";
    ph=input('\nENTER THE MEDICINE NAME TO SELL:')
    addr=int(input('\nENTER THE QUANTITY TO SELL:'))
    sql2='select quantity,cost_unit from stock where name=%s'
    value2=(ph,)
    mycur.execute(sql2,value2)
    rec=mycur.fetchone()
    if(addr>rec[0]):
        print('INSUFFICIENT STOCK IN HAND!!!!!!')
        return
    else:
        balance=rec[0]-addr
        value=(addr,balance,ph)
        try:
            mycur.execute(sql,value)
            mycon.commit()
            print(addr,'UNITS OF',ph,'SOLD')
            print(balance,'UNITS LEFT')
            c = input("Generate the bill (Y/N) :")
            if c.lower()=='y':
                print("+------------------------------------------+")
                print("|Name: ",ph)
                print("|Quantity: ",addr)
                print("|Price each: ",rec[1])
                print("|Total Price : ",addr*rec[1])
                print("+------------------------------------------+")
                
        except:
            print('UNABLE TO SELL MEDICINE!!!!')


def Available():
    ph=input('\nENTER THE MEDICINE NAME TO SEARCH:')
    sql="Select balance from Stock where name=%s"
    value=(ph,)
    mycur.execute(sql,value)
    rec=mycur.fetchone()
    if(rec==None):
        print(ph,'IS NOT AVAILABLE')
    else:
        print(rec[0],'UNITS OF',ph,'IS AVAILABLE')
         


def Dispose():
    sql="Insert into dispose(batch_no,name,date_exp,amount)values(%s,%s,%s,%s)"
    nm=input('\nENTER THE MEDICINE NAME TO DISPOSE:')
    sql2="Select batch_no,name,date_exp,balance from stock where name=%s and date_exp<=%s"
    t_date=datetime.date.today()
    value2=(nm,t_date)
    mycur.execute(sql2,value2)
    rec=mycur.fetchone()
    if(rec==None):
        print(nm,'IS NOT EXPIRED YET')
    else:
        print(nm,'IS EXPIRED')
        c=int(input('\nPRESS 1 TO DISPOSE IT:'))
        if(c==1):
            b=rec[0]
            n=rec[1]
            d=rec[2]
            am=rec[3]
            value=(b,n,d,am)
            sql3='Delete from stock where name=%s'
            value3=(n,)
            try:
                mycur.execute(sql,value)
                mycon.commit()
                print(n,'SUCCESSFULLY DISPOSED')
                mycur.execute(sql3,value3)
                mycon.commit()
            except:
                print('UNABLE TO DISPOSE MEDICINE')
        else:
            print('WARNING!!!!!',nm,'MUST BE DISPOSED LATER')
            return

def Search_Dispose():
    ph=input('\nENTER THE DISPOSED MEDICINE NAME TO SEARCH:')
    sql="Select * from Dispose where name=%s"
    value=(ph,)
    mycur.execute(sql,value)
    rec=mycur.fetchone()
    mycon.commit()
    if(rec==None):
        print(ph,'IS NOT AVAILABLE')
    else:
        print('BATCH NUMBER:\t',rec[0])
        print('MEDICINE NAME:\t',rec[1])
        print('DATE OF EXPIRY:\t',rec[2])
        print('BALANCE AMOUNT:\t',rec[3])
        





def Close():
    
    print('\nTHANK YOU FOR USING THE APPLICATION')
    quit()


def login():
    e = input('\nENTER THE YOUR EMAIL:')
    p = input('\nENTER THE YOUR PASSWORD:')
    q = f"select * from user where email = '{e}' and password = '{p}'"
    mycur.execute(q)
    if mycur.fetchone()!=None:
        print("\n Logged In Successfully !!!")
        home()
    else:
        print("\n Login Failed")
def register():
    n = input('\nENTER THE YOUR NAME:')
    e = input('\nENTER THE YOUR EMAIL:')
    p = input('\nENTER THE YOUR PASSWORD:')
    q = f"insert into user (name,email,password) values('{n}','{e}','{p}')"
    mycur.execute(q)
    mycon.commit()
    print("\nRegistered Successfully !!!")
def home():
    while(True):
        print('\n\nPRESS 1 TO ADD A NEW MEDICINE')
        print('PRESS 2 TO SEARCH A MEDICINE BY NAME')
        print('PRESS 3 TO SEARCH A MEDICINE BY MANUFACTURER')
        print('PRESS 4 TO UPDATE MEDICINE COST')
        print('PRESS 5 TO SELL MEDICINE')
        print('PRESS 6 TO CHECK AVAILABILITY')
        print('PRESS 7 TO DISPOSE EXPIRED MEDICINE')
        print('PRESS 8 TO SEARCH EXPIRED MEDICINE BY NAME')
        print('PRESS 9 TO LOGOUT')
        choice=int(input('ENTER YOUR CHOICE : '))
        if(choice==1):
            Store()
        elif(choice==2):
            Search_by_Name()
        elif(choice==3):
            Search_by_Manu()
        elif(choice==4):
            Cost_Update()
        elif(choice==5):
            Sell()
        elif(choice==6):
            Available()
        elif(choice==7):
            Dispose()
        elif(choice==8):
            Search_Dispose()
        else:
            break
while True:
    print('------------WELCOME TO MEDICINE STOCK CHECKING SYSTEM-------------\n\n')
    print("\nPRESS 1 TO LOGIN") 
    print("PRESS 2 TO REGISTER") 
    print('PRESS 3 TO CLOSE THE APPLICATION')
    choice=int(input('ENTER YOUR CHOICE : '))
    if(choice==1):
        login()
    elif(choice==2):
        register()
    elif(choice==3):
        Close()
    else:
        pass
        
           
    
















