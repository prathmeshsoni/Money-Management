from .models import *
from .forms import *


def get_all_objs(request):
    user = request.session.get('private_admin')
    if not user:
        return {}
    user_obj = User.objects.get(username=user)

    d = ManageForm()
    type_obj = TypeModel.objects.all()
    cat_obj = CategoryModel.objects.filter(user=user_obj)
    account_obj = AccountModel.objects.filter(user=user_obj)

    item = {
        'm': d,
        'type_obj': type_obj,
        'cat_obj': cat_obj,
        'account_obj': account_obj,
    }

    return item
