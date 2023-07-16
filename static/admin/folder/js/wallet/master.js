function openModel() {
    $("#Addcategory")[0].reset();
    $("#add_cat").css('display','block');
    $("#edit_cat").css('display','none');
    $('#categoryModal').modal();
}


function updateModel(id) {
    var category = $('#cname').val().toLowerCase();
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
          url: 'updateCat/',
          method: 'POST',
          data: { 'id': id, csrfmiddlewaretoken: csrf_token },
          dataType: 'JSON',

          success: function (data) {
                $('[name="id"]').val(data.id);
                if (category === 'category') {
                    $('#id_cat_name').val(data.cat_name);
                } else if (category === 'type'){
                    $('#id_type_name').val(data.type_name);
                } else{
                    $('#id_account_name').val(data.account_name);
                }
                $("#add_cat").css('display','none');
                $("#edit_cat").css('display','block');
                $('#categoryModal').modal();

          },

          error: function () {
                alert('Something is Wrong');
          }
    });
}


function Delete(id){
      var confirm_delete = $('#confirm_delete').val();
      var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
      var category = $('#cname').val().toLowerCase();
      $.ajax({
            url: 'remove_cat/',
            data: {'id': id, 'confirm_delete' : confirm_delete ,csrfmiddlewaretoken: csrf_token },
            dataType: 'JSON',
            method: 'POST',
            success: function (data){
                if (data.status === true) {
                    if (data.exists === "error") {
                        window.location.href = "/" + category + "/";
                    }
                    else if (data.exists === "orderexist") {
                        $('#dd').text('Can\'t Delete This (' + data.name + ') ❌');
                        $('#dd_2').css('display', 'none');
                        $('#dd_1').css('display', 'none');
                        $('#dd').css('display', 'block');

                    }
                    else if (data.exists === "done") {
                        $('#filter_' + id + '').remove();
                        $('#dd_1').text('(' + data.name + ') Delete Successfully ✔')
                        $('#dd_2').css('display', 'none');
                        $('#dd').css('display', 'none');
                        $('#dd_1').css('display', 'block');
                        $('#confirm_delete').val(1);

                    }
                    else if (data.exists === "confirmdelete") {
                        let confirmAction = confirm("You want to delete (" + data.name + ") ?");
                        if (confirmAction){
                            $('#confirm_delete').val('0');
                            Delete(id);
                        }
                        else{

                        }
                    }
                }
                else{
                }
            },
            error: function ()
            {
                window.location.href = "/" + category +"/";
            },
      });

}
