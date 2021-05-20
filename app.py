from flask import Flask,render_template,request,send_file
from flask_sqlalchemy import SQLAlchemy
from send_email import sendEmail
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename

app = Flask(__name__)

#Configuring the database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@localhost/height_collector'
db=SQLAlchemy(app)


#Creating table
#from scipt import db
#db.create_all()

class Data(db.Model):
    
    #Declaring the db variables
    __tablename__ = 'data'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120),unique=True)
    height=db.Column(db.Integer)
    
    def __init__(self,email,height):
        self.email = email
        self.height = height
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success',methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email_add']
        height = request.form['height']
        print(email,height)
        
        #Checking if the email present or not
        if db.session.query(Data).filter(Data.email == email).count() == 0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            avgHeight = db.session.query(func.avg(Data.height)).scalar()
            noOfHeights = db.session.query(Data.height).count()
            avgHeight = round(avgHeight,2)
            try:
                sendEmail(email,avgHeight)
            except:
                return render_template('index.html',text="Something went wrong!!!")
                    
            return render_template('success.html')
        else:
            # return render_template('failure.html')
            return render_template('index.html',text="Sorry!Email has been taken!")
       


#Uploading file
@app.route('/upload')
def upload():
    if request.method == 'POST':
        global file
        file = request.files['inFile']
        contents=file.read()
        
        #Saving file
        file.save(secure_filename("Uploaded_file_"+file.filename))
        # print(contents)
        
        #Implementing download button
        return render_template('fileSuccess.html',btn="dn.html")
        #return render_template('index.html',btn="dn.html")
       
#Downloading file
@app.route('/download',methods=['POST'])
def download():
    return send_file("Uploaded_file_"+file.filename,attachment_filename="uploadedfile",as_attachment=True)
  
if __name__ == '__main__':
    app.debug=True
    app.run()