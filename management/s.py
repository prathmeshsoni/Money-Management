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


# from googleapiclient.http import MediaFileUpload
# import os


# 404 Page Not Found
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def viewes(request):
    if request.method == 'POST':
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
                cat_obj.save()

        try:
            check = CategoryModel.objects.get(id=category_name)
        except:
            check = CategoryModel.objects.get(cat_name=category_name)
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
                    usee = None;

                user1 = authenticate(username=username, password=password)

                if (user1 or usee) is None:
                    messages.success(request, 'Wrong Password.')
                    return redirect('/')

                # login(request , user1)
                request.session['private_admin'] = username
                request.session['private_id'] = user1.id
                request.session['login_time'] = datetime.now().timestamp()
                return redirect('/view/')

    # elif request.method == 'GET':
    return render(request, 'login.html', {"checkcon": 10, "Title": "Private "})

    # elif 'username' in request.session:
    #     return redirect('/user/dashboard/')


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


# View All Details
def admin_private_view(request):
    check = 0
    # check = some_view(request)
    if int(check) == 1:
        return redirect('/logout/')
    else:
        if request.method == 'POST':
            try:
                id = request.POST.get('id')
                jj = ManageModel.objects.get(id=id)
                old_type_txt = jj.type.type_name
                old_amount = jj.amount
                try:

                    old_txt = jj.account.account_name
                except:
                    old_txt = ''
                try:
                    old_from = jj.from_account.account_name
                    old_to = jj.to_account.account_name
                except:
                    old_to = ''
                    old_from = ''
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
                if check_1 == 3:
                    if str(type_txt).lower() == 'transfer'.lower():
                        get_obj = AccountModel.objects.get(account_name=from_txt)
                        final_amount_2 = int(get_obj.amount) - int(amount_txt)
                        get_obj.amount = final_amount_2
                        get_obj.save()

                        get_obj_1 = AccountModel.objects.get(account_name=to_txt)
                        final_amount_3 = int(get_obj_1.amount) + int(amount_txt)
                        get_obj_1.amount = final_amount_3
                        get_obj_1.save()
                    else:
                        get_obj = AccountModel.objects.get(account_name=account_txt)
                        get_amount = int(get_obj.amount)

                    if str(type_txt).lower() == 'income'.lower():
                        final_amount_1 = get_amount + int(amount_txt)
                        get_obj.amount = final_amount_1
                        get_obj.save()
                        msg = f'\n\nDear UPI User, ur A/c {account_txt} Credited by Rs.{amount_txt} on {date_text} for {note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'
                    elif str(type_txt).lower() == 'expense'.lower():
                        final_amount_1 = get_amount - int(amount_txt)
                        get_obj.amount = final_amount_1
                        get_obj.save()
                        msg = f'\n\nDear UPI User, ur A/c {account_txt} Debited for Rs.{amount_txt} by {date_text} for {note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'
                    elif str(type_txt).lower() == 'transfer'.lower():
                        msg = f'\n\nDear UPI User, ur A/c {from_txt} To ur A/c {to_txt} Transfer Rs.{amount_txt} on {date_text} for {note_txt} Updated Bal of {from_txt} Rs:{final_amount_2} - {to_txt} Rs:{final_amount_3}'
                    else:
                        final_amount_1 = get_amount + int(amount_txt)
                        get_obj.amount = final_amount_1
                        get_obj.save()
                        msg = f'\n\nDear UPI User, ur A/c {account_txt} Credited by Rs.{amount_txt} on {date_text} for {note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'

                    sent_massage(msg)

                elif check_1 == 0:
                    if str(old_type_txt).lower() == str(type_txt).lower():
                        if str(type_txt).lower() == 'transfer'.lower():
                            old_from_obj = AccountModel.objects.get(account_name=old_from)
                            old_to_obj = AccountModel.objects.get(account_name=old_to)
                            new_from_obj = AccountModel.objects.get(account_name=from_txt)
                            new_to_obj = AccountModel.objects.get(account_name=to_txt)

                            if str(old_from).lower() == str(from_txt).lower():
                                temp_amount = int(old_amount) - int(amount_txt)
                                f = int(old_from_obj.amount) + temp_amount
                                if f < 0:
                                    a = {'name': 'insufficient'}
                                    return JsonResponse(a)
                                old_from_obj.amount = f
                                old_from_obj.save()
                            else:
                                f = int(old_from_obj.amount) + int(amount_txt)
                                f_1 = int(new_from_obj.amount) - int(amount_txt)
                                print(f)
                                print(f_1)
                                if f_1 < 0:
                                    a = {'name': 'insufficient'}
                                    return JsonResponse(a)
                                old_from_obj.amount = f
                                old_from_obj.save()
                                new_from_obj.amount = f_1
                                new_from_obj.save()

                            if str(old_to).lower() == str(to_txt).lower():
                                temp_amount = int(amount_txt) - int(old_amount)
                                f = int(old_to_obj.amount) + temp_amount
                                if f < 0:
                                    a = {'name': 'insufficient'}
                                    return JsonResponse(a)
                                old_to_obj.amount = f
                                old_to_obj.save()
                            else:
                                f = int(old_to_obj.amount) - int(amount_txt)
                                f_1 = int(new_to_obj.amount) + int(amount_txt)
                                if f < 0:
                                    a = {'name': 'insufficient'}
                                    return JsonResponse(a)
                                old_to_obj.amount = f
                                old_to_obj.save()
                                new_to_obj.amount = f_1
                                new_to_obj.save()
                        else:
                            if str(account_txt).lower() == str(old_txt).lower():
                                if str(old_type_txt).lower() == 'expense'.lower():
                                    temp_amount = int(old_amount) - int(amount_txt)
                                else:
                                    temp_amount = int(amount_txt) - int(old_amount)
                                get_obj = AccountModel.objects.get(account_name=account_txt)
                                f = int(get_obj.amount) + temp_amount
                                if f < 0:
                                    a = {'name': 'insufficient'}
                                    return JsonResponse(a)
                                get_obj.amount = f
                                get_obj.save()
                            else:
                                old_get_obj = AccountModel.objects.get(account_name=old_txt)
                                get_obj = AccountModel.objects.get(account_name=account_txt)

                                if str(old_type_txt).lower() == 'income'.lower():
                                    aa = old_get_obj.amount - int(amount_txt)
                                    bb = get_obj.amount + int(amount_txt)
                                elif str(old_type_txt).lower() == 'expense'.lower():
                                    aa = old_get_obj.amount + int(amount_txt)
                                    bb = get_obj.amount - int(amount_txt)
                                else:
                                    aa = old_get_obj.amount - int(amount_txt)
                                    bb = get_obj.amount + int(amount_txt)
                                if aa < 0 or bb < 0:
                                    a = {'name': 'insufficient'}
                                    return JsonResponse(a)
                                old_get_obj.amount = aa
                                old_get_obj.save()
                                get_obj.amount = bb
                                get_obj.save()
                    else:
                        if str(type_txt).lower() == 'transfer'.lower():
                            pass
                            # old_from_obj = AccountModel.objects.get(account_name=old_from)
                            # old_to_obj = AccountModel.objects.get(account_name=old_to)
                            # new_from_obj = AccountModel.objects.get(account_name=from_txt)
                            # new_to_obj = AccountModel.objects.get(account_name=to_txt)
                            #
                            # if str(old_from).lower() == str(from_txt).lower():
                            #     temp_amount = int(old_amount) - int(amount_txt)
                            #     f = int(old_from_obj.amount) + temp_amount
                            #     if f < 0:
                            #         a = {'name': 'insufficient'}
                            #         return JsonResponse(a)
                            #     old_from_obj.amount = f
                            #     old_from_obj.save()
                            # else:
                            #     f = int(old_from_obj.amount) + int(amount_txt)
                            #     f_1 = int(new_from_obj.amount) - int(amount_txt)
                            #     print(f)
                            #     print(f_1)
                            #     if f_1 < 0:
                            #         a = {'name': 'insufficient'}
                            #         return JsonResponse(a)
                            #     old_from_obj.amount = f
                            #     old_from_obj.save()
                            #     new_from_obj.amount = f_1
                            #     new_from_obj.save()
                            #
                            # if str(old_to).lower() == str(to_txt).lower():
                            #     temp_amount = int(amount_txt) - int(old_amount)
                            #     f = int(old_to_obj.amount) + temp_amount
                            #     if f < 0:
                            #         a = {'name': 'insufficient'}
                            #         return JsonResponse(a)
                            #     old_to_obj.amount = f
                            #     old_to_obj.save()
                            # else:
                            #     f = int(old_to_obj.amount) - int(amount_txt)
                            #     f_1 = int(new_to_obj.amount) + int(amount_txt)
                            #     if f < 0:
                            #         a = {'name': 'insufficient'}
                            #         return JsonResponse(a)
                            #     old_to_obj.amount = f
                            #     old_to_obj.save()
                            #     new_to_obj.amount = f_1
                            #     new_to_obj.save()
                        elif str(old_type_txt).lower() == 'transfer'.lower():
                            pass
                        else:
                            print('ssoni')
                            if str(account_txt).lower() == str(old_txt).lower():
                                get_obj = AccountModel.objects.get(account_name=account_txt)
                                if str(old_type_txt).lower() == 'expense'.lower():
                                    temp_amount = int(old_amount) + int(amount_txt)
                                    f = int(get_obj.amount) + temp_amount
                                else:
                                    if str(old_type_txt).lower() == 'Available'.lower() and \
                                            str(type_txt).lower() == 'income'.lower():
                                        f = int(get_obj.amount)
                                    elif str(old_type_txt).lower() == 'income'.lower() and \
                                            str(type_txt).lower() == 'Available'.lower():
                                        f = int(get_obj.amount)
                                    else:
                                        f = int(get_obj.amount) - int(old_amount) - int(amount_txt)

                                print(f)
                                if f < 0:
                                    a = {'name': 'insufficient'}
                                    return JsonResponse(a)
                                get_obj.amount = f
                                get_obj.save()
                            else:
                                old_get_obj = AccountModel.objects.get(account_name=old_txt)
                                get_obj = AccountModel.objects.get(account_name=account_txt)

                                if str(old_type_txt).lower() == 'income'.lower() and \
                                        str(type_txt).lower() == 'Available'.lower():
                                    aa = old_get_obj.amount - int(amount_txt)
                                    bb = get_obj.amount + int(amount_txt)
                                elif str(old_type_txt).lower() == 'Available'.lower() and \
                                        str(type_txt).lower() == 'income'.lower():
                                    aa = old_get_obj.amount - int(amount_txt)
                                    bb = get_obj.amount + int(amount_txt)
                                elif str(old_type_txt).lower() == 'expense'.lower():
                                    aa = old_get_obj.amount + int(amount_txt)
                                    bb = get_obj.amount + int(amount_txt)
                                else:
                                    aa = old_get_obj.amount - int(amount_txt)
                                    bb = get_obj.amount - int(amount_txt)
                                if aa < 0 or bb < 0:
                                    a = {'name': 'insufficient'}
                                    return JsonResponse(a)
                                old_get_obj.amount = aa
                                old_get_obj.save()
                                get_obj.amount = bb
                                get_obj.save()

                    #     get_amount = int(get_obj.amount)
                    # temp_amount = int(jj.amount) - int(d.cleaned_data['amount'])
                    #
                    # if str(type_txt).lower() == 'income'.lower():
                    #     final_val = ''
                    #     temp_amount = int(jj.amount) - int(d.cleaned_data['amount'])
                    # elif str(type_txt).lower() == 'expense'.lower():
                    #     temp_amount = int(jj.amount) - int(d.cleaned_data['amount'])
                    # elif str(type_txt).lower() == 'transfer'.lower():
                    #     temp_amount = int(jj.amount) - int(d.cleaned_data['amount'])
                    # else:
                    #     temp_amount = int(jj.amount) - int(d.cleaned_data['amount'])


                else:
                    print('helo')
                user_id = request.session.get('private_id')
                user_obj = User.objects.get(id=user_id)
                private_data = d.save(commit=False)
                private_data.user = user_obj
                private_data.save()
                p_id = private_data.id
                a = {'status': True}
                return JsonResponse(a)
            else:
                print(d)
                a = {'status': False}
                return JsonResponse(a)
        else:
            if 'private_admin' in request.session:
                d = ManageForm()
                user2 = request.session.get('private_admin')
                user_obj2 = User.objects.get(username=user2)
                b = ManageModel.objects.filter(user=user_obj2).order_by('-date_name')
                cat_obj = CategoryModel.objects.all()
                account_obj = AccountModel.objects.all()
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
    account_list = AccountModel.objects.all()
    amount_list = []
    user2 = request.session.get('private_admin')
    user_obj2 = User.objects.get(username=user2)
    for k in account_list:
        # print(k.account_name)
        account_ = ManageModel.objects.filter(Q(account=k) | Q(to_account=k) | Q(from_account=k) & Q(user=user_obj2))
        total_amount = 0
        for j in account_:
            if k.account_name == 'Cash':
                print(j.type.type_name)
            tye = j.type.type_name
            if str(tye).lower() == 'Expense'.lower():
                total_amount -= int(j.amount)
            elif str(tye).lower() == 'Available'.lower() or str(tye).lower() == 'Income'.lower():
                total_amount += int(j.amount)
            elif str(tye).lower() == 'transfer'.lower():
                print('helo')
                if j.to_account.account_name.lower() == k.account_name:
                    total_amount -= int(j.amount)
                else:
                    total_amount += int(j.amount)
        amount_list.append(total_amount)
    print(amount_list)
    msg = '\n\nAvailable Balance : \n\n'
    for l in range(len(account_list)):
        msg = msg + account_list[l].account_name + f' Rs: ' + str(amount_list[l]) + '\n'
        # msg = msg + account_list[l].account_name + f' Rs: 100000\n'
    sent_massage(msg)
    return redirect('/view/')


