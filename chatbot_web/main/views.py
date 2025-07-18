# 🔧 기본 Django 라이브러리
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.hashers import make_password, check_password # 비밀번호 해싱을 위해 추가
from dotenv import load_dotenv

# 🔧 파이썬 표준 라이브러리
import json
import sys
import os
import requests
from urllib.parse import quote_plus

# 🔧 로컬 모델
from .models import ChatSession, ChatMessage, Post, Comment, Notification # Comment 모델 임포트

# 🔧 시스템 경로 등록
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 🔧 외부 모듈 (LangChain 기반 응답 생성)
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from chat_agent import agent, generate_config
from llm_tools.chat_history_manager import chat_store

load_dotenv()
TOUR_API_KEY = os.getenv("TOUR_API_KEY")

# ===================================================
# 🌐 일반 페이지 뷰
# ===================================================

def index(request):
    return render(request, 'main/index.html')


def board(request):
    return render(request, 'main/board.html')


from datetime import date

@login_required
def profile(request):
    user = request.user

    # 챗봇 대화 수
    chat_session_count = ChatSession.objects.filter(user=user).count()

    # 내가 쓴 글 갯수
    post_count = Post.objects.filter(author=user).count()

    # 내가 쓴 댓글 갯수
    comment_count = Comment.objects.filter(user=user).count()

    # 가입일로부터 경과 일수 계산
    today = date.today()
    days_since_joined = (today - user.date_joined.date()).days

    context = {
        'chat_session_count': chat_session_count,
        'post_count': post_count,
        'comment_count': comment_count,
        'days_since_joined': days_since_joined,
    }
    return render(request, 'main/profile.html', context)

# ===================================================
# 🔐 사용자 인증
# ===================================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('main:home')
        else:
            return render(request, 'main/login.html', {'error': "Invalid username or password."})

    return render(request, 'main/login.html')


def logout_request(request):
    logout(request)
    messages.info(request, "로그아웃 되었습니다.")
    return redirect('main:home')


