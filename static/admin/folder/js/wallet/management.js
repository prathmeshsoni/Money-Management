function openModel() {
    $('[name="id"]').val("");
    $("#Addcategory")[0].reset();
    $("#add_cat").css('display','block');
    $("#edit_cat").css('display','none');
    handleToAccountChange();
    handleFromAccountChange();
    $('#categoryModal').modal();
}


function buttonclick(datas){
    tempurl = window.location.href;
    demo_url = subStr(tempurl)
    if (demo_url){
        final_url = splitstr(demo_url, 0)
        if(final_url){
            final_1 = splitstr(demo_url, 1)
            if (final_1 === 'not'){
                return [0, '/view/']
            }
            else{
                if (final_url === 'type') {
                    if (final_1 === datas.type.toLowerCase()) {
                        return [1, '/view/type/' + datas.type + '/']
                    } else {
                        return [0, '/view/type/' + datas.type + '/']
                    }

                } else if (final_url === 'account') {
                    if (datas.type.toLowerCase() === 'transfer') {
                        if (final_1 === datas.from_account.toLowerCase()) {
                            return [1, '/view/account/' + datas.from_account + '/']
                        } else if (final_1 === datas.to_account.toLowerCase()) {
                            return [1, '/view/account/' + datas.to_account + '/']
                        } else {
                            return [0, '/view/account/' + datas.to_account + '/']
                        }
                    } else {
                        if (final_1 === datas.account.toLowerCase()) {
                            return [1, '/view/account/' + datas.account + '/']
                        } else {
                            return [0, '/view/account/' + datas.account + '/']
                        }
                    }

                } else if (final_url === 'category') {
                    if (datas.category) {
                        if (datas.type.toLowerCase() === 'transfer') {
                            return [0, '/view/']
                        }
                        else{
                            if (final_1.replace('%20', ' ') === datas.category.toLowerCase()) {
                                return [1, '/view/category/' + datas.category + '/']
                            } else {
                                return [0, '/view/category/' + datas.category + '/']
                            }
                        }
                    } else {
                        return [0, '/view/']
                    }
                } else {
                    return [0, '/view/']
                }
            }
        }
        else{
            return [0, '/']
        }
    }
    else{
        return [1, '/view/']
    }
}


function splitstr(str, check_value){
    const myArray = str.split("/");
    if (check_value === 1) {
        if (myArray.length >= 2) {
            return myArray[check_value].toLowerCase();
        }
        else {
            return '';
        }
    }
    else{
        return myArray[check_value].toLowerCase();
    }


}


function updateModel(id, chek_1) {
    $("#Addcategory")[0].reset();
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
                    $("#id_catname_id option[name='" + (data.category.cat_name).toLowerCase() + "']").prop("selected", true);
                }
                $('#id_to_account').val(data.to_account);
                $('#id_from_account').val(data.from_account);
                $('#id_amount').val(data.amount);
                $('#id_note').val(data.note);
                $("#add_cat").css('display','none');
                $("#edit_cat").css('display','block');
                handleToAccountChange();
                handleFromAccountChange();
                if(chek_1 === 0){
                    $('#categoryModal').modal();
                }
          },

          error: function () {
            alert('Something is Wrong');
          }
    });
}


function Delete(id, h_id, s_id){
    // updateModel(id, 0)
    var serializedData = form_se("#Addcategory");
    swal({
        title: "Are you sure?",
        text: "You will not be able to recover Transaction No. (" + h_id + ")",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "No, cancel pls!",
        closeOnConfirm: false,
        closeOnCancel: false
    }, function(isConfirm){
        if (isConfirm) {
            swal("Deleted!", "Your Transaction No. (" + h_id + ") has been deleted.", "success");
            var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: '/remove_pri/',
                data: {'id': id, csrfmiddlewaretoken: csrf_token },
                dataType: 'JSON',
                method: 'POST',
                success: function (data){
                    if (data.status === true) {
                        if (data.exists === "done") {
                            $('#balance-1').val(data.prices['temp_add'])
                            $('#balance-2').val(data.prices['temp_sub'])
                            $('#balance-3').val(data.prices['total_amount'])
                            if (s_id === 0){
                                get_datas(0);
                            }
                            $('#tra_' + id + '').remove();
                            $.toast({
                                heading: 'Success ',
                                text: 'Transaction No. (' + h_id + ') Delete Successfully ✔',
                                position: 'top-right',
                                loaderBg: '#fc4b6c !important',
                                icon: 'success',
                                hideAfter: 8000
                            });
                            data_is()
                        }
                    }
                    else{
                    }
                },
                error: function (){
                        window.location.href = "/view/";
                    },
            });
        } else {
            swal("Cancelled", "Your Transaction is safe :)", "error");
        }
    });
}


