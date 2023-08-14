function openModel() {
    $("#Addcategory")[0].reset();
    $("#add_cat").css('display', 'block');
    $("#edit_cat").css('display', 'none');
    $('#categoryModal').modal();
}


function updateModel(id) {
    const category = $('#cname').val().toLowerCase();
    const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: 'updateCat/',
        method: 'POST',
        data: {'id': id, csrfmiddlewaretoken: csrf_token},
        dataType: 'JSON',

        success: function (data) {
            $('[name="id"]').val(data.id);
            if (category === 'category') {
                $('#id_cat_name').val(data.cat_name);
            } else if (category === 'type') {
                $('#id_type_name').val(data.type_name);
            } else {
                $('#id_account_name').val(data.account_name);
            }
            $("#add_cat").css('display', 'none');
            $("#edit_cat").css('display', 'block');
            $('#categoryModal').modal();

        },

        error: function () {
            alert('Something is Wrong');
        }
    });
}


function Delete(id) {
    const confirm_delete = $('#confirm_delete').val();
    const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    const category = $('#cname').val().toLowerCase();
    $.ajax({
        url: 'remove_cat/',
        data: {'id': id, 'confirm_delete': confirm_delete, csrfmiddlewaretoken: csrf_token},
        dataType: 'JSON',
        method: 'POST',
        success: function (data) {
            if (data.status === true) {
                if (data.exists === "error") {
                    window.location.href = "/" + category + "/";
                } else if (data.exists === "orderexist") {
                    $.toast({
                        heading: 'Failed !!!',
                        text: 'Can\'t Delete This (' + data.name + ') !!!',
                        position: 'top-right',
                        loaderBg: '#fc4b6c !important',
                        icon: 'error',
                        hideAfter: 8000

                    });

                } else if (data.exists === "done") {
                    $('#filter_' + id + '').remove();
                    $.toast({
                        heading: 'Success',
                        text: '(' + data.name + ') Delete Successfully ✔',
                        position: 'top-right',
                        loaderBg: '#fc4b6c !important',
                        icon: 'success',
                        hideAfter: 8000

                    });
                    $('#confirm_delete').val(1);

                } else if (data.exists === "confirmdelete") {
                    swal({
                        title: "Are you sure?",
                        text: "You want to delete (" + data.name + ") ?",
                        type: "warning",
                        showCancelButton: true,
                        confirmButtonColor: "#DD6B55",
                        confirmButtonText: "Yes, delete it!",
                        cancelButtonText: "No, cancel pls!",
                        closeOnConfirm: false,
                        closeOnCancel: false
                    }, function (isConfirm) {
                        if (isConfirm) {
                            swal("Deleted!", "Your Data (" + data.name + ") has been deleted.", "success");
                            $('#confirm_delete').val('0');
                            Delete(id);
                        } else {
                            swal("Cancelled", "Your Data is safe :)", "error");
                        }
                    });
                }
            } else {
            }
        },
        error: function () {
            window.location.href = "/" + category + "/";
        },
    });

}
