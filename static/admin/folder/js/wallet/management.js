function openModel() {
    $('[name="id"]').val("");
    $("#Addcategory")[0].reset();
    $("#add_cat").css('display','block');
    $("#edit_cat").css('display','none');
    handleToAccountChange();
    handleFromAccountChange();
    $('#categoryModal').modal();
}

function updateModel(id) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
          url: '/updatepra/',
          method: 'POST',
          data: { 'id': id, csrfmiddlewaretoken: csrf_token },
          dataType: 'JSON',

          success: function (data) {
                $('[name="id"]').val(data.id);
                $('#id_typename_id').val(data.type);
                var formattedDate = new Date(data.date_name).toISOString().slice(0, 16);
                $('#id_date_name').val(formattedDate);
                if (data.type===3){
                    check_condition(1)
                }
                else{
                    check_condition(2)
                }
                $('#id_accountname_id').val(data.account);
                if ( data.category ){
                    $("#id_catname_id option[name='" + data.category.cat_name + "']").prop("selected", true);
                }
                $('#id_to_account').val(data.to_account);
                $('#id_from_account').val(data.from_account);
                $('#id_amount').val(data.amount);
                $('#id_note').val(data.note);
                $("#add_cat").css('display','none');
                $("#edit_cat").css('display','block');
                handleToAccountChange();
                handleFromAccountChange();
                $('#categoryModal').modal();
          },

          error: function () {
            alert('Something is Wrong');
          }
    });
}

function Delete(id){
    let confirmAction = confirm("You want to delete Private Item?")
    if (confirmAction){
        window.location.href = "/remove_pri/" + id + "";
    }
    else{

    }
}


function subStr(str)
{
    const myArray = str.split("/view/");
    return myArray[1];
}


function openForm_test() {
    $('#final-tra').prop('disabled', true);
    $('#final-tra').css('cursor', 'wait');
    urrll = window.location.href
    uurl = subStr(urrll)
    var typ = parseInt($('#id_typename_id').val(), 10);
    if (typ === 3){
        $.ajax({
              url: '/view/',
              method: 'POST',
              data: $('#Addcategory').serialize(),
              dataType: 'JSON',
              success: function (data) {

                    if (data.status === true) {
                        if (uurl === ''){
                            window.location.href = "/view/";
                        }
                        else{
                            window.location.href = "/view/" + data.link;
                        }
                    } else {
                        alert('Something is Wrong')
                    }
              }
        });
    }
    else {
        var as = $('#id_catname_id option:selected').attr('name');
        if (as === 'add') {
            $('#final-tra').prop('disabled', false);
            $('#final-tra').css('cursor', 'pointer');

            var addd_vall = $('#newOptionInput').val();
            if (addd_vall){
               $('#addButton').click();
               openForm_test()
            }
            else {
                $('#newOptionInput').val('');
                $("#newOptionInput").attr("placeholder", "Enter Category......").css('color', 'red');
                $("#newOptionInput").addClass('warningsd');
                check_val()
                $('#newOptionInput').focus();
            }

        }
        else {
            var optionValues = [];
            $('#id_catname_id option').each(function() {
                var option = {
                    "name": $(this).val(),
                    "id": $(this).attr('id')
                }
                optionValues.push(option);
            });
            var formData = $('#Addcategory').serializeArray();
            var optionValues_final = JSON.stringify(optionValues)
            formData.push({ name: 'option_values', value: optionValues_final });
            $.ajax({
                url: '/viewe/',
                method: 'POST',
                data: formData,
                dataType: 'JSON',
                success: function (data) {

                    if (data.status === true) {
                        var selectElement = document.getElementById('id_catname_id');
                        var deleteOption = selectElement.querySelector('option[name="' + data.cat_name + '"]');
                        deleteOption.remove();
                        var newOption = document.createElement('option');
                        newOption.value = data.cat_id;
                        newOption.textContent = data.cat_name;
                        newOption.selected = true;
                        selectElement.appendChild(newOption);
                        $.ajax({
                              url: '/view/',
                              method: 'POST',
                              data: $('#Addcategory').serialize(),
                              dataType: 'JSON',
                              success: function (data) {
                                    if (data.status === true) {
                                        if (uurl === ''){
                                            window.location.href = "/view/";
                                        }
                                        else{
                                            window.location.href = "/view/" + data.link;
                                        }
                                    } else if(data.name === 'insufficient'){
                                        $('#dd').text('Insufficient Balance. ❌');
                                        $('#dd_2').css('display', 'none');
                                        $('#dd_1').css('display', 'none');
                                        $('#dd').css('display', 'block');
                                        $('#m_close').click()
                                    }
                                    else{
                                        $('#final-tra').prop('disabled', false);
                                    }
                              }
                        })
                    } else {
                          alert('Something is Wrong.!')
                    }
                }
            });
        }
    }
}

function check_val(){
    var vals = $('#newOptionInput').val();

    if (vals){
        $('#deleteButton').css('display', 'initial');
    }
    else {
        $('#deleteButton').css('display', 'none');
    }

}

