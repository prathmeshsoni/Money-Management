import json
from twilio.rest import Client
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.backends import UserModel
from .models import ManageModel
from .forms import ManageForm
from category.models import CategoryModel
from account.models import AccountModel
from Types.models import TypeModel
from .serializer import ManageSerialize
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.http import JsonResponse
import time


# 404 Page Not Found
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def viewes(request):
    if request.method == 'POST':
        user2 = request.session.get('private_admin')
        user_obj = User.objects.get(username=user2)
        category_name = request.POST.get('category')
        category_list = request.POST.getlist("option_values")
        try:
            category_nam = json.loads(category_list[0])
        except:
            category_nam = None

        cat_list = []
        if category_nam:
            for value in category_nam:
                try:
                    id = value['id']
                except:
                    continue
                cat_name = value['name']
                item = {
                    "name": cat_name,
                    "id": '',
                }
                cat_list.append(item)

        if cat_list:
            for j in cat_list:
                cat_obj = CategoryModel()
                cat_obj.cat_name = j['name']
                cat_obj.user = user_obj
                cat_obj.save()

        try:
            check = CategoryModel.objects.get(id=category_name)
        except:
            check = CategoryModel.objects.get(cat_name=category_name, user=user_obj)
        final_id = check.id
        final_name = check.cat_name

        # a = {'status': True,  'cat_name': {'id': final_id, 'name': final_name}}
        a = {'status': True, 'cat_name': final_name, 'cat_id': final_id}
        return JsonResponse(a)


# Private LogIn Screen
def admin_private(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        userobj = User.objects.filter(username=username).first()
        user_obj = User.objects.filter(email=username).first()
        if userobj:
            pass
        if user_obj:
            userobj = user_obj
        if (userobj) is None:
            messages.success(request, 'Username/Email not found.')
            return redirect(request.META.get('HTTP_REFERER'))

        if not (userobj).is_superuser:
            messages.success(request, "User Can't login")
            return redirect(request.META.get('HTTP_REFERER'))

        if (userobj).is_superuser:
            if userobj.is_staff:
                try:
                    user = UserModel.objects.get(email=username)
                    user11 = authenticate(username=user, password=password)
                    if (user11) is None:
                        messages.success(request, 'Wrong Password.')
                        return redirect('/')

                    # login(request , user11)
                    request.session['private_admin'] = user
                    request.session['private_id'] = user11.id
                    request.session['login_time'] = datetime.now().timestamp()
                    return redirect('/view/')

                except:
                    usee = None

                user1 = authenticate(username=username, password=password)

                if (user1 or usee) is None:
                    messages.success(request, 'Wrong Password.')
                    return redirect('/')

                # login(request , user1)
                request.session['private_admin'] = username
                request.session['private_id'] = user1.id
                request.session['login_time'] = datetime.now().timestamp()
                return redirect('/view/')


    return render(request, 'login.html', {"checkcon": 10, "Title": "Private "})


# Private LogOut
def logout_private_admin(request):
    if 'private_admin' in request.session:
        del request.session['private_admin']
        del request.session['login_time']
        try:
            del request.session['private_id']
        except:
            pass
    # logout(request)
    return redirect('/')


# Logout Every 30 minutes
def some_view(request):
    # Check if session has expired
    login_time = request.session.get('login_time')
    if login_time:
        login_time = datetime.fromtimestamp(login_time)
        if datetime.now() - login_time > timedelta(minutes=30):
            check = 1
        else:
            check = 0
    else:
        check = 1
    return check


# View All Transaction
def admin_private_view(request):
    check = 0
    user2 = request.session.get('private_admin')
    user_obj = User.objects.get(username=user2)
    # check = some_view(request)
    if int(check) == 1:
        return redirect('/logout/')
    else:
        if request.method == 'POST':
            try:
                id = request.POST.get('id')
                jj = ManageModel.objects.get(id=id)
                d = ManageForm(request.POST or None, instance=jj)
                check_1 = 0
            except:
                d = ManageForm(request.POST)
                check_1 = 1
            if d.is_valid():
                type_txt = d.cleaned_data['type']
                date_str = str(d.cleaned_data['date_name'])
                date_text = convert_date(date_str)
                amount_txt = d.cleaned_data['amount']
                note_txt = d.cleaned_data['category']
                from_txt = d.cleaned_data['from_account']
                to_txt = d.cleaned_data['to_account']
                account_txt = d.cleaned_data['account']
                if check_1 == 1:
                    if str(type_txt).lower() == 'income'.lower():
                        account_list = check_avil(user_obj, account_txt)
                        final_amount_1 = int(account_list[0]['amount']) + int(amount_txt)
                        msg = f'\n\nDear UPI User, ur A/c {account_txt} Credited by Rs.{amount_txt} on {date_text} for {note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'
                    elif str(type_txt).lower() == 'expense'.lower():
                        account_list = check_avil(user_obj, account_txt)
                        final_amount_1 = int(account_list[0]['amount']) - int(amount_txt)
                        msg = f'\n\nDear UPI User, ur A/c {account_txt} Debited for Rs.{amount_txt} by {date_text} for {note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'
                    elif str(type_txt).lower() == 'transfer'.lower():
                        account_list = check_avil(user_obj, from_txt)
                        account_list_1 = check_avil(user_obj, to_txt)
                        final_amount_2 = int(account_list[0]['amount']) - int(amount_txt)
                        final_amount_3 = int(account_list_1[0]['amount']) + int(amount_txt)
                        msg = f'\n\nDear UPI User, ur A/c {from_txt} To ur A/c {to_txt} Transfer Rs.{amount_txt} on {date_text} for {note_txt} Updated Bal of {from_txt} Rs:{final_amount_2} - {to_txt} Rs:{final_amount_3}'
                    else:
                        account_list = check_avil(user_obj, account_txt)
                        final_amount_1 = int(account_list[0]['amount']) + int(amount_txt)
                        msg = f'\n\nDear UPI User, ur A/c {account_txt} Credited by Rs.{amount_txt} on {date_text} for {note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'

                    # sent_massage(msg)

                private_data = d.save(commit=False)
                private_data.user = user_obj
                private_data.save()
                p_id = private_data.id
                if account_txt:
                    link = f'account/{account_txt}/'
                else:
                    link = f'account/{from_txt}/'
                a = {'status': True, 'link': link}
                return JsonResponse(a)
            else:
                a = {'status': False}
                return JsonResponse(a)
        else:
            if 'private_admin' in request.session:
                d = ManageForm()
                b = ManageModel.objects.filter(user=user_obj).order_by('-date_name')
                cat_obj = CategoryModel.objects.filter(user=user_obj)
                account_obj = AccountModel.objects.filter(user=user_obj)
                type_obj = TypeModel.objects.all()
                x = {
                    'm': d,
                    'list': b,
                    'cat_obj': cat_obj,
                    'account_obj': account_obj,
                    'type_obj': type_obj,
                    'private_master': 'master',
                    'private_active': 'private_master',
                    "private_1": 0,
                    "checkcon": 10,
                }
            else:
                return redirect('/')
            return render(request, 'private_des.html', x)


def convert_date(date_str):
    from datetime import datetime
    datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S%z")
    date_txt = datetime_obj.strftime("%d %b %Y %I:%M %p")
    return date_txt


def sent_massage(msg):
    account_sid = 'AC3906f0671f92d822f886ebd6fdf66271'
    auth_token = '721b9dc48d0809160c16d438db5f1bf9'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=msg,
        from_='+15734982530',
        to='+919157379996'
    )


