from datetime import datetime, timedelta
import mongoengine as me

class User(me.Document):
    username = me.StringField(required=True, unique=True, max_length=100)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    contact_number = me.StringField(required=True, max_length=15)
    full_name = me.StringField(required=True, max_length=200)
    profile_picture = me.URLField()
    job_title = me.StringField(max_length=100)
    department = me.StringField(max_length=100)
    location = me.StringField(max_length=150)
    short_bio = me.StringField(max_length=500)

    meta = {
        'collection': 'users',
        'indexes': ['username', 'email']
    }

class OTP(me.Document):
    email = me.EmailField(required=True)
    otp = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
    expires_at = me.DateTimeField(default=lambda: datetime.utcnow() + timedelta(minutes=5))

    meta = {
        'collection': 'otps',
        'indexes': ['email', 'otp', 'expires_at']
    }

    def is_expired(self):
        return self.expires_at < datetime.utcnow()

class Employee(me.Document):  # Changed class name to singular form
    username = me.StringField(required=True, unique=True, max_length=100)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    contact_number = me.StringField(required=True, max_length=15)
    isverified = me.BooleanField(default=False)

    meta = {
        'collection': 'employees',  # Plural form for the collection name
        'indexes': ['username', 'email']
    }

class Token(me.Document):
    employee = me.ReferenceField(Employee, required=True)  # Changed to singular 'employee'
    key = me.StringField(required=True, unique=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
    expires_at = me.DateTimeField(default=lambda: datetime.utcnow() + timedelta(days=7))  # Token valid for 7 days by default

    meta = {
        'collection': 'tokens'
    }

    def is_valid(self):
        return self.expires_at > datetime.utcnow() if self.expires_at else True
