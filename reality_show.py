import mysql.connector
from datetime import datetime
mydb = mysql.connector.connect(host="localhost", user="root", password="roshna#2001",database="reality_show");
mycursor = mydb.cursor()
class userDetails:
    def __init__(self,username,userpassword):
        self.name=username
        self.password=userpassword
    def isAlreadyuser(self):
        mycursor.execute('select user_id,user_name,password from user_details where user_name like %s',(self.name,))
        details=mycursor.fetchall()
        if(details):
            if(details[0][1]==self.name and details[0][2]==self.password):
                return details[0][0]
        else:
            return 0
class show:
    def displayShow(self):
        mycursor.execute('select show_name,start_date,start_time,end_time,duration,trp,channel_name from shows')
        display=mycursor.fetchall()
        for i in range(len(display)):
            row=display[i]
            print('Show name:',row[0],'Start date:',row[1],'Start time:',row[2],'End time:',row[3],'Show duration:',row[4],'TRP Rate:',row[5],'Channel:',row[6])

class contestant:
    def __init__(self,user_id):
        self.user_id=user_id
    def displayContestant(self):
        print("Enter options which show contestants you want to see \n1.Bigg boss\n2.Dance jodi dance\n3.Cook with comali\n4.Comedy kings\n5.Super singer")
        opt=int(input())
        mycursor.execute(" select contestants.contestant_id, contestants.contestant_name,shows.show_name,contestants.marks,contestants.votes from contestants inner join shows on contestants.show_id=shows.show_id where shows.show_id=%s",(opt,))
        display=mycursor.fetchall()
        show=display[0][2]
        for i in range(len(display)):
            row=display[i]
            print("Contestant id:",row[0],"name:",row[1],"show name:",row[2],"marks:",row[3],"votes:",row[4])
        print("Do you want to vote any of these contestants(y/n):")
        c=str(input())
        if c=='y':
            mycursor.execute("select vote_close_time,voting_status from shows where show_id=%s",(opt,))
            check=mycursor.fetchall()
            f = '%Y-%m-%d %H:%M:%S'
            b=str(check[0][0])
            x = datetime.now()
            a = datetime.strptime(b, f)
            y = datetime.strptime(str(x)[:19], f)
            if (a>y):
                id = int(input("Enter contestant id:"))
                now = datetime.now()
                formattedDate = now.strftime('%Y-%m-%d %H:%M:%S')
                mycursor.execute(
                    "select contestants.votes,contestants.contestant_name from contestants inner join shows on contestants.show_id=shows.show_id where contestants.contestant_id=%s",
                    (id,))
                d = mycursor.fetchall()
                v = d[0][0]
                v = v + 1
                name=d[0][1]
                mycursor.execute("update contestants set votes=%s where contestant_id=%s", (v, id,))
                mydb.commit()
                mycursor.execute("insert into previous_vote(user_id,name,show_name,date) values(%s,%s,%s,%s)",
                                 (self.user_id, name, show, formattedDate,))
                mydb.commit()
                print("Thanks for voting!")
                print("\n")

            else:

                status=check[0][1]
                close='closed'
                if(status=="open"):
                    mycursor.execute("update shows set voting_status=%s where show_id=%s",(close,opt,))
                    mydb.commit()
                    mycursor.execute(("select min(votes),contestant_id,contestant_name from contestants where show_id=%s"),(opt,))
                    elim=mycursor.fetchall()
                    id=elim[0][1]
                    name=elim[0][2]
                    mycursor.execute("insert into eliminates(name,votes,eliminated_date,show_id) values(%s,%s,%s,%s)",(name,0,y,opt,))
                    mydb.commit()
                    mycursor.execute("delete from contestants where contestant_id=%s",(id,))
                    mydb.commit()
                print("Sorry voting time is closed!")
                print("\n")