def check_balance(request):
    # type_list = TypeModel.objects.all()
    user2 = request.session.get('private_admin')
    user_obj2 = User.objects.get(username=user2)
    account_list = check_avil(user_obj2, '')

    msg = '\n\nAvailable Balance : \n\n'
    for l in account_list:
        msg = msg + l['account_name'] + f' Rs: ' + str(l['amount']) + '\n'
    # sent_massage(msg)
    return redirect('/view/')


def check_avil(user_obj2, a_name):
    if a_name:
        account_list = AccountModel.objects.filter(account_name=a_name, user=user_obj2)
    else:
        account_list = AccountModel.objects.filter(user=user_obj2)
    amount_list = []
    for k in account_list:
        account_ = ManageModel.objects.filter(Q(account=k) | Q(to_account=k) | Q(from_account=k), Q(user=user_obj2))
        total_amount = 0
        for j in account_:
            tye = j.type.type_name
            if str(tye).lower() == 'Expense'.lower():
                total_amount -= int(j.amount)
            elif str(tye).lower() == 'Available'.lower() or str(tye).lower() == 'Income'.lower():
                total_amount += int(j.amount)
            elif str(tye).lower() == 'transfer'.lower():
                print(j.from_account.account_name.lower())
                if j.from_account.account_name.lower() == k.account_name.lower():
                    total_amount -= int(j.amount)
                else:
                    total_amount += int(j.amount)
        amount_list.append({
            'id': k.id,
            'account_name': k.account_name,
            'amount': total_amount,

        })
    return amount_list


# Private Detail Function
@api_view(['POST'])
def updatepra(request):
    id = request.POST.get('id')
    get_data = ManageModel.objects.get(id=id)
    serializer = ManageSerialize(get_data)
    return Response(serializer.data)


# Delete Detail Fun
def remove_pri(request, hid):
    if 'private_admin' in request.session:
        user2 = request.session.get('private_admin')
        obj = ManageModel.objects.get(id=hid)
        if obj.user.username == user2:
            obj.delete()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/')


