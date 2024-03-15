function openModel() {
    $('[name="id"]').val("");
    $("#Addcategory")[0].reset();
    $("#add_cat").css('display', 'block');
    $("#edit_cat").css('display', 'none');
    handleToAccountChange();
    handleFromAccountChange();
    $('#categoryModal').modal();
}


function gettransaction() {
    $('#login_loader').css('display', 'flex');
    $.ajax({
        url: '/get_data/',
        method: 'POST',
        data: $('#transaction_form').serialize(),
        dataType: 'JSON',
        success: function (data) {
            remove_all()
            var table = $('#myTable_2').DataTable();
            table.clear();
            $('#date-iss').val(data.hid);
            $('#date_value').html('');
            $('#date_value').html(data.date);
            $('#date_value').css('background', 'rgb(0 0 0 / 72%)');
            $('#date_value').css('color', 'beige');
            if (data.status === true) {
                $('#nodatass').css('display', 'none');
                if (data.not_transfer.length > 0) {
                    for (var i = 0; i < data.not_transfer.length; i++) {
                        let date_name = data.not_transfer[i]['date']

                        transfer_table(data.not_transfer[i]['price'], date_name, 0, 2)
                        transfer_table(data.not_transfer[i]['price'], date_name, 0, 0)

                        for (var j = data.not_transfer[i]['data_list'].length - 1; j >= 0; j--) {
                            transfer_table(data.not_transfer[i]['data_list'][j], date_name, 0, 1)
                        }
                    }
                } else {
                    $('#nodatass').css('text-align', 'center')
                    $('#nodatass').css('display', 'block')
                }
                if (data.transfer.length > 0) {
                    $('#nodatass_1').css('display', 'none')
                    for (var i = 0; i < data.transfer.length; i++) {
                        let date_name = data.transfer[i]['date']
                        transfer_table(data.transfer[i]['price'], date_name, 1, 0)

                        for (var j = data.transfer[i]['data_list'].length - 1; j >= 0; j--) {
                            transfer_table(data.transfer[i]['data_list'][j], date_name, 1, 1)
                        }
                    }
                } else {
                    $('#nodatass_1').css('text-align', 'center')
                    $('#nodatass_1').css('display', 'block')
                }


            } else {
                $('#nodatass').css('text-align', 'center')
                $('#nodatass').css('display', 'block')
                $('#nodatass_1').css('text-align', 'center')
                $('#nodatass_1').css('display', 'block')
            }
            table.draw();
            // var dd = document.querySelectorAll('#myTable_2 tbody tr td')
            // for(var k= 1; k < dd.length; k+=3){dd[k].style.color = '#ff0000';}
            // for(var k= 2; k < dd.length; k+=3){dd[k].style.color = '#000fff';}
            $("#balance-1").val(data.price['temp_add']);
            $("#balance-2").val(data.price['temp_sub']);
            $("#balance-3").val(data.price['total_amount']);
            $('#login_loader').css('display', 'none');
        }
    });
}

function transfer_table(dataArray, date_id, id, check) {
    let tableBody;

    // not_transfer_table
    if (id === 0) {
        tableBody = document.querySelector("#myTable tbody");
    }
    // transfer_table
    else {
        tableBody = document.querySelector("#myTable_1 tbody");
    }
    if (check === 1) {
        const formattedDate = formatDate(dataArray.date_name);

        const rowHTML = createTable(dataArray, formattedDate, date_id, id)
        const newRow = document.createElement("tr");
        newRow.id = 'tra_' + dataArray.id;
        newRow.innerHTML = rowHTML[0];

        var rows = tableBody.querySelector('[id="date-' + date_id + '"]')
        tableBody.insertBefore(newRow, rows.nextSibling);
    } else if (check === 0) {
        const newRow_ = document.createElement("tr");
        newRow_.id = 'date-' + date_id;
        newRow_.style.background = '#e4f3ff';
        newRow_.innerHTML = '<td>' + date_id + '</td>' +
            '<td style="color:#000fff ;" >' + dataArray.temp_add + ' <i class="fa fa-rupee"></i></td>' +
            '<td style="color:#ff0000 ;" >' + dataArray.temp_sub + ' <i class="fa fa-rupee"></i></td>' +
            '<td colspan="4" ></td>';
        tableBody.insertBefore(newRow_, tableBody.firstChild);
    } else {
        var table = $('#myTable_2').DataTable();
        var newData = ['<td>' + date_id + '</td>']
        var newData1 = ['<td><span class="income-cell">' + dataArray.temp_add + ' <i class="fa fa-rupee"></i></span></td>']
        var newData2 = ['<td><span class="expense-cell">' + dataArray.temp_sub + ' <i class="fa fa-rupee"></i></span></td>']
        // var newData = [
        //   '<td>New Date 1</td>',
        //   '<td>New Price 1 <i class="fa fa-rupee"></i></td>',
        //   '<td>New Price 2 <i class="fa fa-rupee"></i></td>'
        // ];
        // table.row.add(newData.join(''));
        table.row.add([newData, newData1, newData2]).draw();

        // tableBody = document.querySelector("#myTable_2 tbody");
        // const newRow_ = document.createElement("tr");
        // newRow_.innerHTML = '<td>' + date_id + '</td>' +
        //     '<td style="color: #000fff !important;" >' + dataArray.temp_add + '<i class="fa fa-rupee"></i></td>' +
        //     '<td style="color: #ff0000 !important;" >' + dataArray.temp_sub + '<i class="fa fa-rupee"></i></td>';
        //
        // tableBody.insertBefore(newRow_, tableBody.firstChild);
    }
}