from django.core.mail import send_mail
from django.conf import settings

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')

        if password != password2:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return render(request, 'main/signup.html', {'username': username, 'nickname': nickname, 'email': email})

        if User.objects.filter(username=username).exists():
            messages.error(request, "이미 존재하는 아이디입니다.")
            return render(request, 'main/signup.html', {'username': username, 'nickname': nickname, 'email': email})

        if User.objects.filter(email=email).exists():
            messages.error(request, "이미 가입된 이메일 주소입니다.")
            return render(request, 'main/signup.html', {'username': username, 'nickname': nickname, 'email': email})

        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = nickname
        user.save()

        try:
            subject = '여행 나래에 오신 것을 환영합니다!'
            message = f'안녕하세요, {nickname}님! 여행 나래에 가입해주셔서 감사합니다.\n\n저희 서비스와 함께 즐거운 여행 계획을 세워보세요!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request, "회원가입이 완료되었습니다. 환영 이메일이 전송되었습니다.")
        except Exception as e:
            messages.warning(request, f"회원가입은 완료되었으나, 환영 이메일 전송에 실패했습니다: {e}")

        login(request, user)
        return redirect('main:home')

    return render(request, 'main/signup.html')

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
            return redirect('main:profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'main/profile_edit.html', {'form': form})


# ===================================================
# 💬 채팅 시스템: 페이지 + 대화 처리
# ===================================================

@login_required
def chatbot(request):
    # 이 뷰는 이제 chat_bot_view로 리디렉션하거나, 
    # 혹은 chat_bot_view가 직접 렌더링하도록 통합될 수 있습니다.
    # 여기서는 session_id 없이 chat_bot_view를 호출하도록 수정합니다.
    return chat_bot_view(request, session_id=None)


@login_required
def chatbot_redirect_to_latest_session(request):
    # 현재 사용자의 가장 최근 채팅 세션을 찾음
    latest_session = ChatSession.objects.filter(user=request.user).order_by('-created_at').first()

    if latest_session:
        # 가장 최근 세션으로 리디렉션
        return redirect('main:chat_bot', session_id=latest_session.id)
    else:
        # 채팅 세션이 없으면 새로 만들어서 해당 세션으로 이동
        return redirect('main:chatbot_new')


@login_required
def chat_bot_view(request, session_id=None):
    user = request.user
    sessions = ChatSession.objects.filter(user=user).order_by('-created_at')
    
    selected_session = None
    chat_messages = []

    if session_id:
        selected_session = get_object_or_404(ChatSession, id=session_id, user=user)
        chat_messages = selected_session.messages.order_by('timestamp')

    return render(request, 'main/chatbot.html', {
        'sessions': sessions,
        'selected_session': selected_session,
        'chat_messages': chat_messages,
    })

# ===================================================
# ⚙️ 유틸리티 함수: 세션 ID, 챗봇 응답
# ===================================================

def summarize_message(user_message):
    # LLM을 사용하여 메시지를 한 줄로 요약
    try:
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
        prompt = f"다음 사용자 메시지를 기반으로, 채팅방의 제목으로 쓸 짧은 요약을 12글자 이내로 생성해줘. 반말은 사용하지 마. 예를 들어, '경복궁 가는 길 알려줘'는 '경복궁 가는 길'로 요약해줘.\n\n사용자 메시지: {user_message}\n\n요약:"
        summary = llm.invoke(prompt).content.strip()
        return summary
    except Exception as e:
        # 요약 실패 시 기본 제목 반환
        print(f"Title summarization failed: {e}")
        return "새로운 채팅"

def get_session_id(request):
    # 인증된 유저의 고유 세션 키를 가져옴
    if request.user.is_authenticated:
        return request.user.username
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def chatbot_response(request, user_message):
    # LangChain 기반 챗봇 응답 생성
    session_id = get_session_id(request)
    app = agent()
    config = generate_config(session_id)
    state = {"session_id": session_id, "messages": [HumanMessage(content=user_message)]}

    try:
        response = app.invoke(state, config=config)
        return response["messages"][-1].content
    except Exception as e:
        return f"챗봇 오류 발생: {e}"

# ===================================================
# 🔄 비동기 API (AJAX 기반)
# ===================================================

@csrf_exempt
@login_required
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST 요청만 허용"}, status=405)

    try:
        data = json.loads(request.body)
        user_msg = data.get("message", "")
        session_id = data.get("session_id")

        session = None
        is_new_session = False
        if session_id:
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        else:
            # 새 세션인 경우, 임시 제목으로 생성
            if user_msg:
                session = ChatSession.objects.create(user=request.user, title="대화 시작...")
                is_new_session = True

        if not session:
            return JsonResponse({"error": "세션을 찾거나 생성할 수 없습니다."}, status=400)

        # 유저 메시지 저장
        ChatMessage.objects.create(session=session, role='user', content=user_msg)

        # AI 응답 생성
        reply = chatbot_response(request, user_msg)

        # AI 메시지 저장
        ChatMessage.objects.create(session=session, role='assistant', content=reply)

        response_data = {"reply": reply}
        if is_new_session:
            response_data["new_session_id"] = session.id

        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({"error": f"요청 처리 오류: {str(e)}"}, status=500)

@login_required
def search_chat_sessions(request):
    query = request.GET.get('query', '')
    if not query:
        # 검색어가 없으면 모든 세션을 반환 (또는 빈 목록을 반환할 수도 있음)
        sessions = ChatSession.objects.filter(user=request.user).values_list('id', flat=True)
        return JsonResponse({'session_ids': list(sessions)})

    # 메시지 내용에 검색어가 포함된 세션을 찾음
    matching_sessions = ChatSession.objects.filter(
        user=request.user,
        messages__content__icontains=query
    ).distinct().values_list('id', flat=True)

    return JsonResponse({'session_ids': list(matching_sessions)})


@csrf_exempt
@login_required
def update_chat_title(request, session_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_message = data.get('first_message')
            if not first_message:
                return JsonResponse({'status': 'error', 'message': '첫 메시지가 필요합니다.'}, status=400)

            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
            
            # 제목 요약 및 업데이트
            new_title = summarize_message(first_message)
            session.title = new_title
            session.save()
            
            return JsonResponse({'status': 'success', 'new_title': new_title})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'POST 요청만 허용됩니다.'}, status=405)


@csrf_exempt
@login_required
def delete_chat_session(request, session_id):
    if request.method == 'DELETE':
        try:
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
            session.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'DELETE method required'}, status=405)


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    notification_list = []
    for notif in notifications:
        notification_list.append({
            'id': notif.id,
            'message': notif.message,
            'link': notif.link,
            'created_at': notif.created_at.strftime("%Y-%m-%d %H:%M"),
            'is_read': notif.is_read
        })
    return JsonResponse({'notifications': notification_list})


