from django.urls import path, include, reverse_lazy # include, reverse_lazy 추가
from . import views
from django.contrib.auth import views as auth_views # Django 기본 인증 뷰 임포트
from .forms import CustomPasswordResetForm # CustomPasswordResetForm 임포트

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('chatbot/', views.chatbot_redirect_to_latest_session, name='chatbot'),
    path('chatbot/new/', views.chat_bot_view, name='chatbot_new'),
    path('login/', views.login_view, name='login'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile, name="profile"),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('signup/', views.signup, name='signup'),
    path('chatbot/<int:session_id>/', views.chat_bot_view, name='chat_bot'),
    path('api/chat/search/', views.search_chat_sessions, name='search_chat_sessions'),
    path('api/chat/update_title/<int:session_id>/', views.update_chat_title, name='update_chat_title'),
    path('api/chat/session/<int:session_id>/delete/', views.delete_chat_session, name='delete_chat_session'),
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('map/', views.map_view, name='map'),

    # 비밀번호 재설정 URL
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='main/password_reset_form.html',
        email_template_name='main/password_reset_email.html',
        subject_template_name='main/password_reset_subject.txt', # 제목 템플릿 명시
        success_url=reverse_lazy('main:password_reset_done'),
        form_class=CustomPasswordResetForm # CustomPasswordResetForm 사용
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='main/password_reset_confirm.html',
        success_url=reverse_lazy('main:password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name='password_reset_complete'),

    # 게시판 URL
    path('board/', views.PostListView.as_view(), name='board_list'),
    path('board/<int:pk>/', views.PostDetailView.as_view(), name='board_detail'),
    path('board/new/', views.PostCreateView.as_view(), name='board_new'),
    path('board/<int:pk>/edit/', views.PostUpdateView.as_view(), name='board_edit'),
    path('board/<int:pk>/delete/', views.PostDeleteView.as_view(), name='board_delete'),
    path('api/board/<int:pk>/like/', views.like_post, name='like_post'),
    path('api/board/<int:pk>/comments/add/', views.add_comment, name='add_comment'),
    path('api/comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('api/board/<int:pk>/toggle_announcement/', views.toggle_announcement, name='toggle_announcement'),
]