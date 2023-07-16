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
                        // $('#dd').text('Can\'t Delete This (' + data.name + ') ❌');
                        // $("#alerttopright_").fadeToggle(350);
                        // $("#alerttopright_").css('display', 'block');
                        // $("#alerttopright").css('display', 'none');
                        // $("#alerttopright_1").css('display', 'none');
                        // $.toast({
                        //     heading: 'Welcome to my Fab Admin',
                        //     text: 'Use the predefined ones, or specify a custom position object.',
                        //     position: 'top-right',
                        //     loaderBg: '#ff6849',
                        //     icon: 'success',
                        //     hideAfter: 3500,
                        //     stack: 6
                        // });
                         $.toast({
                            heading: 'Failed !!!',
                            text: 'Can\'t Delete This (' + data.name + ') !!!',
                            position: 'top-right',
                            loaderBg: '#fc4b6c !important',
                            icon: 'error',
                            hideAfter: 5500

                        });

                    }
                    else if (data.exists === "done") {
                        $('#filter_' + id + '').remove();
                        $.toast({
                            heading: 'Success ',
                            text: '(' + data.name + ') Delete Successfully ✔',
                            position: 'top-right',
                            loaderBg: '#fc4b6c !important',
                            icon: 'success',
                            hideAfter: 5500

                        });
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