# View All Photo, Add Photo
# def private_view(request, hid):
#     check = some_view(request)
#     if int(check) == 1:
#         # call this fun logout_private_admin()
#         return redirect('/logout/')
#     else:
#         if request.method == 'POST':
#             id = request.POST.get("p_id")
#             myfile = request.FILES.getlist("private_img")
#
#             for f in myfile:
#                 chek = str(f).split('.')[-1]
#                 if (chek == "mp4"):
#                     type = "video"
#                 else:
#                     type = "photo"
#                 pro_obj = Private_SubModel()
#                 pri_id = ManageModel.objects.get(id=id)
#                 pro_obj.private_id = pri_id
#                 pro_obj.private_img = f
#                 pro_obj.type = type
#                 pro_obj.save()
#
#             return redirect(f"/view/{hid}")
#         else:
#             if 'private_admin' in request.session:
#                 user2 = request.session.get('private_admin')
#                 order = ManageModel.objects.get(id=hid)
#                 if order.user.username == user2:
#                     pro_list = Private_SubModel.objects.filter(private_id=hid)
#                     d = ManageForm()
#                     data = {'m': d, 'private_master': 'master', 'private_activee': 'private_masterr', 'lists': pro_list,
#                             'order': order, "private_1": 0, "checkcon": 0}
#                 else:
#                     return redirect('/view/')
#             else:
#                 return redirect('/')
#             return render(request, 'private.html', data)


