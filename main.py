import json
import random
import string 
from pathlib import Path

print("===================================")
print("    WELCOME TO BANK MANAGEMENT")
print("===================================")

class bank:
    database = 'data.json'
    data =[]
    try: 
        if Path(database).exists():

            with open(database) as file:
                data= json.load(file)
        else:
            print("no such file exists")

    except Exception as err:
        print(f"an error occured {err}")        

    @staticmethod
    def update():
        with open(bank.database, "w") as file:
            file.write(json.dumps(bank.data))

    @classmethod
    def __accountnogenerate(cls):
        alpha = random.choices(string.ascii_letters , k=5)
        num = random.choices(string.digits, k=5)
        id = alpha + num
        random.shuffle(id)
        return "".join(id)



    def createaccount(self):
        info = {"Name": input("Tell your name "),
                "age" :int(input("enter your age ")),
                "email": input("enter your email "),
                "pin": int(input("tell your 4 number pin ")),
                "accountNo" : bank.__accountnogenerate(),
                "balance" : 0
                }
        if info['age']< 18 or len(str(info['pin']))!=4 :
            print("sorry you can not create your account")
        else:
            print("your account has been successfully created")
            for i in info :
                print(f"{i} : {info[i]}")    
            print("please note down your account number")


            bank.data.append(info)
            bank.update()
    
    def depositmoney(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please enter your pin"))

        userdata = [i for i in bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("sorry no data found ")
        else:
            amount = int(input("how much you want to deposit "))
            if amount > 10000 or amount < 0:
                print("sorry you can only deposit between 0 to 10000")
            else :
                userdata[0]['balance'] += amount
                bank.update()
                print("amount deposited successfully")
                       
    def withdrawmoney(self):
            accnumber = input("please tell your account number ")
            pin = int(input("please enter your pin"))
    
            userdata = [i for i in bank.data if i['accountNo'] == accnumber and i['pin'] == pin]
    
            if userdata == False:
                print("sorry no data found ")
            else:
                amount = int(input("how much you want to withdraw "))
                if userdata[0]['balance'] < amount or amount < 0:
                    print("sorry no money big dreams")
                else :
                    userdata[0]['balance'] -= amount
                    bank.update()
                    print("amount withdrawn successfully")

    def details(self):
         accnumber = input("please tell your account number ")
         pin = int(input("please enter your pin"))
         
         userdata = [i for i in bank.data if i['accountNo'] == accnumber and i['pin'] == pin]
             
         if userdata == False:
                print("sorry no data found ")
         else:
              for i in userdata[0]:
                   print(f"{i}:{userdata[0][i]}")

    def checkbalance(self):
         accnumber = input("please tell your account number ")
         pin = int(input("please enter your pin"))
         
         userdata = [i for i in bank.data if i['accountNo'] == accnumber and i['pin'] == pin]
             
         if userdata == False:
                print("sorry no data found ")
         else:
                   print(f"balance :{userdata[0]['balance']}")

    def updatedetails(self):
          accnumber = input("please tell your account number ")
          pin = int(input("please enter your pin"))
                  
          userdata = [i for i in bank.data if i['accountNo'] == accnumber and i['pin'] == pin]
                      
          if userdata == False:
                         print("sorry no data found ")
          else:
               a= int(input("enter 1 to update name , enter 2 to update email , enter 3 to update pin  "))
               if a==1:
                    newname = input("enter the new name ")
                    userdata[0]['Name'] = newname
                    bank.update()
                    print(f"your name has successfully changed into {newname}")

               elif a==2:
                                    newmail = input("enter the new mail ")
                                    userdata[0]['email'] = newmail
                                    bank.update()
                                    print(f"your name has successfully changed into {newmail}")                              

               elif a==3:
                                    newpin =int(input("enter the new pin "))
                                    userdata[0]['pin'] = newpin
                                    bank.update()
                                    print(f"your name has successfully changed into {newpin}")                              
               else:
                     print("invalid input")                                  

if __name__ == "__main__":
    
    user = bank()    

    while True:

        print("1. Create an account")
        print("2. Check balance")
        print("3. Deposit money")
        print("4. Withdraw money")
        print("5. Details")
        print("6. Update Details")
        print("7. Exit")

        action = int(input ("choose any serial no. "))

        if action == 1:
            user.createaccount()
        elif action == 2:
            user.checkbalance()
        elif action == 3:
            user.depositmoney()
        elif action == 4:
            user.withdrawmoney()
        elif action == 5:
            user.details()
        elif action == 6:
            user.updatedetails()
        elif action == 7:
            break
        else:
            print("Invalid choice")
            

 