function formatDate11(dateString) {
    const options = {hour: 'numeric', minute: 'numeric', hour12: true};
    const formattedDate = new Date(dateString).toLocaleTimeString('en-US', options);
    return formattedDate;
}

function createTable(i, formattedDate, date_id, id) {
    let color_ = '#000'
    let che = '#a3a6a4';
    var f_date = formatDate(i.date_name.replace('Z', ''))
    var f_date_1 = `${f_date[1]} ${f_date[0]}`;
    if (id === 1) {
        return [('<td><i style="margin-right: 20px;" class="fa fa-info-circle" aria-hidden="true"></i></td>' + '<td>' + f_date[0] + '</td>' + '<td>' + i.from_account.account_name + '</td>' + '<td>' + i.to_account.account_name + '</td>' + '<td style="color: ' + color_ + ' !important;">' + i.amount + ' <i class="fa fa-rupee"></i></td>' + '<td>' + i.note + '</td>' + '<td>' + '    <a href="javascript:void(0)" onclick="updateModel(' + i.id + ',' + 0 + ')" class="bg-info mr-2">' + '        <span class="label label-success">\n' + '            Edit\n' + '    </span>' + '    </a>' + '    <a href="javascript:void(0)" onclick="Delete(' + i.id + ',' + 1 + ', \'' + f_date_1 + '\')" class="bg-info ml-2">' + '        <span class="label label-danger">' + '            Delete' + '        </span>' + '    </a>' + '</td>' + '<td name="' + date_id + '" style="display:none;" >' + date_id + '</td>'), che, color_]
    } else {
        if (i.type.type_name.toLowerCase() === 'available' || i.type.type_name.toLowerCase() === 'income') {
            color_ = '#000fff'
            che = '#cbf8cb';
        } else if (i.type.type_name.toLowerCase() === 'expense') {
            color_ = '#ff0000'
            che = '#f8cbcb';
        }

        return [('<td><i style="margin-right: 20px;" class="fa fa-info-circle" aria-hidden="true"></i></td>' + '<td>' + f_date[0] + '</td>' + '<td>' + i.category.cat_name + '</td>' + '<td>' + i.account.account_name + '</td>' + '<td style="color: ' + color_ + ' !important;">' + i.amount + ' <i class="fa fa-rupee"></i></td>' + '<td>' + i.note + '</td>' + '<td>' + '    <a href="javascript:void(0)" onclick="updateModel(' + i.id + ',' + 0 + ')" class="bg-info mr-2">' + '        <span class="label label-success">\n' + '            Edit\n' + '    </span>' + '    </a>' + '    <a href="javascript:void(0)" onclick="Delete(' + i.id + ',' + 1 + ', \'' + f_date_1 + '\')" class="bg-info ml-2">' + '        <span class="label label-danger">' + '            Delete' + '        </span>' + '    </a>' + '</td>' + '<td name="' + date_id + '" style="display:none;" >' + date_id + '</td>'), che, color_]
    }
}