@csrf_exempt
@login_required
def mark_notification_as_read(request, notification_id):
    if request.method == 'POST':
        try:
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=405)


# ===================================================
# 여행코스 추천 + 호버링 기능 구현 map
# ===================================================
    


from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import certifi

# 🔐 OpenSSL 보안 우회용 어댑터 정의
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')  # 낮은 보안 수준 허용
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# 💥 적용된 함수
def recommendation(request):
    tour_api_key = os.getenv("TOUR_API_KEY")
    recommended_items = []

    if request.method == 'POST':
        area_code = request.POST.get('region')
        sigungu_code = request.POST.get('sub-region')

        url = "https://apis.data.go.kr/B551011/KorService2/areaBasedList2"
        params = {
            'serviceKey': tour_api_key,
            'MobileOS': 'ETC',
            'MobileApp': 'MyApp',
            '_type': 'json',
            'numOfRows': 10,
            'pageNo': 1,
            'areaCode': area_code,
            'sigunguCode': sigungu_code,
            'contentTypeId': 12,
        }

        try:
            # 세션에 어댑터 장착
            session = requests.Session()
            session.mount("https://", TLSAdapter())

            response = session.get(url, params=params,verify=certifi.where())
            response.raise_for_status()
            data = response.json()

            if data and data['response']['body']['items']:
                items = data['response']['body']['items']['item']
                if isinstance(items, dict):
                    recommended_items.append(items)
                else:
                    recommended_items = items
            else:
                messages.info(request, "해당 지역에 대한 추천 여행지가 없습니다.")

        except requests.exceptions.RequestException as e:
            messages.error(request, f"API 호출 중 오류 발생: {e}")
        except KeyError:
            messages.error(request, "API 응답 구조가 예상과 다릅니다.")

    return render(request, 'main/recommended.html', {
        'TOUR_API_KEY': tour_api_key,
        'recommended_items': recommended_items,
    })


def map_view(request):
    return render(request, 'main/heritage_map.html')  # 아직 구현 안 됐음

# ===================================================
# 📝 게시판 기능
# ===================================================

from django.db.models import Count # Count 임포트 추가
from .forms import CommentForm, UserChangeForm # UserChangeForm 임포트 추가

class PostListView(ListView):
    model = Post
    template_name = 'main/board_list.html'  # 게시글 목록을 보여줄 템플릿
    context_object_name = 'posts'  # 템플릿에서 사용할 변수 이름
    paginate_by = 10  # 한 페이지에 10개의 게시글
    # ordering = ['-created_at']  # 최신순 정렬 추가

    def get_queryset(self):
        # 일반 게시글 (is_announcement=False)은 created_at 역순으로 정렬
        normal_posts = super().get_queryset().filter(is_announcement=False).annotate(
            likes_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        ).order_by('-created_at')

        # 페이지네이션을 위해 일반 게시글만 사용
        return normal_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 공지 게시글을 별도로 컨텍스트에 추가
        context['announcements'] = Post.objects.filter(is_announcement=True).annotate(
            likes_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        ).order_by('-created_at')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'main/board_detail.html'  # 게시글 상세를 보여줄 템플릿
    context_object_name = 'post'  # 템플릿에서 사용할 변수 이름

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.error(request, "요청하신 게시글을 찾을 수 없거나 삭제되었습니다.")
            return redirect('main:board_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_superuser'] = self.request.user.is_superuser
        # 최상위 댓글만 가져오고, 템플릿에서 재귀적으로 대댓글을 렌더링
        context['comments'] = self.object.comments.filter(parent__isnull=True).order_by('created_at')
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'main/board_form.html'  # 게시글 작성 폼 템플릿
    fields = ['title', 'content', 'is_anonymous']  # 사용자가 입력할 필드
    success_url = reverse_lazy('main:board_list')  # 작성 성공 시 이동할 URL

    def form_valid(self, form):
        form.instance.author = self.request.user  # 작성자를 현재 로그인한 사용자로 설정
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'main/board_form.html'  # 게시글 수정 폼 템플릿
    fields = ['title', 'content', 'is_anonymous']  # 사용자가 수정할 필드
    success_url = reverse_lazy('main:board_list')  # 수정 성공 시 이동할 URL

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser  # 작성자이거나 superuser인 경우 수정 가능

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'main/board_confirm_delete.html'  # 게시글 삭제 확인 템플릿
    success_url = reverse_lazy('main:board_list')  # 삭제 성공 시 이동할 URL

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser # 작성자이거나 superuser인 경우 삭제 가능

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # 게시글과 관련된 모든 알림 삭제
        Notification.objects.filter(link=reverse_lazy('main:board_detail', kwargs={'pk': self.object.pk})).delete()
        return super().delete(request, *args, **kwargs)

