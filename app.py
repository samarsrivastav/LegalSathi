from flask import Flask,redirect,request,render_template,url_for,jsonify,flash

import pyrebase
import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv
load_dotenv()

cred = credentials.Certificate("legalsathi-28082-firebase-adminsdk-g7weq-ec492b1a85.json")
firebase_admin.initialize_app(cred)



app=Flask(__name__)
app.secret_key='MyFlaskApp'


config = {
  "apiKey": os.getenv('apiKey'),
  "authDomain": os.getenv('authDomain'),
  "databaseURL": os.getenv('databaseURL'),
  "storageBucket": "PASTE_HERE"
}


#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#to keep session data for client or lawyer
lawyer = {"is_logged_in": False, "name": "", "email": "", "lid": ""}
client = {"is_logged_in": False, "name": "", "email": "", "lid": ""}


@app.route("/")
def landing():
    #session out for both client or lawyer
    client["is_logged_in"] = False
    client["email"] = ""
    client["name"] = ""
    client["uid"] = ""
    lawyer["is_logged_in"] = False
    lawyer["email"] = ""
    lawyer["name"] = ""
    return render_template("index.html")

@app.route("/client_register",methods=['GET','POST'])
def client_register():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass']
             #Try signing in the user with the given information
        try:

            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global client
            client["is_logged_in"] = True
            client["email"] = user["email"]
            client["name"] = username
            client["uid"] = user["localId"]
            flash("Logged In Successfully")
            return redirect(url_for('clientHome'))
        
            #If there is any error, redirect back to login
            # return redirect(url_for('client_register'))
        except:
            #If there is any error, redirect back to login
            flash("Login not Successful")
            return redirect(url_for('client_register'))
        
 
    else:
        return render_template("register_client.html")
    



@app.route("/lawyer_register",methods=['GET','POST'])
def lawyer_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['e-mail']
        zipcode=request.form['zipcode']
        phno = request.form['number']
        address = request.form['fulladdress']
        experience = request.form['experience']
        speciality= request.form['Speciality']
        qualification = request.form['qualification']
        bio = request.form['bio']
        lawyer["is_logged_in"] = True
        lawyer["email"] = email
        lawyer["name"] = fullname
        
        db.child("LegalSathi").child("lawyers").child(fullname).update({'address':address,'email':email,'bio':bio,'experience':experience,'name':fullname,'phone':phno,'qualification':qualification,'speciality':speciality,'token':50,'zipcode':zipcode})
        db.child("LegalSathi").child("token").update({fullname:50})
        data=data=db.child("LegalSathi").child("lawyers").child(lawyer["name"]).get()
        return render_template("profile.html",data=data.val())

        


    return render_template("register_lawyer.html")

@app.route("/clienthome")
def clientHome():
    return render_template("clientHome.html")



@app.route("/leaderboard")
def leaderboard():
    data=db.child("LegalSathi").child("token").get().val()
    print(client['email'])
    sortedDict = sorted(data.items(), key=lambda x:x[1])
    name =[]
    token=[]
    for i in range(len(sortedDict)-1,-1,-1):
          f = sortedDict[i]
          name.append(f[0])
          token.append(f[1])
          
    
    return render_template("leaderBoard.html",board=zip(name,token))

