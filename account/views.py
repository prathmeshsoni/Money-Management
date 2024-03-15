from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from management.models import ManageModel
from management.views import account_value, custom_login_required, get_user_obj
from .forms import AccountForm
from .models import AccountModel
from .serializer import AccountSerialize


@custom_login_required
def acc_page(request):
    user_obj = get_user_obj(request)
    if request.method == 'POST':
        try:
            id_1 = request.POST.get('id')
            jj = AccountModel.objects.get(id=id_1)
            d = AccountForm(request.POST or None, request.FILES or None, instance=jj)
            check = 1
        except:
            d = AccountForm(request.POST or None, request.FILES or None)
            check = 0
        if d.is_valid():
            unique_field_value = d.cleaned_data['account_name'].lower()
            existing_records = AccountModel.objects.filter(account_name__iexact=unique_field_value, user=user_obj)

            if check == 1:
                if existing_records.exists() and int(id_1) != int(existing_records[0].id):
                    messages.error(request, 'Account Already Exists. ❌')
                    return redirect('/account/')
                else:
                    d.save()
                    messages.warning(request, 'Data Updated Successfully ✔')
                    return redirect('/account/')
            else:
                if existing_records.exists():
                    messages.error(request, 'Account Already Exists. ❌')
                    return redirect('/account/')
                else:

                    private_data = d.save(commit=False)
                    private_data.user = user_obj
                    private_data.save()
                    messages.success(request, 'Data Saved Successfully ✔')
                    return redirect('/account/')
        else:
            messages.error(request, "Account Already Exists.")
            return redirect('/account/')
    else:
        d = AccountForm()
        b = AccountModel.objects.filter(user=user_obj)
        data_list = []
        for i in b:
            c = account_value(user_obj, i.account_name)
            data_list.append(c[0])
        x = {
            'm': d,
            'list': data_list,
            'cat_master': 'master',
            'cat_active': 'account_master',
            'category': 'Account',
            'type_nam': 'account_name'
        }
        return render(request, "cate_wise.html", x)


@api_view(['POST'])
def updateacc(request):
    id_1 = request.POST.get('id')
    get_data = AccountModel.objects.get(id=id_1)
    serializer = AccountSerialize(get_data)
    return Response(serializer.data)


@custom_login_required
def remove_acc(request):
    if request.method == 'POST':
        try:
            hid = request.POST.get('id')
            obj = AccountModel.objects.get(id=hid)
            name = obj.account_name
            aa = ManageModel.objects.filter(account=hid)
            aa_count = aa.count()
            if int(aa_count) == 0:
                confirm_delete = request.POST.get('confirm_delete')
                if int(confirm_delete) == 0:
                    obj.delete()
                    a = {'status': True, 'exists': 'done', 'name': name}
                    return JsonResponse(a)
                a = {'status': True, 'exists': 'confirmdelete', 'name': name}
                return JsonResponse(a)
            else:
                a = {'status': True, 'exists': 'orderexist', 'name': name}
                return JsonResponse(a)
        except:
            a = {'status': True, 'exists': 'error'}
            return JsonResponse(a)
    else:
        return redirect('/account/')