# Private Detail Function
@api_view(['POST'])
def updatepra(request):
    id = request.POST.get('id')
    get_data = ManageModel.objects.get(id=id)
    serializer = ManageSerialize(get_data)
    return Response(serializer.data)


#
#
# Delete Detail Fun
def remove_pri(request, hid):
    if 'private_admin' in request.session:
        user2 = request.session.get('private_admin')
        obj = ManageModel.objects.get(id=hid)
        if obj.user.username == user2:
            obj.delete()
            return redirect('/view/')
        else:
            return redirect('/view/')
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
        cat_obj = CategoryModel.objects.all()
        account_obj = AccountModel.objects.all()
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
            type_ = AccountModel.objects.get(account_name__iexact=hid)
        except:
            return redirect('/view/account/')
        b = ManageModel.objects.filter(
            Q(account=type_.id) |
            Q(from_account=type_.id) |
            Q(to_account=type_.id) &
            Q(user=user_obj2)
        ).order_by('-date_name')
        cat_obj = CategoryModel.objects.all()
        account_obj = AccountModel.objects.all()
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
            type_ = CategoryModel.objects.get(cat_name__iexact=hid.lower())
        except:
            return redirect('/view/category/')
        b = ManageModel.objects.filter(category=type_.id, user=user_obj2).order_by('-date_name')
        cat_obj = CategoryModel.objects.all()
        account_obj = AccountModel.objects.all()
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
        if hid.lower() == 'account':
            b = AccountModel.objects.all()
            private_master = 'account_master'
        elif hid.lower() == 'category':
            b = CategoryModel.objects.all()
            private_master = 'cat_master'
        elif hid.lower() == 'type':
            b = TypeModel.objects.all()
            private_master = 'type_master'
        else:
            b = ''
            private_master = 'all_master'
        cat_obj = CategoryModel.objects.all()
        account_obj = AccountModel.objects.all()
        type_obj = TypeModel.objects.all()
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
#
#
# # Delete Photo Fun
# def remove_photo(request, hid):
#     if 'private_admin' in request.session:
#         user2 = request.session.get('private_admin')
#         obj = Private_SubModel.objects.get(id=hid)
#         if obj.private_id.user.username == user2:
#             jj = obj.private_id.id
#             obj.delete()
#             return redirect(f'/view/{jj}')
#         else:
#             return redirect('/view/')
#     else:
#         return redirect('/')