@app.route("/lawyerfilter")
def lawyerfilter():
    data=db.child("LegalSathi").child("token").get().val()
    sortedDict = sorted(data.items(), key=lambda x:x[1])
    name =[]
    token=[]
    for i in range(len(sortedDict)-1,-1,-1):
          f = sortedDict[i]
          name.append(f[0])
          token.append(f[1])
    items=[]
    if request.method == 'POST':
        experience = request.form['experience']
        speciality= request.form['speciality']
        location= request.form['location']
        if(experience != "none" and speciality != "none" and location != "none" ):
            
    
            
            for i in range(len(sortedDict)):
                spec=db.child("LegalSathi").child("lawyers").child(name[i]).child("speciality").get()
                loc=db.child("LegalSathi").child("lawyers").child(name[i]).child("location").get()
                exp=db.child("LegalSathi").child("lawyers").child(name[i]).child("experience").get()
                if(spec == speciality and loc == location and  exp == experience):
                    items.append([name[i],exp,loc])
            return render_template('ClientLawyer.html',items=items)
        else:
            if(experience != "none" and speciality != "none"):
                 
            
                for i in range(len(sortedDict)):
                    spec=db.child("LegalSathi").child("lawyers").child(name[i]).child("speciality").get()
                    loc=db.child("LegalSathi").child("lawyers").child(name[i]).child("location").get()
                    exp=db.child("LegalSathi").child("lawyers").child(name[i]).child("experience").get()
                    if(spec == speciality and  exp == experience):
                        items.append([name[i],exp,loc])
                return render_template('ClientLawyer.html',items=items)
            elif(speciality != "none" and location != "none"):
                 
            
                for i in range(len(sortedDict)):
                    spec=db.child("LegalSathi").child("lawyers").child(name[i]).child("speciality").get()
                    loc=db.child("LegalSathi").child("lawyers").child(name[i]).child("location").get()
                    exp=db.child("LegalSathi").child("lawyers").child(name[i]).child("experience").get()
                    if(spec == speciality and  loc == location):
                        items.append([name[i],exp,loc])
                return render_template('ClientLawyer.html',items=items)
            elif(experience != "none" and location != "none"):
                  
            
                for i in range(len(sortedDict)):
                    spec=db.child("LegalSathi").child("lawyers").child(name[i]).child("speciality").get()
                    loc=db.child("LegalSathi").child("lawyers").child(name[i]).child("location").get()
                    exp=db.child("LegalSathi").child("lawyers").child(name[i]).child("experience").get()
                    if(exp == experience and  loc == location):
                        items.append([name[i],exp,loc])
                return render_template('ClientLawyer.html',items=items)
            elif(experience != "none"):
                 
            
                for i in range(len(sortedDict)):
                    spec=db.child("LegalSathi").child("lawyers").child(name[i]).child("speciality").get()
                    loc=db.child("LegalSathi").child("lawyers").child(name[i]).child("location").get()
                    exp=db.child("LegalSathi").child("lawyers").child(name[i]).child("experience").get()
                    if(exp == experience ):
                        items.append([name[i],exp,loc])
                return render_template('ClientLawyer.html',items=items)
            elif(speciality != "none"):
                  
            
                for i in range(len(sortedDict)):
                    spec=db.child("LegalSathi").child("lawyers").child(name[i]).child("speciality").get()
                    loc=db.child("LegalSathi").child("lawyers").child(name[i]).child("location").get()
                    exp=db.child("LegalSathi").child("lawyers").child(name[i]).child("experience").get()
                    if(spec == speciality ):
                        items.append([name[i],exp,loc])
                return render_template('ClientLawyer.html',items=items)
            else:
                 
            
                for i in range(len(sortedDict)):
                    spec=db.child("LegalSathi").child("lawyers").child(name[i]).child("speciality").get()
                    loc=db.child("LegalSathi").child("lawyers").child(name[i]).child("location").get()
                    exp=db.child("LegalSathi").child("lawyers").child(name[i]).child("experience").get()
                    if(loc == location ):
                        items.append([name[i],exp,loc])
                return render_template('ClientLawyer.html',items=items)
    else:
        for i in range(len(sortedDict)):
                spec=db.child("LegalSathi").child("lawyers").child(name[i]).child("speciality").get()
                loc=db.child("LegalSathi").child("lawyers").child(name[i]).child("location").get()
                exp=db.child("LegalSathi").child("lawyers").child(name[i]).child("experience").get()
                items.append([name[i],exp,loc])
        return render_template('ClientLawyer.html',items=items)

@app.route("/lawyerdetails")
def lawyerdetails():
    name= request.args.get('name')
    data=db.child("LegalSathi").child("lawyers").child(name).get().val()
    return render_template("lawyerDetails.html",items=data)

         
@app.route('/casehire', methods=["POST"])
def add_token():
    
    
    if request.method == 'POST':
        name= request.args.get('name')
        exis_token = db.child('LegalSathi').child("lawyers").child(name).child("token").get().val()
        assign_hire_token = 50 +exis_token
        
        
        # if not username:
        #     return jsonify({
        #         "message": "Invalid username"
        #     }), 400
        
        # if not token:
        #     return jsonify({
        #         "message": "Token not found"
        #     }), 400
        
        # Update the tokens in Firebase
        print(client["name"])
        speciality=db.child('LegalSathi').child("lawyers").child(name).child("speciality").get().val()
        # db.child('LegalSathi').child("tokenupdated").child(name).update(assign_hire_token)
        db.child('LegalSathi').child("lawyers").child(name).update({"token":assign_hire_token})
        db.child('LegalSathi').child("token").update({name:assign_hire_token})
        db.child('LegalSathi').child("lawyerclient").child(name).child(client["name"]).update({"specialty":speciality})
        #return the required template 
        data=db.child("LegalSathi").child("lawyers").child(name).get().val()
        flash("Lawyer: "+name+" is hired for your case")
        return render_template("lawyerDetails.html",show=True,items=data)
             
@app.route('/currentcase', methods=["POST"])
def currentcase():

    data=db.child('LegalSathi').child("lawyerclient").child(lawyer["name"]).get().val()
    if len(data)==0:
        return render_template("curentcase.html",found=False)
        
    else:
        items=[]
        for client,details in data.items():
            items.append([client,details['speciality']])
        return render_template("curentcase.html",items=items)
    
@app.route('/access',methods=['POST'])
def access():
    if request.method == 'POST':
        tool=request.form['tool']
        
        exis_token = db.child('LegalSathi').child("lawyers").child(lawyer["name"]).child("token").get().val()
        if tool =="docasst":
            if exis_token <= 30:
                flash("You do not have enough tokens to redeem for accessing this tool")
                return str('subscriptionpage')
            else:
                assign_token = exis_token-30
                db.child('LegalSathi').child("lawyers").child(lawyer["name"]).update({"token":assign_token})
                return redirect('http://localhost:8501')



        elif tool =="docsum":
            if exis_token <= 10:
                flash("You do not have enough tokens to redeem for accessing the tool")
                return str('subscriptionpage')
            else:
                assign_token = exis_token-10
                db.child('LegalSathi').child("lawyers").child(lawyer["name"]).update({"token":assign_token})
                return redirect('http://localhost:8502')
        else:
            return str('subscriptionpage')
    else:
        return str('subscriptionpage')

        
    
    

    
    
    
        


    
          
    
    
if __name__=="__main__":
    
    app.run(debug=True)