function buttonclick(datas) {
    let tempurl = window.location.href;
    let demo_url = subStr(tempurl)
    let final_url;
    let final_1;
    if (demo_url) {
        final_url = splitstr(demo_url, 0)
        if (final_url) {
            final_1 = splitstr(demo_url, 1)
            if (final_1 === 'not') {
                return [0, '/view/']
            } else {
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
                        } else {
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
        } else {
            return [0, '/']
        }
    } else {
        return [1, '/view/']
    }
}


function splitstr(str, check_value) {
    const myArray = str.split("/");
    if (check_value === 1) {
        if (myArray.length >= 2) {
            return myArray[check_value].toLowerCase();
        } else {
            return '';
        }
    } else {
        return myArray[check_value].toLowerCase();
    }


}


function updateModel(id, chek_1) {
    $("#Addcategory")[0].reset();
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/updatepra/', method: 'POST', data: {'id': id, csrfmiddlewaretoken: csrf_token}, dataType: 'JSON',

        success: function (data) {
            $('[name="id"]').val(data.id);
            $('#id_typename_id').val(data.type);
            var formattedDate = new Date(data.date_name).toISOString().slice(0, 16);
            $('#id_date_name').val(formattedDate);
            if (data.type === 3) {
                check_condition(1)
            } else {
                check_condition(2)
            }
            $('#id_accountname_id').val(data.account);
            if (data.category) {
                $("#id_catname_id option[name='" + (data.category.cat_name).toLowerCase() + "']").prop("selected", true);
            }
            $('#id_to_account').val(data.to_account);
            $('#id_from_account').val(data.from_account);
            $('#id_amount').val(data.amount);
            $('#id_note').val(data.note);
            $("#add_cat").css('display', 'none');
            $("#edit_cat").css('display', 'block');
            handleToAccountChange();
            handleFromAccountChange();
            if (chek_1 === 0) {
                $('#categoryModal').modal();
            }
        },

        error: function () {
            alert('Something is Wrong');
        }
    });
}


function Delete(id, h_id, s_id) {
    var massage_1 = ''
    var massage_2 = ''
    var massage_3 = ''
    if (s_id === 0) {
        massage_1 = "You will not be able to recover Transaction No. (" + h_id + ")";
        massage_2 = "Your Transaction No. (" + h_id + ") has been deleted.";
        massage_3 = 'Transaction No. (' + h_id + ') Delete Successfully ✔';
    } else {
        massage_1 = "You will not be able to recover Transaction Date of\n (" + s_id + ")";
        massage_2 = "Your Transaction (" + s_id + ") has been deleted.";
        massage_3 = 'Transaction (' + s_id + ') Delete Successfully ✔';
    }
    swal({
        title: "Are you sure?",
        text: massage_1,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "No, cancel pls!",
        closeOnConfirm: false,
        closeOnCancel: false
    }, function (isConfirm) {
        if (isConfirm) {
            swal("Deleted!", massage_2, "success");
            var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            var date_val = $('#date-iss').val();
            $.ajax({
                url: '/remove_transaction/',
                data: {'id': id, csrfmiddlewaretoken: csrf_token, 'date_val': date_val},
                dataType: 'JSON',
                method: 'POST',
                success: function (data) {
                    if (data.status === true) {
                        if (data.exists === "done") {
                            $('#balance-1').val(data.prices['temp_add'])
                            $('#balance-2').val(data.prices['temp_sub'])
                            $('#balance-3').val(data.prices['total_amount'])
                            if (s_id === 0) {
                                get_datas(0);
                            }
                            $('#tra_' + id + '').remove();
                            $.toast({
                                heading: 'Success ',
                                text: massage_3,
                                position: 'top-right',
                                loaderBg: '#fc4b6c !important',
                                icon: 'success',
                                hideAfter: 8000
                            });
                            data_is()
                        }
                    } else {
                    }
                },
                error: function () {
                    window.location.href = "/view/";
                },
            });
        } else {
            swal("Cancelled", "Your Transaction is safe :)", "error");
        }
    });
}