#  if check_1 == 1:
#                     lks = []
#                     if str(type_txt).lower() == 'transfer'.lower():
#                         account_txt = d.cleaned_data['from_account']
#                         to_txt = d.cleaned_data['to_account']
#                         lks.append(account_txt)
#                         lks.append(to_txt)
#                     else:
#                         account_txt = d.cleaned_data['account']
#                         lks.append(account_txt)
#                     amount_list = []
#                     user_id = request.session.get('private_id')
#                     user_obj = User.objects.get(id=user_id)
#                     for k in lks:
#                         get_a = ManageModel.objects.filter(
#                             Q(account=k) |
#                             Q(to_account=k) |
#                             Q(from_account=k) &
#                             Q(user=user_obj)
#                         )
#                         total_amount = 0
#                         for j in get_a:
#                             tye = j.type.type_name
#                             if str(tye).lower() == 'Expense'.lower():
#                                 total_amount -= int(j.amount)
#                             elif str(tye).lower() == 'Available'.lower() or str(tye).lower() == 'Income'.lower():
#                                 total_amount += int(j.amount)
#                             elif str(tye).lower() == 'transfer'.lower():
#                                 if j.to_account.account_name.lower() == k:
#                                     total_amount -= int(j.amount)
#                                 else:
#                                     total_amount += int(j.amount)
#                         amount_list.append(total_amount)
#
#                     datetime_string = str(d.cleaned_data['date_name'])
#                     from datetime import datetime
#                     datetime_obj = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S%z")
#                     date_txt = datetime_obj.strftime("%d %b %Y %I:%M %p")
#                     amount_txt = d.cleaned_data['amount']
#                     note_txt = d.cleaned_data['category']
#                     if str(type_txt).lower() == 'income'.lower():
#                         amount_list[0] += int(amount_txt)
#                         msg = f'\n\nDear UPI User, ur A/c {account_txt} Credited by Rs.{amount_txt} on {date_txt} for {note_txt} Avl Bal Rs:{amount_list[0]} -{account_txt} Bank'
#                     elif str(type_txt).lower() == 'expense'.lower():
#                         amount_list[0] -= int(amount_txt)
#                         msg = f'\n\nDear UPI User, ur A/c {account_txt} Debited for Rs.{amount_txt} by {date_txt} for {note_txt} Avl Bal Rs:{amount_list[0]} -{account_txt} Bank'
#                     elif str(type_txt).lower() == 'transfer'.lower():
#                         note_txt = d.cleaned_data['note']
#                         to_account = d.cleaned_data['to_account']
#                         amount_list[0] -= int(amount_txt)
#                         amount_list[1] += int(amount_txt)
#                         msg = f'\n\nDear UPI User, ur A/c {account_txt} To ur A/c {to_account} Transfer Rs.{amount_txt} on {date_txt} for {note_txt} Updated Bal of {account_txt} Rs:{amount_list[0]} - {to_account} Rs:{amount_list[1]}'
#                     else:
#                         msg = ''
