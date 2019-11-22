import jwt
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from .forms import SignupForm
from .models import ChatRoom, LoggedInUser
import json


User = get_user_model()


def home(request):
    return render(request, 'chat/home.html')


@login_required(login_url='/')
def user_list(request):
    users = User.objects.select_related('logged_in_user')
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Off-line'
    username = request.user
    mess = ChatRoom.objects.all()
    arr = []
    for i in range(len(mess.values())):
        if mess.values()[i]["room_name"] not in arr:
            arr.append(mess.values()[i]["room_name"])
    print(arr)
    return render(request, 'mysite/userlist.html', {'users': users, 'username': username, 'rooms': arr})


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user is not None:
                login(request, user)
                return redirect(reverse('mysite:user_list'))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, 'mysite/login.html')
    return render(request, 'mysite/login.html')


def reset_link(request):
    if request.method == 'POST':
        to_email = request.POST['email']
        current_site = get_current_site(request)

        mail_subject = 'Reset your password.'
        jwt_token = jwt.encode({'Email': to_email}, 'private_key', algorithm='HS256').decode("utf-8")
        email = EmailMessage(
            mail_subject,
            'http://' + str(current_site.domain) + '/chat/resetpassword/' + jwt_token + '/',
            to=[to_email]
        )
        email.send()
        return render(request, 'mysite/checkmail.html')
    else:
        form = PasswordResetForm()
    return render(request, "mysite/resetpassword.html",
                  {"form": form})


@login_required(login_url='/login/')
def log_out(request):
    logout(request)
    return redirect(reverse('mysite:log_in'))


@login_required(login_url='/login')
def create_Chat_Room(request):
    return render(request, 'chat/index.html', {})


@login_required(login_url='/')
def chat_room(request, room_name):
    users = User.objects.select_related('logged_in_user')
    username = request.user
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'off-line'
    loggedusers = LoggedInUser.objects.all()  # new
    message = ChatRoom.objects.filter(room_name=room_name).values('message')  # new
    message = list(message)
    return render(request, 'chat/room.html',
                  {"room_name_json": room_name, 'online user': loggedusers,
                   'message': mark_safe(json.dumps(message)), 'users': users, 'username': username
                   }
                  )


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # User Activation Through mail
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            jwt_token = jwt.encode({user.username: user.email}, 'private_key', algorithm='HS256').decode("utf-8")
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject,
                'http://' + str(current_site.domain) + '/chat/activate/' + jwt_token + '/',
                to=[to_email]
            )
            email.send()
            return render(request, 'chat/mail.html')
    else:
        form = SignupForm()
    return render(request, 'mysite/signup.html', {'form': form})


def activate(request, token):
    decoded_token = jwt.decode(token, 'private_key', algorithms='HS256')
    try:
        user = User.objects.get(username=list(decoded_token.keys())[0])
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('you are not registered yet, please sign up first')
    if user is not None and not user.is_active:
        user.is_active = True
        user.save()
        return render(request, 'chat/confirmmail.html')
    else:
        return render(request, template_name='chat/home.html')


def reset_password(request, token):
    decoded_token = jwt.decode(token, 'private_key', algorithms='HS256')
    try:
        user = User.objects.get(email=list(decoded_token.values())[0])
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        context = {'userReset': user.username}
        print(context)
        return redirect('/resetpassword/' + str(user))
    else:
        return render(request, template_name='chat/home.html')


def new_password(request, userReset):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2 or password2 == "" or password1 == "":
            messages.info(request, "password does not match ")
            return render(request, 'mysite/confirmpassword.html')
        else:
            try:
                user = User.objects.get(username=userReset)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None:
                user.set_password(password1)
                user.save()
                messages.info(request, "password reset done")
                return render(request, 'mysite/resetdone.html')
    else:
        return render(request, 'mysite/confirmpassword.html')
