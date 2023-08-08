import json
# from twilio.rest import Client
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
from .serializer import ManageSerialize, ManageSerialize_1
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.views import PasswordChangeForm


# 404 Page Not Found
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('private_admin'):
            return view_func(request, *args, **kwargs)
        else:
            messages.success(request, 'First You Need to Login')
            return redirect('/')

    return wrapper


def custom_login_required_not(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('private_admin'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/view/')

    return wrapper


@custom_login_required
def custom_change_password(request):
    user_obj = get_user_obj(request)
    if request.method == 'POST':
        form = PasswordChangeForm(user=user_obj, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Changed Successfully ✔')
            # Redirect to the desired URL after successful password change
            return redirect('/change-password/')  # Replace with your desired URL
    else:
        form = PasswordChangeForm(user=request.user)
    d, cat_obj, account_obj, type_obj = get_forms(user_obj)
    return render(request, 'admin/change-password-1.html', {
        'search': 'search',
        'form': form,
        'm': d,
        'cat_obj': cat_obj,
        'account_obj': account_obj,
        'type_obj': type_obj,
        'password_master': 'master',
        'password_active': 'password_master',
    })


def get_user_obj(request):
    user = request.session.get('private_admin')
    user_obj = User.objects.get(username=user)
    return user_obj


def get_forms(user_obj):
    d = ManageForm()
    cat_obj = CategoryModel.objects.filter(user=user_obj)
    account_obj = AccountModel.objects.filter(user=user_obj)
    type_obj = TypeModel.objects.all()
    return d, cat_obj, account_obj, type_obj


def get_date_data(b):
    categorized_data = {}
    for entry in b:
        date = entry.date_name.strftime("%d %B")  # Format the date as 'dd-mm-yyyy'
        if date in categorized_data:
            if entry.type.type_name == 'Transfer':
                categorized_data[date].append(entry)
        else:
            if entry.type.type_name == 'Transfer':
                categorized_data[date] = [entry]
    categorized_data_1 = {}
    for entry in b:
        date = entry.date_name.strftime("%d %B")  # Format the date as 'dd-mm-yyyy'
        if date in categorized_data_1:
            if entry.type.type_name == 'Transfer':
                pass
            else:
                categorized_data_1[date].append(entry)
        else:
            if entry.type.type_name == 'Transfer':
                pass
            else:
                categorized_data_1[date] = [entry]

    categorized_data = dict(sorted(categorized_data.items(), key=lambda item: item[0]))
    categorized_data_1 = dict(sorted(categorized_data_1.items(), key=lambda item: item[0]))
    return categorized_data, categorized_data_1


# Private Login
@custom_login_required_not
def admin_private(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj2 = User.objects.filter(Q(username=username) | Q(email=username)).first()
        user_obj = User.objects.filter(email=username).first()
        if user_obj2:
            pass
        if user_obj:
            user_obj2 = user_obj
        if user_obj2 is None:
            messages.success(request, 'Username/Email not found.')
            return redirect(request.META.get('HTTP_REFERER'))

        if not user_obj2.is_superuser:
            messages.success(request, "User Can't login")
            return redirect(request.META.get('HTTP_REFERER'))

        if user_obj2.is_superuser and user_obj2.is_staff:
            user = UserModel.objects.get(Q(username=username) | Q(email=username))
            user11 = authenticate(username=user, password=password)
            if user11 is None:
                messages.success(request, 'Wrong Password.')
                return redirect('/')

            request.session['private_admin'] = user.username
            request.session['private_id'] = user11.id
            request.session['login_time'] = datetime.now().timestamp()
            return redirect('/view/')

    else:
        if 'private_admin' in request.session:
            return redirect('/view/')
    return render(request, 'login.html', {"checkcon": 10, "Title": "Private "})


# Private Logout
def logout_private_admin(request):
    if 'private_admin' in request.session:
        del request.session['private_admin']
    if 'login_time' in request.session:
        del request.session['login_time']
    if 'private_id' in request.session:
        del request.session['private_id']
    # logout(request)
    return redirect('/')


# View All Transaction
@custom_login_required
def admin_private_view(request):
    import datetime
    user_obj = get_user_obj(request)
    if request.method == 'POST':
        dat_ = request.POST.get('date-iss')
        try:
            id_1 = request.POST.get('id')
            jj = ManageModel.objects.get(id=id_1)
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
                    account_list = account_value(user_obj, account_txt)
                    final_amount_1 = int(account_list[0]['amount']) + int(amount_txt)
                    msg = f'\n\nDear UPI User, ur A/c {account_txt} Credited by Rs.{amount_txt} on {date_text} for ' \
                          f'{note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'
                elif str(type_txt).lower() == 'expense'.lower():
                    account_list = account_value(user_obj, account_txt)
                    final_amount_1 = int(account_list[0]['amount']) - int(amount_txt)
                    msg = f'\n\nDear UPI User, ur A/c {account_txt} Debited for Rs.{amount_txt} by {date_text} for ' \
                          f'{note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'
                elif str(type_txt).lower() == 'transfer'.lower():
                    account_list = account_value(user_obj, from_txt)
                    account_list_1 = account_value(user_obj, to_txt)
                    final_amount_2 = int(account_list[0]['amount']) - int(amount_txt)
                    final_amount_3 = int(account_list_1[0]['amount']) + int(amount_txt)
                    msg = f'\n\nDear UPI User, ur A/c {from_txt} To ur A/c {to_txt} Transfer Rs.{amount_txt} on ' \
                          f'{date_text} for {note_txt} Updated Bal of {from_txt} Rs:{final_amount_2} - {to_txt} ' \
                          f'Rs:{final_amount_3}'
                else:
                    account_list = account_value(user_obj, account_txt)
                    final_amount_1 = int(account_list[0]['amount']) + int(amount_txt)
                    msg = f'\n\nDear UPI User, ur A/c {account_txt} Credited by Rs.{amount_txt} on {date_text} for ' \
                          f'{note_txt} Avl Bal Rs:{final_amount_1} -{account_txt} Bank'

                # sent_massage(msg)

            private_data = d.save(commit=False)
            private_data.user = user_obj
            private_data.save()
            link_check = request.META.get('HTTP_REFERER').split('/view/')
            if len(link_check) >= 2:
                items = calculate_amount(user_obj, link_check[1], dat_)
            else:
                items = []
            p_id = private_data.id
            if account_txt:
                link = f'account/{account_txt}/'
            else:
                link = f'account/{from_txt}/'
            if check_1 == 0:
                link = '/' + "/".join("".join(request.META.get('HTTP_REFERER')).split('/')[3:])
            else:
                pass
            a = {'status': True, 'id': p_id, 'link': link, 'prices': items}
            return JsonResponse(a)
        else:
            a = {'status': False}
            return JsonResponse(a)
    else:
        parsed_date = datetime.datetime.now()
        month_ = parsed_date.month
        year_ = parsed_date.year
        b = ManageModel.objects.filter(user=user_obj, date_name__month=month_, date_name__year=year_).order_by('-date_name')
        d, cat_obj, account_obj, type_obj = get_forms(user_obj)
        categorized_data, categorized_data_1 = get_date_data(b)
        items = {
            'm': d,
            'list': b,
            'cat_obj': cat_obj,
            'account_obj': account_obj,
            'type_obj': type_obj,
            'private_master': 'master',
            'private_active': 'private_master',
            "private_1": 0,
            "checkcon": 10,
            'untransfer_data': categorized_data_1,
            'transfer_data': categorized_data,
            'month': parsed_date
        }

        return render(request, 'private_des.html', items)


@custom_login_required
def get_date_transaction(request):
    if request.method == 'POST':
        hid = request.POST.get('transaction-month')
        date_ = "".join(hid).split('-')
        parsed_date = datetime.strptime(hid, "%Y-%m").strftime('%B %Y')
        month_ = date_[1]
        year_ = date_[0]
        user_obj = get_user_obj(request)
        obj_manage = ManageModel.objects.filter(user=user_obj, date_name__month=month_, date_name__year=year_).order_by('-date_name')
        categorized_data, categorized_data_1 = get_date_data(obj_manage)
        items = calculate_amount(user_obj, '', hid)
        try:
            final_list_not_transfer = get_serialize_list(categorized_data_1)
        except:
            final_list_not_transfer = []
        try:
            final_list_transfer = get_serialize_list(categorized_data)
        except:
            final_list_transfer = []
        if final_list_transfer or final_list_not_transfer:
            a = {
                'status': True,
                'transfer': final_list_transfer,
                'not_transfer': final_list_not_transfer,
                'price': items,
                'date': parsed_date,
                'hid': hid
            }
        else:
            a = {
                'status': False,
                'date': parsed_date,
                'hid': hid,
                'price': items,
            }
        return JsonResponse(a, safe=False)
    else:
        return redirect('/view/')


def get_serialize_list(data_list):
    final_list = []
    for k in data_list:
        temp_list = []
        if data_list[f'{k}']:
            for i in data_list[f'{k}']:
                m_id = i.id
                get_data = ManageModel.objects.get(id=m_id)
                serializer = ManageSerialize_1(get_data)
                temp_list.append(serializer.data)

            a = {
                'date': k,
                'data_list': temp_list
            }
            final_list.append(a)
    return final_list


# Search Page
@custom_login_required
def search_page(request):
    user_obj = get_user_obj(request)
    if request.method == 'POST':
        search_param = "".join(request.POST.get('search-param')).strip().lower()
        filter_name = request.POST.get('filter')
        if filter_name == 'type':
            obj_manage = ManageModel.objects.filter(
                Q(type__type_name__icontains=search_param),
                user=user_obj
            ).order_by('date_name')
        elif filter_name == 'account':
            obj_manage = ManageModel.objects.filter(
                Q(account__account_name__icontains=search_param) |
                Q(from_account__account_name__icontains=search_param) |
                Q(to_account__account_name__icontains=search_param),
                user=user_obj
            ).order_by('date_name')
        elif filter_name == 'category':
            obj_manage = ManageModel.objects.filter(
                Q(category__cat_name__icontains=search_param),
                user=user_obj
            ).order_by('date_name')
        else:
            obj_manage = ManageModel.objects.filter(
                Q(type__type_name__icontains=search_param) |
                Q(account__account_name__icontains=search_param) |
                Q(from_account__account_name__icontains=search_param) |
                Q(to_account__account_name__icontains=search_param) |
                Q(category__cat_name__icontains=search_param) |
                Q(amount__icontains=search_param) |
                Q(note__icontains=search_param),
                user=user_obj
            ).order_by('date_name')
        temp_list = []
        total_amount = 0
        temp_add = 0
        temp_sub = 0
        if obj_manage:
            for i in obj_manage:
                m_id = i.id
                get_data = ManageModel.objects.get(id=m_id)
                serializer = ManageSerialize_1(get_data)
                temp_list.append(serializer.data)

                tye = i.type.type_name
                if str(tye).lower() == 'Expense'.lower():
                    total_amount -= int(i.amount)
                    temp_sub += int(i.amount)
                elif str(tye).lower() == 'Available'.lower() or str(tye).lower() == 'Income'.lower():
                    total_amount += int(i.amount)
                    temp_add += int(i.amount)
                if str(tye).lower() == 'transfer'.lower():
                    if search_param in i.from_account.account_name.lower():
                        total_amount -= int(i.amount)
                        temp_sub += int(i.amount)
                    elif search_param in i.to_account.account_name.lower():
                        total_amount += int(i.amount)
                        temp_add += int(i.amount)
            a = {
                'status': True,
                'data_list': temp_list,
                'params': "".join(search_param).strip().lower(),
                'total_amount': total_amount,
                'temp_add': temp_add,
                'temp_sub': temp_sub,
                'filter_name': filter_name
            }
            return JsonResponse(a, safe=False)
            # a = {'status': True}
            # return JsonResponse(a, safe=False)
        else:
            a = {'status': False}
            return JsonResponse(a, safe=False)
    else:
        d, cat_obj, account_obj, type_obj = get_forms(user_obj)
        item = {
            'search': 'search',
            'search_master': 'master',
            'search_active': 'search_master',
            'cat_obj': cat_obj,
            'account_obj': account_obj,
            'type_obj': type_obj,
            'm': d,
        }
        return render(
            request,
            'search-page.html',
            item
        )


@custom_login_required
def chart_page(request, hid):
    # import datetime
    date_ = "".join(hid).split('-')
    parsed_date = datetime.strptime(hid, "%Y-%m")
    month_ = date_[1]
    year_ = date_[0]

    user_obj = get_user_obj(request)
    d, cat_obj, account_obj, type_obj = get_forms(user_obj)
    total_ = 0
    total_1 = 0
    total_income = []
    total_expense = []
    cat_list = []
    cat_list_ = []
    for i in cat_obj:
        ll = "".join(i.cat_name).strip()

        cat = CategoryModel.objects.get(id=i.id)
        val = ManageModel.objects.filter(user=user_obj, category=cat, date_name__month=month_, date_name__year=year_)
        temp_income = 0
        temp_expense = 0
        for k in val:
            types = k.type.type_name
            if str(types).lower() == 'Available'.lower() or str(types).lower() == 'Income'.lower():
                temp_income += k.amount
            elif str(types).lower() == 'Expense'.lower():
                temp_expense += k.amount
        total_ += temp_income
        total_1 += temp_expense
        if temp_income == 0:
            pass
        else:
            cat_list_.append(f'{ll}')
            total_income.append(str(temp_income))
            
        if temp_expense == 0:
            pass
        else:
            cat_list.append(f'{ll}')
            total_expense.append(str(temp_expense))

    item = {
        'names_': cat_list,
        'total_income': ", ".join(total_income),
        'income': total_,
        'names': cat_list_,
        'total_expense': ", ".join(total_expense),
        'expense': total_1,
        'search': 'search',
        'chart_master': 'master',
        'chart_active': 'chart_master',
        'cat_obj': cat_obj,
        'account_obj': account_obj,
        'type_obj': type_obj,
        'm': d,
        'month': parsed_date
    }
    return render(
        request,
        'chart-page.html',
        item
    )


@custom_login_required
def chart_page_1(request):
    import datetime
    datee = datetime.datetime.now().strftime("%Y-%m")
    return redirect(f'/chart/{datee}/')
    # e = chart_page(request, datetime.datetime.now().strftime("%Y-%m"))
    # print(e)


@custom_login_required
def category_add(request):
    user_obj = get_user_obj(request)
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
                    id_1 = value['id']
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

        a = {'status': True, 'cat_name': final_name, 'cat_id': final_id}
        return JsonResponse(a)
    else:
        return redirect('/view/')


@custom_login_required
def view_all(request, other):
    user_obj = get_user_obj(request)
    if other.lower() == 'account':
        b = []
        c = AccountModel.objects.filter(user=user_obj)
        for i in c:
            c = account_value(user_obj, i.account_name)
            b.append(c[0])
        private_master = 'account_master'
    elif other.lower() == 'category':
        b = CategoryModel.objects.filter(user=user_obj)
        private_master = 'cat_master'
    elif other.lower() == 'type':
        b = TypeModel.objects.all()
        private_master = 'type_master'
    else:
        b = ''
        private_master = 'all_master'
    if private_master == 'all_master':
        other = 'all'
        pass
    else:
        if not b:
            b = 1
    d, cat_obj, account_obj, type_obj = get_forms(user_obj)
    x = {
        'm': d,
        'filter_master': 'master',
        'filter_active': private_master,
        'main': other,
        'cat_obj': cat_obj,
        'account_obj': account_obj,
        'type_obj': type_obj,
    }
    if b == 1:
        b = ''
        x['list'] = b
    else:
        if b:
            x['list'] = b
        else:
            x['list1'] = type_obj
            x['list2'] = account_obj
            x['list3'] = cat_obj
    return render(request, 'all_data.html', x)


@custom_login_required
def check_balance(request):
    user_obj = get_user_obj(request)
    account_list = account_value(user_obj, '')

    msg = '\n\nAvailable Balance : \n\n'
    for item in account_list:
        msg = msg + item['account_name'] + f' Rs: ' + str(item['amount']) + '\n'

    # sent_massage(msg)
    return redirect('/view/')


# Private Detail Function
@custom_login_required
@api_view(['GET', 'POST'])
def get_value(request):
    if request.method == 'GET':
        return redirect('/view/')
    else:
        id_1 = request.POST.get('id')
        get_data = ManageModel.objects.get(id=id_1)
        serializer = ManageSerialize(get_data)
        return Response(serializer.data)


# Delete Detail Function
@custom_login_required
def remove_pri(request):
    if request.method == 'POST':
        try:
            dat_ = request.POST.get('date_val')
            user_obj = get_user_obj(request)
            hid = request.POST.get('id')
            obj = ManageModel.objects.get(id=hid)
            obj.delete()
            link_check = request.META.get('HTTP_REFERER').split('/view/')
            if len(link_check) >= 2:
                items = calculate_amount(user_obj, link_check[1], dat_)
            else:
                items = []
            a = {'status': True, 'exists': 'done', 'prices': items}
            return JsonResponse(a)
        except:
            a = {'status': True, 'exists': 'error'}
            return JsonResponse(a)
    else:
        return redirect('/view/')


@custom_login_required
def view_type(request, hid):
    user_obj = get_user_obj(request)
    try:
        type_ = TypeModel.objects.get(type_name__iexact=hid)
    except:
        return redirect('/view/type')
    b = ManageModel.objects.filter(type=type_.id, user=user_obj).order_by('-date_name')
    d, cat_obj, account_obj, type_obj = get_forms(user_obj)
    categorized_data, categorized_data_1 = get_date_data(b)

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
        "main": hid,
        'untransfer_data': categorized_data_1,
        'transfer_data': categorized_data,
    }
    return render(request, 'private_des.html', x)


@custom_login_required
def view_account(request, hid):
    user_obj = get_user_obj(request)
    try:
        type_ = AccountModel.objects.get(account_name__iexact=hid, user=user_obj)
    except:
        return redirect('/view/account')
    b = ManageModel.objects.filter(
        Q(account=type_.id) |
        Q(from_account=type_.id) |
        Q(to_account=type_.id),
        Q(user=user_obj)
    ).order_by('-date_name')
    d, cat_obj, account_obj, type_obj = get_forms(user_obj)
    categorized_data, categorized_data_1 = get_date_data(b)

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
        "main": hid,
        'untransfer_data': categorized_data_1,
        'transfer_data': categorized_data,
    }
    return render(request, 'private_des.html', x)


@custom_login_required
def view_category(request, hid):
    user_obj = get_user_obj(request)
    try:
        type_ = CategoryModel.objects.get(cat_name__iexact=hid.lower(), user=user_obj)
    except:
        return redirect('/view/category')
    b = ManageModel.objects.filter(category=type_.id, user=user_obj).order_by('-date_name')
    d, cat_obj, account_obj, type_obj = get_forms(user_obj)
    categorized_data, categorized_data_1 = get_date_data(b)

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
        "main": hid,
        'untransfer_data': categorized_data_1,
        'transfer_data': categorized_data,
    }
    return render(request, 'private_des.html', x)


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


def convert_date(date_str):
    from datetime import datetime
    datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S%z")
    date_txt = datetime_obj.strftime("%d %b %Y %I:%M %p")
    return date_txt


def sent_massage(msg):
    pass
    # account_sid = 'AC3906f0671f92d822f886ebd6fdf66271'
    # auth_token = '721b9dc48d0809160c16d438db5f1bf9'
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body=msg,
    #     from_='+15734982530',
    #     to='+919157379996'
    # )


def account_value(user_obj, a_name):
    if a_name:
        account_list = AccountModel.objects.filter(account_name=a_name, user=user_obj)
    else:
        account_list = AccountModel.objects.filter(user=user_obj)
    amount_list = []
    for k in account_list:
        account_ = ManageModel.objects.filter(
            Q(account=k) |
            Q(to_account=k) |
            Q(from_account=k),
            Q(user=user_obj)
        )
        total_amount = 0
        temp_add = 0
        temp_sub = 0
        for j in account_:
            tye = j.type.type_name
            if str(tye).lower() == 'Expense'.lower():
                total_amount -= int(j.amount)
                temp_sub += int(j.amount)
            elif str(tye).lower() == 'Available'.lower() or str(tye).lower() == 'Income'.lower():
                total_amount += int(j.amount)
                temp_add += int(j.amount)
            elif str(tye).lower() == 'transfer'.lower():
                if j.from_account.account_name.lower() == k.account_name.lower():
                    total_amount -= int(j.amount)
                    temp_sub += int(j.amount)
                else:
                    total_amount += int(j.amount)
                    temp_add += int(j.amount)

        items = {
            'id': k.id,
            'account_name': k.account_name,
            'amount': total_amount,
            'temp_add': temp_add,
            'temp_sub': temp_sub,
        }
        amount_list.append(items)
    return amount_list


def dd(request):
    return render(request, 'admin/account.html')


def calculate_amount(user_obj, url_list, dates):
    if dates:
        date_ = "".join(dates).split('-')
        month_ = date_[1]
        year_ = date_[0]
    else:
        pass
    total_amount = 0
    temp_add = 0
    temp_sub = 0
    if url_list:
        check = 1
        temp = url_list.split('/')
        name = temp[0]
        value = temp[1]
        if name.lower() == 'type':
            obj_list = ManageModel.objects.filter(
                Q(type__type_name__iexact=value.lower()),
                user=user_obj
            )
        elif name.lower() == 'account':
            obj_list = ManageModel.objects.filter(
                Q(account__account_name__iexact=value.lower()) |
                Q(from_account__account_name__icontains=value.lower()) |
                Q(to_account__account_name__icontains=value.lower()),
                user=user_obj
            )
        else:
            obj_list = ManageModel.objects.filter(
                Q(category__cat_name__iexact=value.lower()),
                user=user_obj
            )
    else:
        try:
            obj_list = ManageModel.objects.filter(
                user=user_obj,
                date_name__month=month_,
                date_name__year=year_
            )
        except:
            obj_list = ManageModel.objects.filter(
                user=user_obj,
            )
        check = 0
    for j in obj_list:
        tye = j.type.type_name
        if str(tye).lower() == 'Expense'.lower():
            total_amount -= int(j.amount)
            temp_sub += int(j.amount)
        elif str(tye).lower() == 'Available'.lower() or str(tye).lower() == 'Income'.lower():
            total_amount += int(j.amount)
            temp_add += int(j.amount)
        if check == 1:
            if str(tye).lower() == 'transfer'.lower():
                if j.from_account.account_name.lower() == value.lower():
                    total_amount -= int(j.amount)
                    temp_sub += int(j.amount)
                else:
                    total_amount += int(j.amount)
                    temp_add += int(j.amount)

    item_1 = {
        'total_amount': total_amount,
        'temp_add': temp_add,
        'temp_sub': temp_sub,
    }
    return item_1
