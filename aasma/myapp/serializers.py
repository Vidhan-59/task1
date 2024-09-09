import re
import bcrypt
from rest_framework import serializers
from .models import User, Employee  # Adjust the import according to your app structure


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    contact_number = serializers.CharField(max_length=15)
    full_name = serializers.CharField(max_length=200, required=True)
    profile_picture = serializers.URLField(required=False, allow_null=True)
    job_title = serializers.CharField(max_length=100, required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_null=True)
    location = serializers.CharField(max_length=150, required=False, allow_null=True)
    short_bio = serializers.CharField(max_length=500, required=False, allow_null=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserDetailSerializer(serializers.Serializer):
    id = serializers.CharField()  # Use CharField for ObjectId
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    contact_number = serializers.CharField(max_length=15)
    full_name = serializers.CharField(max_length=200)
    profile_picture = serializers.URLField(allow_null=True, required=False)
    job_title = serializers.CharField(max_length=100, allow_null=True, required=False)
    department = serializers.CharField(max_length=100, allow_null=True, required=False)
    location = serializers.CharField(max_length=150, allow_null=True, required=False)
    short_bio = serializers.CharField(max_length=500, allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert ObjectId to string representation
        representation['id'] = str(instance.id)
        return representation
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    contact_number = serializers.CharField(max_length=15)

    def validate(self, data):

        if Employee.objects(username=data['username']).first():
            raise serializers.ValidationError("Username already exists")

        if Employee.objects(email=data['email']).first():
            raise serializers.ValidationError("Email already exists")

        password = data['password']
        if len(password) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long")
        if not re.search(r'\d', password):
            raise serializers.ValidationError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Password must contain at least one special character")

        contact_number = data['contact_number']
        if not re.fullmatch(r'\d{10,15}', contact_number):
            raise serializers.ValidationError("Contact number must be between 10 and 15 digits long")

        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print('123')
        username = data.get('username')
        password = data.get('password')

        # Authenticate user
        try:
            user = Employee.objects.get(username=username)
            print(user.username)
        except:
            raise serializers.ValidationError("Invalid username or password.")

        # Check if the password is correct
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise serializers.ValidationError("Invalid username or password.")

        return data


from rest_framework import serializers

class UserProfileSerializer(serializers.Serializer):
    user_id = serializers.CharField(source='id', read_only=True)  # Adjust for `id` field
    profile_picture = serializers.URLField(required=False, allow_null=True)
    full_name = serializers.CharField(max_length=200)
    job_title = serializers.CharField(max_length=100, required=False, allow_null=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Ensure _id is included as user_id in the output
        return representation