function subStr(str){
    const myArray = str.split("/view/");
    return myArray[1];
}


function openForm_test() {
    var value_name = $('[name="id"]').val();
    $('#final-tra').prop('disabled', true);
    $('#final-tra').css('cursor', 'wait');
    var serializedData = form_se("#Addcategory");
    let refresh_check = buttonclick(serializedData)
    var searchValue = document.querySelector('input[name="search-param"]');
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
                        final_function(value_name, searchValue, data, refresh_check)
                    }
                    else {
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

                        var deleteOption = selectElement.querySelector('option[name="' + data.cat_name.toLowerCase() + '"]');
                        deleteOption.remove();

                        var newOption = document.createElement('option');
                        newOption.value = data.cat_id;
                        newOption.textContent = data.cat_name.toLowerCase();
                        newOption.selected = true;
                        newOption.setAttribute('name', data.cat_name.toLowerCase());

                        const firstOption_1 = selectElement.getElementsByTagName('option')[0];
                        selectElement.insertBefore(newOption, firstOption_1.nextSibling);

                        $.ajax({
                              url: '/view/',
                              method: 'POST',
                              data: $('#Addcategory').serialize(),
                              dataType: 'JSON',
                              success: function (data) {
                                    final_function(value_name, searchValue, data, refresh_check)
                              }
                        })
                    }
                    else {
                          alert('Something is Wrong.!')
                    }
                }
            });
        }
    }
}


function final_function(value_name, searchValue, data, refresh_check){
    if (data.status === true) {
        $('#balance-1').val(data.prices['temp_add'])
        $('#balance-2').val(data.prices['temp_sub'])
        $('#balance-3').val(data.prices['total_amount'])
        let serializedData = form_se("#Addcategory");
        if (value_name){
            if (refresh_check[0] === 0) {
                $.toast({
                    heading: 'Changed',
                    text: 'Data Updated Successfully ✔',
                    position: 'top-right',
                    loaderBg: '#fc4b6c !important',
                    icon: 'success',
                    hideAfter: 2000
                });
                $('#m_close').click()
                setTimeout(() => {
                    window.location.href = refresh_check[1];
                }, 2000);
            }
            else{
                if (searchValue){
                    get_datas(0);
                }
                renderTableRows(serializedData, data.id)
                $('#final-tra').prop('disabled', false);
                $('#final-tra').css('cursor', 'pointer');
                $('#m_close').click()
                $.toast({
                    heading: 'Changed',
                    text: 'Data Updated Successfully ✔',
                    position: 'top-right',
                    loaderBg: '#fc4b6c !important',
                    icon: 'success',
                    hideAfter: 8000
                });
            }
        }
        else {
            if (refresh_check[0] === 0){
                $.toast({
                    heading: 'Added',
                    text: 'Data Saved Successfully ✔',
                    position: 'top-right',
                    loaderBg: '#fc4b6c !important',
                    icon: 'success',
                    hideAfter: 2000
                });
                $('#m_close').click()
                setTimeout(() => {
                    window.location.href = refresh_check[1];
                }, 2000);
            }
            else{
                renderTableRows(serializedData, data.id)
                $('#final-tra').prop('disabled', false);
                $('#final-tra').css('cursor', 'pointer');
                $('#m_close').click()
                $.toast({
                        heading: 'Added',
                        text: 'Data Saved Successfully ✔',
                        position: 'top-right',
                        loaderBg: '#fc4b6c !important',
                        icon: 'success',
                        hideAfter: 8000
                });
            }
        }
    }
    else if(data.name === 'insufficient'){
        $('#final-tra').prop('disabled', false);
        $('#final-tra').css('cursor', 'pointer');
        $('#m_close').click()
        $.toast({
            heading: 'Failed !',
            text: 'Insufficient Balance. ❌',
            position: 'top-right',
            loaderBg: '#fc4b6c !important',
            icon: 'error',
            hideAfter: 8000
        });
    }
    else{
        $('#final-tra').prop('disabled', false);
        $('#final-tra').css('cursor', 'pointer');
    }

}


