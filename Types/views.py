from django.shortcuts import render,redirect
from .forms import TypeForm
from .models import TypeModel
from management.models import ManageModel
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import TypeSerialize
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
def cat_page(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            jj = TypeModel.objects.get(id=id)
            d = TypeForm(request.POST or None,request.FILES or None,instance=jj)
            check = 1
        except:
            d = TypeForm(request.POST or None,request.FILES or None)
            check = 0
        if d.is_valid():
            unique_field_value = d.cleaned_data['type_name'].lower()
            existing_records = TypeModel.objects.filter(type_name__iexact=unique_field_value)

            if check == 1:
                if existing_records.exists() and int(id) != int(existing_records[0].id):
                    messages.error(request, 'Type Already Exists. ❌')
                    return redirect('/type/')
                else:
                    d.save()
                    messages.warning(request, 'Data Updated Successfully ✔')
                    return redirect('/type/')
            else:
                if existing_records.exists():
                    messages.error(request, 'Type Already Exists. ❌')
                    return redirect('/type/')
                else:
                    d.save()
                    messages.success(request, 'Data Saved Successfully ✔')
                    return redirect('/type/')

        else:
            messages.error(request, "Type Already Exists. ❌")
            return redirect('/type/')
    else:
        d = TypeForm()
        b = TypeModel.objects.all()
        x = {
            'm': d,
            'list': b,
            'cat_master': 'master',
            'cat_active': 'type_master',
            'category': 'Type',
            'type_nam': 'type_name',
            'type_nam_field': 'm.instance.type_name|as_crispy_field'

        }
        return render(request, "admin/filter.html", x)


@api_view(['POST'])
def updateCat(request):
    id = request.POST.get('id')
    get_data = TypeModel.objects.get(id = id)
    serializer = TypeSerialize(get_data)
    return Response(serializer.data)


def remove_cat(request):
    if request.method == 'POST':
        try:
            hid = request.POST.get('id')
            obj = TypeModel.objects.get(id = hid)
            name = obj.type_name
            aa = ManageModel.objects.filter(type = hid)
            aa_count = aa.count()
            if int(aa_count) == 0:
                confirm_delete = request.POST.get('confirm_delete')
                if int(confirm_delete) == 0:
                    obj.delete()
                    a = {'status': True,'exists':'done', 'name': name}
                    return JsonResponse(a)
                # messages.success(request,"Delete successfully ✔")
                a = {'status': True,'exists':'confirmdelete', 'name': name}
                return JsonResponse(a)
                # return redirect('/user/address/')
            else:
                a = {'status': True,'exists':'orderexist', 'name': name}
                return JsonResponse(a)
        except:
            a = {'status': True,'exists':'error'}
            return JsonResponse(a)
    else:
        return redirect('/type/')
