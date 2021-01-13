from datetime import datetime

from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from common.views import get_unique_username
from banking_system.settings import LOGIN_REDIRECT_URL, ADMIN_LOGIN_REDIRECT_URL
from customer.models import AccountMaster
from user_master.models import CustomUser


def index(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(LOGIN_REDIRECT_URL)
    else:
        return HttpResponseRedirect(ADMIN_LOGIN_REDIRECT_URL)


class Login(View):
    def get(self, request):
        user = request.user

        # checking if the user is logged in the returning the user to user home
        if user.is_authenticated:
            if user.is_active:
                if not user.is_superuser:
                    return HttpResponseRedirect(LOGIN_REDIRECT_URL)
                else:
                    return HttpResponseRedirect(ADMIN_LOGIN_REDIRECT_URL)

        return render(request, 'user_master/login.html')

    def post(self, request):
        form = request.POST
        print(form)

        account_no = form.get('account_no')
        password = form.get('password')

        check_user = CustomUser.objects.filter(username__iexact=account_no).exists()
        if not check_user:
            user_context = {
                'msg': "Invalid account number",
                "type": 1
            }
            return JsonResponse(user_context)

        user = authenticate(username=account_no, password=password)
        print(user, 'user')

        if user:
            if user.is_authenticated:
                if user.is_active:

                    # logging user in
                    login(request, user)

                    # setting user id into session
                    request.session['user_account_no'] = user.username
                    request.session['user_id'] = user.id

                    user_context = {
                        'msg': "Login Success",
                        "is_success": True
                    }
                    return JsonResponse(user_context)

            user_context = {
                'msg': "This user is not active please contact to service & support",
                "type": 2
            }
            return JsonResponse(user_context)
        else:
            user_context = {
                'msg': "Either username or password in incorrect",
                "type": 3
            }
            return JsonResponse(user_context)


class SignUp(View):
    def get(self, request):
        user = request.user
        # checking if the user is logged in the returning the user to user home
        if user.is_authenticated:
            if user.is_active:
                if not user.is_superuser:
                    return HttpResponseRedirect(LOGIN_REDIRECT_URL)
                else:
                    return HttpResponseRedirect(ADMIN_LOGIN_REDIRECT_URL)

        return render(request, 'user_master/signup.html')

    def post(self, request):
        form = request.POST
        print(form)
        f_name = form.get('firstName')
        l_name = form.get('lastName')
        email = form.get('email')
        password = form.get('password')
        phone_no = form.get('phoneNumber')

        # function to return the unique username for the new user
        username = get_unique_username()
        print(username)
        qs_user = CustomUser.objects.create_user(username=username,
                                                 password=password,
                                                 email=email,
                                                 mobile_no=phone_no,
                                                 first_name=f_name,
                                                 last_name=l_name)

        if qs_user:
            AccountMaster.objects.create(account_no=username,
                                         fullname=f'{f_name} {l_name}',
                                         upd_date=datetime.now(),
                                         account_holder_id=qs_user.pk)

            # logging in the user after successful signup
            login(request, qs_user)
            # setting values to the session
            request.session['user_id'] = qs_user.pk
            request.session['user_email'] = email

            user_context = {
                'id': qs_user.pk,
                'msg': f"Account Created Successfully & your account number is {username}",
                "is_success": True,
            }
            return JsonResponse(user_context)
        else:
            user_context = {
                'id': 0,
                'msg': "Something went wrong",
                "is_success": False
            }
            return JsonResponse(user_context)

