from django.shortcuts import get_object_or_404
from users.models import *
from users.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
# Create your views here.

class RegisterView(APIView):
    
    def get(self,request):
        user = CustomUser.objects.all().order_by('-id')
        serializer = RegisterSerilaizer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegisterSerilaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User saved Successfully and Password has been sent on email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id=None):
        try:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return Response({'message': 'User Deleted Successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self, request):
        serilaizer = CustomLoginSerializer(data=request.data)
        if serilaizer.is_valid():
            return Response({'message': 'Login Success','tokens': serilaizer.validated_data}, status=status.HTTP_200_OK)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class QuestionView(APIView):
        permission_classes  = [IsAuthenticated]
        
        def get(self, request, id=None):
            if id:
                if request.user.id != id :
                    return Response({'message': 'You are not authorized to view this question'}, status=status.HTTP_403_FORBIDDEN)
                questions = Question.objects.filter(id=id)
            else:
                questions = Question.objects.all().order_by('-id')
            
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        def post(self, request):
            serializers  = QuestionSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save(user=request.user)
                return Response({'message': 'Question Created Successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            if request.user.id != id:
                return Response({'message': 'You are not authorized to view this answer'}, status=status.HTTP_403_FORBIDDEN)
            answers = Answer.objects.filter(id=id)
        else:
            answer = Answer.objects.all().order_by('-id')

        serializer = AnswerSerializer(answer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Answer Posted Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        answer_id = request.data.get('answer')
        if not answer_id:
            return Response({'error': 'Answer ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        answer = get_object_or_404(Answer, id=answer_id)

        # Check if already liked → Unlike
        like = Like.objects.filter(user=request.user, answer=answer).first()
        if like:
            like.delete()
            return Response({'message': 'Unliked'}, status=status.HTTP_200_OK)
        
        # Else like it
        Like.objects.create(user=request.user, answer=answer)
        return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)
    
    
class LikedAnswersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        likes = Like.objects.filter(user=request.user).select_related('answer').order_by('-created_at')
        answers = [like.answer for like in likes]
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AnswerLikesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, answer_id):
        likes = Like.objects.filter(answer_id=answer_id).select_related('user')
        data = [{'user_id': like.user.id, 'username': like.user.username} for like in likes]
        return Response(data, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)