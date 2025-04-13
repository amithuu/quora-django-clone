from users.models import *
from rest_framework import serializers
import random
import string
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','phone', 'first_name', 'last_name']
        
    
    def create(self, validated_data):
        try:
            with transaction.atomic():
                password = ''.join(random.choices(string.ascii_lowercase, k=6))
                user = CustomUser.objects.create(
                    email = validated_data['email'],
                    first_name = validated_data['first_name'],
                    last_name = validated_data['last_name'],
                    phone = validated_data['phone'],
                )
                print(f'Email sent to {user.email} with password: {password}')
                
                user.set_password(password)
                user.save()

                
                ## once user is cerate we will send the email for him through SFTP
                from users.utils import send_password_email
                send_password_email(validated_data['email'], password)
                
                return user 
        except Exception as e:
            raise serializers.ValidationError({'error': f'User creation failed: {str(e)}'})
        
        


class CustomLoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        print(data)
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')
        
        try:
            user = CustomUser.objects.get(email = email_or_phone)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(phone = email_or_phone)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid email or phone number.")
            
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")
        
        refresh = RefreshToken.for_user(user)
        
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','title', 'body']
        read_only_fields = ['id', 'user', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    question_title = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Answer
        fields = ['id','question','question_title','answer','like_count']
        read_only_fields = ['id', 'user', 'created_at','question_title']
        
    def get_question_title(self, obj):
        return obj.question.title
    
    def get_like_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'answer', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']