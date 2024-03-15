from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from management.models import ManageModel
from management.views import custom_login_required, get_user_obj
from .forms import CategoryForm
from .models import CategoryModel
from .serializer import CategorySerialize


@custom_login_required
def cat_page(request):
    user_obj = get_user_obj(request)
    if request.method == 'POST':
        try:
            id_1 = request.POST.get('id')
            jj = CategoryModel.objects.get(id=id_1)
            d = CategoryForm(request.POST or None, request.FILES or None, instance=jj)
            check = 1
        except:
            d = CategoryForm(request.POST or None, request.FILES or None)
            check = 0
        if d.is_valid():
            unique_field_value = d.cleaned_data['cat_name'].lower()
            existing_records = CategoryModel.objects.filter(cat_name__iexact=unique_field_value, user=user_obj)
            if check == 1:
                if existing_records.exists() and int(id_1) != int(existing_records[0].id):
                    messages.error(request, 'Category Already Exists. ❌')
                    return redirect('/category/')
                else:
                    d.save()
                    messages.warning(request, 'Data Updated Successfully ✔')
                    return redirect('/category/')
            else:
                if existing_records.exists():
                    messages.error(request, 'Category Already Exists. ❌')
                    return redirect('/category/')
                else:
                    private_data = d.save(commit=False)
                    private_data.user = user_obj
                    private_data.save()
                    messages.success(request, 'Data Saved Successfully ✔')
                    return redirect('/category/')

        else:
            messages.error(request, "Category Already Exists. ❌")
            return redirect('/category/')

    else:
        d = CategoryForm()
        b = CategoryModel.objects.filter(user=user_obj)
        x = {
            'm': d,
            'list': b,
            'cat_master': 'master',
            'cat_active': 'cat_master',
            'category': 'Category',
            'type_nam': 'cat_name'
        }
        return render(request, "cate_wise.html", x)


@api_view(['POST'])
def updateCat(request):
    id_1 = request.POST.get('id')
    get_data = CategoryModel.objects.get(id=id_1)
    serializer = CategorySerialize(get_data)
    return Response(serializer.data)


@custom_login_required
def remove_cat(request):
    if request.method == 'POST':
        try:
            hid = request.POST.get('id')
            obj = CategoryModel.objects.get(id=hid)
            name = obj.cat_name
            aa = ManageModel.objects.filter(category=hid)
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
        return redirect('/category/')