class eliminates:
    def __init__(self,id):
        self.user_id=id
    def displayEliminates(self):
        print("Enter options which show eliminates you want to see \n1.Bigg boss\n2.Dance jodi dance\n3.Cook with comali\n4.Comedy kings\n5.Super singer")
        opt = int(input())
        mycursor.execute("select eliminates.e_id, eliminates.name, eliminates.votes, shows.show_name from eliminates inner join shows on eliminates.show_id = shows.show_id where shows.show_id=%s",(opt,))
        details=mycursor.fetchall()
        show=details[0][3]
        for i in range(len(details)):
            row=details[i]
            print('si:',i+1,' ','eliminates id',row[0],' ','Name:',row[1],' ','Votes:',row[2],' ','Show name:',row[3])

        print("Do you want to vote any contestants(y/n)")
        c=str(input())
        if(c=='y'):
            id = int(input("Enter contestant id:"))
            now = datetime.now()
            formattedDate = now.strftime('%Y-%m-%d %H:%M:%S')
            mycursor.execute(
                "select eliminates.votes,eliminates.name, from eliminates inner join shows on eliminates.show_id=shows.show_id where eliminates.e_id=%s",
                (id,))
            d = mycursor.fetchall()
            v = d[0][0]
            v = v + 1
            name=d[0][1]
            mycursor.execute("update eliminates set votes=%s where e_id=%s", (v, id,))
            mydb.commit()
            mycursor.execute("insert into previous_vote(user_id,name,show_name,date) values(%s,%s,%s,%s)",
                             (self.user_id, name, show, formattedDate,))
            mydb.commit()
            print("Thanks for voting!")
class previousVote:
    def __init__(self,id):
        self.user_id=id
    def displayVotes(self):
        mycursor.execute("select name,show_name from previous_vote where user_id=%s",(self.user_id,))
        details=mycursor.fetchall()
        for i in range(len(details)):
            row=details[i]
            print(i+1,' ','name:',row[0],' ','show name:',row[1])
        print("\n")
class wildcard:
    def displayWildcard(self):
        print("Enter options which show eliminates you want to see \n1.Bigg boss\n2.Dance jodi dance\n3.Cook with comali\n4.Comedy kings\n5.Super singer")
        opt = int(input())
        mycursor.execute("select wildcards.name,wildcards.total_votes,wildcards.entry_date,shows.show_name from wildcards inner join shows on wildcards.show_id=shows.show_id where shows.show_id=%s",(opt,))
        details=mycursor.fetchall()
        mycursor.execute("select wildcard_status from shows where show_id=%s;",(opt,))
        check=mycursor.fetchall()
        if(check[0][0]=='open'):
            mycursor.execute("select max(votes),name,e_id from eliminates where show_id=%s",(opt,))
            insert=mycursor.fetchall()
            id=insert[0][2]
            now= datetime.now()
            formatted = now.strftime('%Y-%m-%d %H:%M:%S')
            mycursor.execute("insert into wildcards(total_votes,entry_date,show_id,name) values(%s,%s,%s,%s)",(insert[0][0],formatted,opt,insert[0][1],))
            mydb.commit()
            mycursor.execute("delete from eliminates where e_id=%s",(id,))
            mydb.commit()
            mycursor.execute("update shows set wildcard_status=%s where show_id=%s",('closed',opt,))
            mydb.commit()
        mycursor.execute("select wildcards.name,wildcards.total_votes,wildcards.entry_date,shows.show_name from wildcards inner join shows on wildcards.show_id=shows.show_id where shows.show_id=%s",
            (opt,))
        details = mycursor.fetchall()
        for i in range(len(details)):
            row=details[i]
            print(i+1,' ','Name:',row[0],' ','Total votes:',row[1],' ','Entry date:',row[2],' ','Show:',row[3])


if __name__ == '__main__':
    username = str(input("Enter your name:"))
    userpassword = str(input("Enter password:"))
    user=userDetails(username,userpassword)
    isal= user.isAlreadyuser()
    if isal:
        
        while True:
            print("1.Reality Shows")
            print("2.Show contestants list")
            print("3.Show eliminated contestants")
            print("4.Show my previous votes")
            print("5.Show wilcard contestants")
            print("6.Exit")
            a=int(input("Enter your option:"))
            if(a==6):
                print("Thank you visit again")
                exit()
            if(a==1):
                s=show()
                s.displayShow()
            if(a==2):
                x=contestant(isal)
                x.displayContestant()
            if(a==3):
                e=eliminates(isal)
                e.displayEliminates()
            if(a==4):
                p=previousVote(isal)
                p.displayVotes()
            if(a==5):
                w=wildcard()
                w.displayWildcard()
    else:
        email=str(input("Enter your email:"))
        phone=str(input("Enter your phone number:"))
        mycursor.execute("insert into user_details(user_name,password,email,phone_number) values(%s,%s,%s,%s)",(username,userpassword,email,phone,))
        mydb.commit()
        print("you are successfully signed in")


