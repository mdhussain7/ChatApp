# from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
# from django.views.decorators.csrf import csrf_exempt
# from .forms import SignupForm
from rest_framework_swagger.views import get_swagger_view
# from rest_framework import viewsets
# from .serializers import Userlogin
# import jwt

# Create your views here.
User = get_user_model()

schema_view = get_swagger_view(title='My FunDoo Application ')


def home(request):
    return render(request, 'fun/home.html')


from .serializers import LoginDataSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Login
from rest_framework import status, generics


class ContactData(generics.GenericAPIView):
    serializer_class = LoginDataSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        login = Login.objects.all()
        serializer = LoginDataSerializer(login, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LoginDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class LoginAuthentication(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = Userlogin
#
#     @csrf_exempt
#     def log_in(request):
#         if request.method == 'POST':
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(username=username, password=password)
#             try:
#                 if user is not None:
#                     login(request, user)
#                     return redirect(reverse('fun:home'))
#             except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#                 return render(request, 'mysite/login.html')
#         return render(request, 'mysite/login.html')
#
#     def reset_link(request):
#         if request.method == 'POST':
#             to_email = request.POST['email']
#             current_site = get_current_site(request)
#             mail_subject = 'Reset your password.'
#             jwt_token = jwt.encode({'Email': to_email}, 'key', algorithm='HS256').decode("utf-8")
#             email = EmailMessage(
#                 mail_subject,
#                 'http://' + str(current_site.domain) + '/fun/resetpassword/' + jwt_token + '/',
#                 to=[to_email]
#             )
#             email.send()
#             return render(request, 'mysite/checkmail.html')
#         else:
#             form = PasswordResetForm()
#         return render(request, "mysite/resetpassword.html", {"form": form})
#
#     @login_required(login_url='/login/')
#     def log_out(request):
#         logout(request)
#         return redirect(reverse('mysite:log_in'))
#
#     @csrf_exempt
#     def sign_up(request):
#         if request.method == 'POST':
#             mail_subject = 'Activate your account.'
#             jwt_token = jwt.encode(mail_subject, 'key', algorithm='HS256').decode("utf-8")
#             return render(request, 'fun/mail.html')
#         return render(request, 'mysite/signup.html', {'form': form})
#
#     def activate(request, token):
#         decoded_token = jwt.decode(token, 'key', algorithms='HS256')
#         try:
#             user = User.objects.get(username=list(decoded_token.keys())[0])
#         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return HttpResponse('you are not registered yet, please sign up first')
#         if user is not None and not user.is_active:
#             user.is_active = True
#             user.save()
#             return render(request, 'fun/confirmmail.html')
#         else:
#             return render(request, template_name='fun/home.html')
#
#     def reset_password(request, token):
#         decoded_token = jwt.decode(token, 'key', algorithms='HS256')
#         try:
#             user = User.objects.get(email=list(decoded_token.values())[0])
#         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#         if user is not None:
#             context = {'userReset': user.username}
#             print(context)
#             return redirect('/resetpassword/' + str(user))
#         else:
#             return render(request, template_name='fun/home.html')
#
#     def new_password(request, userReset):
#         if request.method == 'POST':
#             password1 = request.POST['password1']
#             password2 = request.POST['password2']
#             if password1 != password2 or password2 == "" or password1 == "":
#                 messages.info(request, "password does not match ")
#                 return render(request, 'mysite/confirmpassword.html')
#             else:
#                 try:
#                     user = User.objects.get(username=userReset)
#                 except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#                     user = None
#                 if user is not None:
#                     user.set_password(password1)
#                     user.save()
#                     messages.info(request, "password reset done")
#                     return render(request, 'mysite/resetdone.html')
#         else:
#             return render(request, 'mysite/confirmpassword.html')