function subStr(str) {
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
    if (typ === 3) {
        $.ajax({
            url: '/view/',
            method: 'POST',
            data: $('#Addcategory').serialize(),
            dataType: 'JSON',
            success: function (data) {
                if (data.status === true) {
                    final_function(value_name, searchValue, data, refresh_check)
                } else {
                    alert('Something is Wrong')
                }
            }
        });
    } else {
        var as = $('#id_catname_id option:selected').attr('name');
        if (as === 'add') {
            $('#final-tra').prop('disabled', false);
            $('#final-tra').css('cursor', 'pointer');

            var addd_vall = $('#newOptionInput').val();
            if (addd_vall) {
                $('#addButton').click();
                openForm_test()
            } else {
                $('#newOptionInput').val('');
                $("#newOptionInput").attr("placeholder", "Enter Category......").css('color', 'red');
                $("#newOptionInput").addClass('warningsd');
                check_val()
                $('#newOptionInput').focus();
            }

        } else {
            var optionValues = [];
            $('#id_catname_id option').each(function () {
                var option = {
                    "name": $(this).val(), "id": $(this).attr('id')
                }
                optionValues.push(option);
            });
            var formData = $('#Addcategory').serializeArray();
            var optionValues_final = JSON.stringify(optionValues)
            formData.push({name: 'option_values', value: optionValues_final});
            $.ajax({
                url: '/viewe/', method: 'POST', data: formData, dataType: 'JSON', success: function (data) {
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
                    } else {
                        alert('Something is Wrong.!')
                    }
                }
            });
        }
    }
}