function form_se(form) {
    var formData = {};
    $(form).find(":input").each(function () {
        var name = $(this).attr("name");
        var value;

        if ($(this).is("select")) {
            var selectedOption = $(this).find("option:selected");
            var optionName = selectedOption.attr("name");
            value = optionName;
        } else {
            value = $(this).val();
        }

        formData[name] = value;
    });
    return formData;
}


function renderTableRows(dataArray, id) {
    const formattedDate = formatDate(dataArray.date_name);
    let tableBody = ''
    var demo = 0;

    if (dataArray.type.toLowerCase() === 'transfer'){
        tableBody = document.querySelector("#myTable_1 tbody");
        demo = 1;

    }
    else{
        tableBody = document.querySelector("#myTable tbody");
        demo = 2;
    }

    const rowHTML = createTableRow(dataArray, formattedDate, id)
    const newRow = document.createElement("tr");
    newRow.style.background = rowHTML[1];
    newRow.id = 'tra_'+ id;
    newRow.innerHTML = rowHTML[0];

    var rows = tableBody.querySelector('[id="date-' + formattedDate[1] + '"]')
    if ( rows ) {

    }
    else{
        const newRow_ = document.createElement("tr");
        newRow_.id = 'date-'+ formattedDate[1];
        newRow_.innerHTML = '<td>' + formattedDate[1] + '</td>';
        tableBody.insertBefore(newRow_, tableBody.firstChild);
        rows = tableBody.querySelector('[id="date-' + formattedDate[1] + '"]')
    }
    tableBody.insertBefore(newRow, rows.nextSibling);
    data_is()
}


