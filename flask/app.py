from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow 
from flask_cors import CORS #ModuleNotFoundError: No module named 'flask_cors' = pip install Flask-Cors
 
app = Flask(__name__)
CORS(app)
 
# Databse configuration                                  Username:password@hostname/databasename
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
 
ma=Marshmallow(app)
 
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date = db.Column(db.DateTime,default=datetime.datetime.now)
 
    def __init__(self,name,email):
        self.name=name
        self.email=email
 
 
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','date')
 
user_schema = UserSchema()
users_schema = UserSchema(many=True)
 
@app.route('/listusers',methods =['GET'])
def listusers():
    all_users = Users.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)
 
@app.route('/userdetails/<id>',methods =['GET'])
def userdetails(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)
 
@app.route('/userupdate/<id>',methods = ['PUT'])
def userupdate(id):
    user = Users.query.get(id)
 
    name = request.json['name']
    email = request.json['email']
 
    user.name = name
    user.email = email
 
    db.session.commit()
    return user_schema.jsonify(user)
 
@app.route('/userdelete/<id>',methods=['DELETE'])
def userdelete(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
 
@app.route('/useradd',methods=['POST'])
def useradd():
    name = request.json['name']
    email = request.json['email']
 
    users = Users(name,email)
    db.session.add(users)
    db.session.commit()
    return user_schema.jsonify(users)
 
if __name__=='__main__':
    app.run(debug=True)