function final_function(value_name, searchValue, data, refresh_check) {
    if (data.status === true) {
        $('#balance-1').val(data.prices['temp_add'])
        $('#balance-2').val(data.prices['temp_sub'])
        $('#balance-3').val(data.prices['total_amount'])
        let serializedData = form_se("#Addcategory");
        if (value_name) {
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
            } else {
                if (searchValue) {
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
        } else {
            if (refresh_check[0] === 0) {
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
            } else {
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
    } else if (data.name === 'insufficient') {
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
    } else {
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

    if (dataArray.type.toLowerCase() === 'transfer') {
        tableBody = document.querySelector("#myTable_1 tbody");
        demo = 1;

    } else {
        tableBody = document.querySelector("#myTable tbody");
        demo = 2;
    }

    const rowHTML = createTableRow(dataArray, formattedDate, id)
    const newRow = document.createElement("tr");
    newRow.style.background = rowHTML[1];
    newRow.id = 'tra_' + id;
    newRow.innerHTML = rowHTML[0];

    var rows = tableBody.querySelector('[id="date-' + formattedDate[1] + '"]')
    if (rows) {

    } else {
        const newRow_ = document.createElement("tr");
        newRow_.id = 'date-' + formattedDate[1];
        newRow_.style.background = '#e4f3ff';
        newRow_.innerHTML = '<td>' + formattedDate[1] + '</td>' +
            '<td style="color:'+ rowHTML[2] +' ;" >' + dataArray.amount + ' <i class="fa fa-rupee"></i></td>' +
            '<td colspan="5" ></td>';
        tableBody.insertBefore(newRow_, tableBody.firstChild);
        rows = tableBody.querySelector('[id="date-' + formattedDate[1] + '"]')
    }
    tableBody.insertBefore(newRow, rows.nextSibling);
    data_is()
}


function createTableRow(i, formattedDate, id) {
    var searchValue = document.querySelector('input[name="search-param"]');
    var value_name = $('[name="id"]').val();
    formattedDate = formatDate(i.date_name.replace('Z', ''))
    var formattedDate_1 = `${formattedDate[1]} ${formattedDate[0]}`;
    if (searchValue || value_name) {
        if (searchValue) {
            searchValue = searchValue.value;
        }
        try {
            const firstTableRowWithId_ = document.querySelector('#myTable_1 tbody tr#tra_' + id);
            const firstTd_ = firstTableRowWithId_.querySelector('td');
        } catch (error) {
            const firstTableRowWithId_ = document.querySelector('#myTable tbody tr#tra_' + id);
            const firstTd_ = firstTableRowWithId_.querySelector('td');
        }
    }
    $('#tra_' + id + '').remove();
    if (i.type.toLowerCase() === 'transfer') {

        var check_account = $('#check_account').val();
        var color_ = ''
        var che = 0;
        if (searchValue) {
            if (i.from_account.toLowerCase().includes(searchValue)) {
                color_ = '#ff0000'
                che = '#f8cbcb';
            } else if (i.to_account.toLowerCase().includes(searchValue)) {
                color_ = '#000fff'
                che = '#cbf8cb';
            } else {
                color_ = '#000'
                che = '#a3a6a4';
            }
        } else {
            if (i.from_account.toLowerCase() === check_account.toLowerCase()) {
                color_ = '#ff0000'
                che = '#f8cbcb';
            } else if (i.to_account.toLowerCase().includes(searchValue) === check_account.toLowerCase()) {
                color_ = '#000fff'
                che = '#cbf8cb';
            } else {
                color_ = '#000'
                che = '#a3a6a4';
            }
        }

        return [('<td><i style="margin-right: 20px;" class="fa fa-info-circle" aria-hidden="true"></i></td>' + '<td>' + formattedDate[0] + '</td>' + '<td>' + i.from_account + '</td>' + '<td>' + i.to_account + '</td>' + '<td style="color: ' + color_ + ' !important;">' + i.amount + ' <i class="fa fa-rupee"></i></td>' + '<td>' + i.note + '</td>' + '<td>' + '    <a href="javascript:void(0)" onclick="updateModel(' + id + ',' + 0 + ')" class="bg-info mr-2">' + '        <span class="label label-success">\n' + '            Edit\n' + '    </span>' + '    </a>' + '    <a href="javascript:void(0)" onclick="Delete(' + id + ',' + 1 + ', \'' + formattedDate_1 + '\')" class="bg-info ml-2">' + '        <span class="label label-danger">' + '            Delete' + '        </span>' + '    </a>' + '</td>' + '<td name="' + formattedDate[1] + '" style="display:none;" >' + formattedDate[1] + '</td>'), che, color_]
    } else {
        var color_ = ''
        var che = 0;
        if (i.type.toLowerCase() === 'available' || i.type.toLowerCase() === 'income') {
            color_ = '#000fff'
            che = '#cbf8cb';
        } else if (i.type.toLowerCase() === 'expense') {
            color_ = '#ff0000'
            che = '#f8cbcb';
        } else {
            color_ = '#000'
            che = '#a3a6a4';
        }

        return [('<td><i style="margin-right: 20px;" class="fa fa-info-circle" aria-hidden="true"></i></td>' + '<td>' + formattedDate[0] + '</td>' + '<td>' + i.category + '</td>' + '<td>' + i.account + '</td>' + '<td style="color: ' + color_ + ' !important;">' + i.amount + ' <i class="fa fa-rupee"></i></td>' + '<td>' + i.note + '</td>' + '<td>' + '    <a href="javascript:void(0)" onclick="updateModel(' + id + ',' + 0 + ')" class="bg-info mr-2">' + '        <span class="label label-success">\n' + '            Edit\n' + '    </span>' + '    </a>' + '    <a href="javascript:void(0)" onclick="Delete(' + id + ',' + 1 + ', \'' + formattedDate_1 + '\')" class="bg-info ml-2">' + '        <span class="label label-danger">' + '            Delete' + '        </span>' + '    </a>' + '</td>' + '<td name="' + formattedDate[1] + '" style="display:none;" >' + formattedDate[1] + '</td>'), che, color_]
    }
}


function formatDate(inputDate) {
    const date = new Date(inputDate);
    const day = date.getDate().toString().padStart(2, '0')
    const month = date.toLocaleString('default', {month: 'long'});
    const year = date.getFullYear();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const formattedDate = `${hours % 12 === 0 ? 12 : hours % 12}:${minutes.toString().padStart(2, '0')}${ampm}`;
    const formattedDate1 = day + " " + month;
    return [formattedDate, formattedDate1];
}


function check_val() {
    var vals = $('#newOptionInput').val();

    if (vals) {
        $('#deleteButton').css('display', 'initial');
    } else {
        $('#deleteButton').css('display', 'none');
    }

}


function add_category() {
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
        } else {
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
    } else if (id === 2) {
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
    if (ss) {
        var deleteOption = selectBox.querySelector('option[name="' + val + '"]');
        deleteOption.remove();
        $("#id_catname_id option[name='add']").prop("selected", true);
        document.getElementById('newOptionInput').value = '';
        $("#newOptionInput").focus();
    } else {
        $("#newOptionInput").focus();
        $("#newOptionInput").val('');
        check_val()
        $("#newOptionInput").attr("placeholder", "Can Not Delete......");
        $("#newOptionInput").addClass('warningsd');
    }
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
        if (i === 0) {

        } else if ($(existingOptions[i]).attr('name').toLowerCase() === newOptionValue) {

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
    $('#id_from_account option[value="' + a + '"]').prop('disabled', true);
    $('#id_from_account option[value!="' + a + '"]').prop('disabled', false);
};document.getElementById('id_to_account').onchange = handleToAccountChange;


function handleFromAccountChange() {

    var a = $('#id_from_account').val();
    $('#id_to_account option[value="' + a + '"]').prop('disabled', true);
    $('#id_to_account option[value!="' + a + '"]').prop('disabled', false);
}

document.getElementById('id_from_account').onchange = handleFromAccountChange;