function add_category(){
    var a = $('#id_catname_id option:selected').attr('name');
    var selectBox = document.getElementById("id_catname_id");
    var selectedOption = selectBox.options[selectBox.selectedIndex];
    var selectedId = selectedOption.id;
    if (a === 'add' || selectedId === 'newOptionValue') {
        $('#add-cat').css('display', 'block');
        $('#add-cat-1').css('display', 'block');
        if (selectedId === 'newOptionValue') {
            $('#newOptionInput').val(a);
            check_val()
        }
        else {
            $('#newOptionInput').val('');
            check_val()
        }
    } else {
        $('#add-cat').css('display', 'none');
        $('#add-cat-1').css('display', 'none');

    }

}


function check_condition(id) {
    if (id === 0) {
        var a = parseInt($('#id_typename_id').val(), 10);
    } else if(id === 2){
        var a = 1;
    } else {
        var a = 3;
    }
    if (a === 3) {
            $('#div_id_from_account').css('display', 'block');
            $('#div_id_to_account').css('display', 'block');
            $('#id_to_account').prop("required", true);
            $('#id_from_account').prop("required", true);

            $('#div_id_catname_id').css('display', 'none');
            $('#div_id_accountname_id').css('display', 'none');
            $('#id_accountname_id').prop("required", false);
            $('#id_catname_id').prop("required", false);

    } else {
        $('#div_id_from_account').css('display', 'none');
        $('#div_id_to_account').css('display', 'none');
        $('#id_to_account').prop("required", false);
        $('#id_from_account').prop("required", false);

        $('#div_id_catname_id').css('display', 'block');
        $('#div_id_accountname_id').css('display', 'block');
        $('#id_accountname_id').prop("required", true);
        $('#id_catname_id').prop("required", true);

    }

}


document.getElementById('deleteButton').addEventListener('click', function() {
    var val = $('#newOptionInput').val();
    var selectBox = document.getElementById('id_catname_id');
    var existingOptions = selectBox.getElementsByTagName('option');
    var op = selectBox.options[selectBox.selectedIndex];
    var ss = op.id;
    if (ss){
        var deleteOption = selectBox.querySelector('option[name="' + val + '"]');
        deleteOption.remove();
        $("#id_catname_id option[name='add']").prop("selected", true);
        document.getElementById('newOptionInput').value = '';
        $("#newOptionInput").focus();
    }
    else {
        $("#newOptionInput").focus();
        $("#newOptionInput").val('');
        check_val()
        $("#newOptionInput").attr("placeholder", "Can Not Delete......");
        $("#newOptionInput").addClass('warningsd');
    }

    // var selectContainer = document.getElementById('selectContainer');
    //
    // var newOptionValue = document.getElementById('newOptionInput').value.toLowerCase();
    //
    // if (newOptionValue.trim() === '') {
    //     alert('Please enter a value for the option.');
    //     return;
    // }
    //
    // var newOption = document.createElement('option');
    // newOption.value = newOptionValue;
    // newOption.textContent = newOptionValue;
    // newOption.id = 'newOptionValue';
    // newOption.selected = true; // Automatically select the new option
    //
    // selectBox.appendChild(newOption);
    //
    // document.getElementById('newOptionInput').value = ''; // Clear the input field after adding option
});


document.getElementById('addButton').addEventListener('click', function() {
    var selectContainer = document.getElementById('selectContainer');
    var selectBox = document.getElementById('id_catname_id');
    var newOptionValue = document.getElementById('newOptionInput').value.toLowerCase();

    if (newOptionValue.trim() === '') {
        alert('Please enter a value for the option.');
        return;
    }

    var existingOptions = $('#id_catname_id option');


    for (var i = 0; i < existingOptions.length; i++) {
        if (i===0){

        }
        else if ($(existingOptions[i]).attr('name').toLowerCase() === newOptionValue) {

            $(existingOptions[i]).prop('selected', true);
            document.getElementById('newOptionInput').value = '';
            check_val()
            return;
        }
    }

    var newOption = document.createElement('option');
    newOption.value = newOptionValue;
    newOption.textContent = newOptionValue;
    newOption.id = 'newOptionValue';
    newOption.setAttribute('name', newOptionValue);
    newOption.selected = true; // Automatically select the new option

    selectBox.appendChild(newOption);

    // document.getElementById('newOptionInput').value = ''; // Clear the input field after adding option
});



// document.getElementById('id_to_account').onchange =
function handleToAccountChange() {

    var a = $('#id_to_account').val();
    $('#id_from_account option[value="'+ a +'"]').prop('disabled', true);
    $('#id_from_account option[value!="'+ a +'"]').prop('disabled', false);
};


// document.getElementById('id_from_account').onchange =
function handleFromAccountChange() {

    var a = $('#id_from_account').val();
    $('#id_to_account option[value="'+ a +'"]').prop('disabled', true);
    $('#id_to_account option[value!="'+ a +'"]').prop('disabled', false);
}
document.getElementById('id_to_account').onchange = handleToAccountChange;

// Set the onchange event for 'id_from_account'
document.getElementById('id_from_account').onchange = handleFromAccountChange;
