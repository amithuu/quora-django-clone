from users import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('register/<int:id>/', views.RegisterView.as_view(), name = 'delete-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('questions/', views.QuestionView.as_view(), name='questions'),
    path('questions/<int:id>', views.QuestionView.as_view(), name='questions'),
    path('answers/', views.AnswerView.as_view(), name='answer'),
    path('answers/<int:id>', views.AnswerView.as_view(), name='answer'),
    path('like/', views.LikeView.as_view(), name='like-answer'),
    path('liked-answers/', views.LikedAnswersView.as_view(), name='liked-answers'),
    path('answer-likes/<int:answer_id>/', views.AnswerLikesView.as_view(), name='answer-likes'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]