function createTableRow(i, formattedDate, id) {
    var searchValue = document.querySelector('input[name="search-param"]');
    var value_name = $('[name="id"]').val();
    if (searchValue || value_name ){
        if(searchValue){
            searchValue = searchValue.value;
        }
        try{
            const firstTableRowWithId_ = document.querySelector('#myTable_1 tbody tr#tra_' + id);
            const firstTd_ = firstTableRowWithId_.querySelector('td');
        }catch (error){
            const firstTableRowWithId_ = document.querySelector('#myTable tbody tr#tra_' + id);
            const firstTd_ = firstTableRowWithId_.querySelector('td');
        }
    }
    $('#tra_' + id + '').remove();
    if (i.type.toLowerCase() === 'transfer'){

        var check_account = $('#check_account').val();
        var color_ = ''
        var che = 0;
        if(searchValue){
            if ( i.from_account.toLowerCase().includes(searchValue) ){
                color_ = '#ff0000'
                che = '#f8cbcb';
            }
            else if ( i.to_account.toLowerCase().includes(searchValue) ){
                color_ = '#000fff'
                che = '#cbf8cb';
            }
            else{
                color_ = '#000'
                che = '#a3a6a4';
            }
        }
        else{
             if ( i.from_account.toLowerCase() === check_account.toLowerCase() ){
                color_ = '#ff0000'
                che = '#f8cbcb';
            }
            else if ( i.to_account.toLowerCase().includes(searchValue) === check_account.toLowerCase() ){
                color_ = '#000fff'
                che = '#cbf8cb';
            }
            else{
                color_ = '#000'
                che = '#a3a6a4';
            }
        }

        return [(
            '<td><i style="margin-right: 20px;" class="fa fa-info-circle" aria-hidden="true"></i></td>' +
            '<td>' + formattedDate[0] + '</td>' +
            '<td>' + i.from_account + '</td>' +
            '<td>' + i.to_account + '</td>' +
            '<td style="color: '+ color_ +' !important;">' + i.amount + ' ₹</td>' +
            '<td>' + i.note + '</td>' +
            '<td>' +
            '    <a href="javascript:void(0)" onclick="updateModel(' + id + ',' + 0 + ')" class="bg-info mr-2">' +
            '        <span class="label label-success">\n' +
            '            Edit\n' +
            '    </span>' +
            '    </a>' +
            '    <a href="javascript:void(0)" onclick="Delete(' + id + ',' + 1 + ')" class="bg-info ml-2">' +
            '        <span class="label label-danger">' +
            '            Delete' +
            '        </span>' +
            '    </a>' +
            '</td>' +
            '<td name="' + formattedDate[1] + '" style="display:none;" >' + formattedDate[1] + '</td>'
        ), che]
    }
    else{
        var color_ = ''
        var che = 0;
        if (i.type.toLowerCase() === 'available' || i.type.toLowerCase() === 'income' ){
            color_ = '#000fff'
            che = '#cbf8cb';
        }
        else if ( i.type.toLowerCase() === 'expense' ){
            color_ = '#ff0000'
            che = '#f8cbcb';
        }
        else{
            color_ = '#000'
            che = '#a3a6a4';
        }

        return [(
            '<td><i style="margin-right: 20px;" class="fa fa-info-circle" aria-hidden="true"></i></td>' +
            '<td>' + formattedDate[0] + '</td>' +
            '<td>' + i.category + '</td>' +
            '<td>' + i.account + '</td>' +
            '<td style="color: '+ color_ +' !important;">' + i.amount + ' ₹</td>' +
            '<td>' + i.note + '</td>' +
            '<td>' +
            '    <a href="javascript:void(0)" onclick="updateModel(' + id + ',' + 0 + ')" class="bg-info mr-2">' +
            '        <span class="label label-success">\n' +
            '            Edit\n' +
            '    </span>' +
            '    </a>' +
            '    <a href="javascript:void(0)" onclick="Delete(' + id + ',' + 1 + ')" class="bg-info ml-2">' +
            '        <span class="label label-danger">' +
            '            Delete' +
            '        </span>' +
            '    </a>' +
            '</td>' +
            '<td name="' + formattedDate[1] + '" style="display:none;" >' + formattedDate[1] + '</td>'
        ), che]
    }
}


function formatDate(inputDate) {
    const date = new Date(inputDate);
    const day = date.getDate().toString().padStart(2, '0');
    const month = date.toLocaleString('default', { month: 'long' });
    const year = date.getFullYear();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const formattedDate = `${hours % 12 === 0 ? 12 : hours % 12}:${minutes.toString().padStart(2, '0')}${ampm}`;
    const formattedDate1 = day + " " + month;
    console.log(formattedDate)
    console.log(formattedDate1)
    return [formattedDate, formattedDate1];
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


function add_button() {
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
}
document.getElementById('deleteButton').onclick = add_button;


function delete_button() {
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
}
document.getElementById('addButton').onclick = delete_button;


function handleToAccountChange() {

    var a = $('#id_to_account').val();
    $('#id_from_account option[value="'+ a +'"]').prop('disabled', true);
    $('#id_from_account option[value!="'+ a +'"]').prop('disabled', false);
};
document.getElementById('id_to_account').onchange = handleToAccountChange;


function handleFromAccountChange() {

    var a = $('#id_from_account').val();
    $('#id_to_account option[value="'+ a +'"]').prop('disabled', true);
    $('#id_to_account option[value!="'+ a +'"]').prop('disabled', false);
}
document.getElementById('id_from_account').onchange = handleFromAccountChange;