@login_required
@csrf_exempt
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if request.method == 'POST':
        data = json.loads(request.body or '{}')
        force_like = data.get('force_like', False)

        if force_like:
            if user not in post.likes.all():
                post.likes.add(user)
            liked = True
        else:
            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
            else:
                post.likes.add(user)
                liked = True
        
        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
    return JsonResponse({'error': 'Invalid request', 'status': 400})

@csrf_exempt
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        data = json.loads(request.body)
        author_name = data.get('author_name')
        password = data.get('password')
        content = data.get('content')
        parent_id = data.get('parent_id')

        # 로그인한 사용자인 경우 user 필드에 저장
        comment_user = request.user if request.user.is_authenticated else None

        if not all([author_name, password, content]):
            return JsonResponse({'error': '모든 필드를 입력해주세요.'}, status=400)

        hashed_password = make_password(password)
        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(pk=parent_id)
                if parent_comment.parent:
                    return JsonResponse({'error': '대댓글에는 다시 대댓글을 달 수 없습니다.'}, status=400)
            except Comment.DoesNotExist:
                return JsonResponse({'error': '부모 댓글을 찾을 수 없습니다.'}, status=404)

        comment = Comment.objects.create(
            post=post,
            user=comment_user, # user 필드 추가
            parent=parent_comment,
            author_name=author_name,
            password=hashed_password,
            content=content
        )

        # 게시글 작성자에게 댓글 알림 생성
        if post.author != request.user: # 자신의 게시글에 댓글을 달면 알림을 보내지 않음
            Notification.objects.create(
                user=post.author,
                message=f'{author_name}님이 회원님의 게시글 "{post.title}"에 댓글을 남겼습니다.',
                link=reverse_lazy('main:board_detail', kwargs={'pk': post.pk})
            )
        return JsonResponse({
            'success': True,
            'author_name': comment.author_name,
            'content': comment.content,
            'created_at': comment.created_at.strftime("%Y.%m.%d %H:%M"),
            'comment_id': comment.id,
            'parent_id': comment.parent_id
        })
    return JsonResponse({'error': 'Invalid request', 'status': 400})

@csrf_exempt
def delete_comment(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        data = json.loads(request.body)
        password = data.get('password')

        # superuser인 경우 비밀번호 확인 없이 바로 삭제 (소프트 삭제)
        if request.user.is_superuser:
            comment.content = "관리자에 의해 삭제된 메시지입니다."
            comment.is_deleted_by_admin = True
            comment.save()
            return JsonResponse({'success': True, 'is_soft_deleted': True, 'new_content': comment.content})

        # 일반 사용자인 경우 비밀번호 확인 후 완전 삭제
        if not password:
            return JsonResponse({'error': '비밀번호를 입력해주세요.'}, status=400)

        if check_password(password, comment.password):
            comment.delete()
            return JsonResponse({'success': True, 'is_soft_deleted': False})
        else:
            return JsonResponse({'error': '비밀번호가 일치하지 않습니다.'}, status=403)
    return JsonResponse({'error': 'Invalid request', 'status': 400})

@login_required
@csrf_exempt
def toggle_announcement(request, pk):
    if not request.user.is_superuser:
        return JsonResponse({'error': '권한이 없습니다.'}, status=403)

    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        post.is_announcement = not post.is_announcement
        post.save()

        # 모든 활성 사용자에게 공지 알림 생성
        message_text = f'새로운 공지사항: "{post.title}"이(가) 등록되었습니다.' if post.is_announcement else f'공지사항 "{post.title}"이(가) 해제되었습니다.'
        link_url = reverse_lazy('main:board_detail', kwargs={'pk': post.pk})

        for user in User.objects.filter(is_active=True):
            Notification.objects.create(
                user=user,
                message=message_text,
                link=link_url
            )

        return JsonResponse({'success': True, 'is_announcement': post.is_announcement})
    return JsonResponse({'error': 'Invalid request method'}, status=405)