def view_type(request, hid):
    if 'private_admin' in request.session:
        d = ManageForm()
        user2 = request.session.get('private_admin')
        user_obj2 = User.objects.get(username=user2)
        try:
            type_ = TypeModel.objects.get(type_name__iexact=hid)
        except:
            return redirect('/view/type/')
        b = ManageModel.objects.filter(type=type_.id, user=user_obj2).order_by('-date_name')
        cat_obj = CategoryModel.objects.filter(user=user_obj2)
        account_obj = AccountModel.objects.filter(user=user_obj2)
        type_obj = TypeModel.objects.all()

        x = {
            'm': d,
            'list': b,
            'filter_master': 'master',
            'filter_active': 'type_master',
            'cat_obj': cat_obj,
            'account_obj': account_obj,
            'type_obj': type_obj,
            "private_1": 0,
            "checkcon": 0,
            "reletedtype": type_.id,
            "main": hid
        }
    else:
        return redirect('/')
    return render(request, 'private_des.html', x)


def view_account(request, hid):
    if 'private_admin' in request.session:
        d = ManageForm()
        user2 = request.session.get('private_admin')
        user_obj2 = User.objects.get(username=user2)
        try:
            type_ = AccountModel.objects.get(account_name__iexact=hid, user=user_obj2)
        except:
            return redirect('/view/account/')
        b = ManageModel.objects.filter(
            Q(account=type_.id) |
            Q(from_account=type_.id) |
            Q(to_account=type_.id),
            Q(user=user_obj2)
        ).order_by('-date_name')
        cat_obj = CategoryModel.objects.filter(user=user_obj2)
        account_obj = AccountModel.objects.filter(user=user_obj2)
        type_obj = TypeModel.objects.all()
        x = {
            'm': d,
            'list': b,
            'filter_master': 'master',
            'filter_active': 'account_master',
            'cat_obj': cat_obj,
            'account_obj': account_obj,
            'type_obj': type_obj,
            "private_1": 0,
            "checkcon": 10,
            "reletedaccount": type_.id,
            "main": hid
        }
    else:
        return redirect('/')
    return render(request, 'private_des.html', x)


def view_category(request, hid):
    if 'private_admin' in request.session:
        d = ManageForm()
        user2 = request.session.get('private_admin')
        user_obj2 = User.objects.get(username=user2)
        try:
            type_ = CategoryModel.objects.get(cat_name__iexact=hid.lower(), user=user_obj2)
        except:
            return redirect('/view/category/')
        b = ManageModel.objects.filter(category=type_.id, user=user_obj2).order_by('-date_name')
        cat_obj = CategoryModel.objects.filter(user=user_obj2)
        account_obj = AccountModel.objects.filter(user=user_obj2)
        type_obj = TypeModel.objects.all()
        x = {
            'm': d,
            'list': b,
            'filter_master': 'master',
            'filter_active': 'cat_master',
            'cat_obj': cat_obj,
            'account_obj': account_obj,
            'type_obj': type_obj,
            "private_1": 0,
            "checkcon": 0,
            "reletedcat": type_.id,
            "main": hid
        }
    else:
        return redirect('/')
    return render(request, 'private_des.html', x)


def view_all(request, hid):
    if 'private_admin' in request.session:
        d = ManageForm()
        user2 = request.session.get('private_admin')
        user_obj2 = User.objects.get(username=user2)
        if hid.lower() == 'account':
            b = []
            c = AccountModel.objects.filter(user=user_obj2)
            for i in c:
                c = check_avil(user_obj2, i.account_name)
                b.append(c[0])
            private_master = 'account_master'
        elif hid.lower() == 'category':
            b = CategoryModel.objects.filter(user=user_obj2)
            private_master = 'cat_master'
        elif hid.lower() == 'type':
            b = TypeModel.objects.all()
            private_master = 'type_master'
        else:
            b = ''
            private_master = 'all_master'
        print(b)
        if private_master == 'all_master':
            pass
        else:
            if not b:
                b = 1
        print(private_master)
        cat_obj = CategoryModel.objects.filter(user=user_obj2)
        account_obj = AccountModel.objects.filter(user=user_obj2)
        type_obj = TypeModel.objects.all()
        if b == 1:
            b = ''
            x = {
                'm': d,
                'list': b,
                'filter_master': 'master',
                'filter_active': private_master,
                'main': hid,
                'cat_obj': cat_obj,
                'account_obj': account_obj,
                'type_obj': type_obj,
            }
        else:
            if b:
                x = {
                    'm': d,
                    'list': b,
                    'filter_master': 'master',
                    'filter_active': private_master,
                    'main': hid,
                    'cat_obj': cat_obj,
                    'account_obj': account_obj,
                    'type_obj': type_obj,
                }
            else:
                x = {
                    'm': d,
                    'list1': type_obj,
                    'list2': account_obj,
                    'list3': cat_obj,
                    'filter_master': 'master',
                    'filter_active': private_master,
                    'main': 'all',
                    'cat_obj': cat_obj,
                    'account_obj': account_obj,
                    'type_obj': type_obj,
                }
    else:
        return redirect('/')
    return render(request, 'all_data.html', x)


def dd(request):
    return render(request, 'admin/account.html')


def search_page(request):
    item = {
        'search': 'search'
    }
    return render(
        request,
        'search-page.html',
        item
    )
