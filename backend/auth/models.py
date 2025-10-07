from extensions import db
import re
from sqlalchemy.orm import validates
class User(db.Model):
    __bind_key__ = 'auth'   
    __tablename__="loginpage"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False)

    def to_dict(self):
        return{
            "id":self.id,
            "username":self.username,
            "password":self.password
        }
    EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'

    @validates("username")
    def validate_username(self, key, username):
        if not re.match(self.EMAIL_REGEX, username):
            raise ValueError("Invalid email address")
        return username

    @validates("password")
    def validate_password(self, key, password):
        if not re.match(self.PASSWORD_REGEX, password):
            raise ValueError(
                "Password must have 1 uppercase, 1 lowercase, 1 number, "
                "1 special character, and be at least 8 characters long"
            )
        return password

class Profile(db.Model):
    __bind_key__ = 'auth'  # same database or different if needed
    __tablename__ = "user_profile"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('loginpage.id'), unique=True, nullable=False)
    
    # Profile fields
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    
    # Relationship with User
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "bio": self.bio,
            "phone_number": self.phone_number
        }


    
