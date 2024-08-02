from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import boto3
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/user_management'
CORS(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    picture_url = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    about = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)


s3 = boto3.client('s3', aws_access_key_id='enter access', aws_secret_access_key='enter secret')
BUCKET_NAME = 'ijse-inclass-assignment'

@app.route("/", methods=["GET"])
def index():
    return "<h1>Hello world</h1>"

@app.route("/api/user", methods=["POST"])
def create_user():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    dob = request.form['dob']
    picture = request.files['picture']
    username = request.form['username']
    about = request.form['about']
    
    age = datetime.now().year - datetime.strptime(dob, '%Y-%m-%d').year
    
    # Upload picture to S3
    picture_filename = f"{firstName}_{picture.filename}"
    s3.upload_fileobj(picture, BUCKET_NAME, "user_image/"+picture_filename)
    picture_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{picture_filename}"

    user = User(first_name=firstName, last_name=lastName, email=email, dob=dob, picture_url=picture_url , username=username, about=about)
    db.session.add(user)
    db.session.commit()
    return jsonify({})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
    