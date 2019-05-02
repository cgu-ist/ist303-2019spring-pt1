$.ajax({
    url:  '/customer/list',
    type:  'get',
    dataType:  'json',
    success: function  (data) {
        if (data.ret == 0) {
            let rows =  '';
            data.customers.forEach(customer => {
                rows += `<tr id="tr_${customer.id}">
                        <td class="col-2">${customer.first_name} ${customer.last_name}</td>
                        <td class="col-3">${customer.gender}</td>
                        <td class="col-1">${customer.email}</td>
                        <td class="col-2">${customer.tel}</td>
                        <td class="col-4">
                            <button class="btn deleteBtn btn-primary" data-id="${customer.id}">Delete</button>
                            <button class="btn updateBtn btn-primary" data-id="${customer.id}">Update</button>
                            <button class="btn checkInBtn btn-primary" data-id="${customer.id}">Check-In</button>
                        </td>
                    </tr>`;
            });

            $('#myTable tbody').append(rows);
            bindBtn();
        } else {
            // do something
        }
    }
});

function bindBtn() {
    $('.deleteBtn').each((i, elm) => {
        $(elm).on("click",  (e) => {
            deleteCustomer($(elm))
        })
    })
    $('.updateBtn').each((i, elm) => {
        $(elm).on("click",  (e) => {
            updateCustomer($(elm))
        })
    })
    $('.checkInBtn').each((i, elm) => {
        $(elm).on("click",  (e) => {
            checkInCustomer($(elm))
        })
    })
}

function deleteCustomer(el){
    let customerId  =  $(el).data('id')
    $.ajax({
        url:  `/customer/${customerId}`,
        type:  'delete',
        dataType:  'json',
        success:  function (data) {
            $(el).parents()[1].remove()
        }
    });
}

function checkInCustomer(el){
    let customerId  =  $(el).data('id')
    $.ajax({
        url:  `/customer/checkin/${customerId}`,
        type:  'post',
        dataType:  'json',
        success:  function (data) {
            console.log("Checked In")
        }
    });
}

function newCustomer(){
    let form = `<br><br>
           <div>
                <div id="errorDiv" class="alert alert-danger hidden"></div>
                <label for="first_name">First Name: </label>
                <input id="form_first_name" type="text" class="form-control required" name="first_name" required="true"><br>
                <label for="last_name">Last Name: </label>
                <input id="form_last_name" type="text" class="form-control required" name="last_name" required="true"><br>
                <label for="gender">Gender: </label>
                <select id="form_gender" class="form-control required" name="gender" required="true">
                    <option value="Female">Female</option>
                    <option value="Male">Male</option>
                    <option value="Unknown">Unknown</option>
                </select><br>
                <label for="email">EMail:</label>
                <input id="form_email" type="email" class="form-control required" name="email" required="true"><br>
                <label for="tel">Tel:</label>
                <input id="form_tel" type="text" class="form-control required" name="tel" required="true"><br>
                <button class="btn submitBtn btn-primary">New</button> <button type="reset" class="btn btn-primary">Clear</button> <button class="btn btn-primary" onclick="cancelForm()" >Cancel</button>
            </div>`;
    $('#customerform').empty();
    $('#customerform').append(form);
    $('.submitBtn').bind("click", () => {
        let first_name = $('#form_first_name').val();
        let last_name = $('#form_last_name').val();
        let gender = $('#form_gender').val();
        let email = $('#form_email').val();
        let tel = $('#form_tel').val();
        ajaxNewCustomer({
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'email': email,
            'tel': tel
        })
    });
}

function ajaxNewCustomer(customer) {
    $.ajax({
        url:  '/customer/list',
        type:  'post',
        dataType:  'json',
        data: customer,
        success:  function (data) {
            if (data.ret == 0) {
                let customer = data.customer;
                let row = `<tr id="tr_${customer.id}">
                                <td class="col-1">${customer.first_name} ${customer.last_name}</td>
                                <td class="col-3">${customer.gender}</td>
                                <td class="col-1">${customer.email}</td>
                                <td class="col-1">${customer.tel}</td>
                                <td class="col-3">
                                    <button class="btn deleteBtn btn-primary" data-id="${customer.id}">Delete</button>
                                    <button class="btn updateBtn btn-primary" data-id="${customer.id}">Update</button>
                                    <button class="btn checkInBtn btn-primary" data-id="${customer.id}">Check-In</button>
                                </td>
                            </tr>`;
                $('#myTable tbody').append(row);
                $('#customerform').empty();
                bindBtn();
            } else {
                let errorRow = `<div id="errorDiv" class="alert alert-danger">${data.message}</div>`
                $('#errorDiv').replaceWith(errorRow)
            }

        }
    });
}

function updateCustomer(el){
    let customerId  =  $(el).data('id')
    $.ajax({
        url:  `/customer/${customerId}`,
        type:  'get',
        dataType:  'json',
        success:  function (data) {
            if (data.ret == 0) {
                let customer = data.customer;
                let form = `<br><br>
                       <div>
                            <div id="errorDiv" class="alert alert-danger hidden"></div>
                            <input id="form_id" type="hidden" value="${customer.id}">
                            <label for="first_name">First Name: </label>
                            <input id="form_first_name" type="text" class="form-control required" name="first_name" value="${customer.first_name}" required="true"><br>
                            <label for="last_name">Last Name: </label>
                            <input id="form_last_name" type="text" class="form-control required" name="last_name" value="${customer.last_name}" required="true"><br>
                            <label for="gender">Gender: </label>
                            <select id="form_gender"  class="form-control required" name="gender">
                                <option value="Female">Female</option>
                                <option value="Male">Male</option>
                                <option value="Unknown">Unknown</option>
                            </select><br>
                            <label for="email">Email:</label>
                            <input id="form_email" type="text" class="form-control required" name="email" value="${customer.email}" required="true"><br>
                            <label for="tel">Tel:</label>
                            <input id="form_tel" type="text" class="form-control required" name="tel" value="${customer.tel}" required="true"><br>
                            <button class="btn submitBtn btn-primary">Update</button><button type="reset" class="btn btn-primary">Clear</button><button class="btn btn-primary" onclick="cancelForm()" >Cancel</button>
                        </div>`;
                $('#customerform').empty();
                $('#customerform').append(form);
                $('#form_gender').val(`${customer.gender}`);
                $('.submitBtn').bind("click", () => {
                    let id = $('#form_id').val();
                    let first_name = $('#form_first_name').val();
                    let last_name = $('#form_last_name').val();
                    let gender = $('#form_gender').val();
                    let email = $('#form_email').val();
                    let tel = $('#form_tel').val();
                    ajaxUpdateCustomer({
                        'id': id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'gender': gender,
                        'email': email,
                        'tel': tel
                    }, el)
                });
            }
        }
    });
}


function ajaxUpdateCustomer(customer, elm) {
    $.ajax({
        url:  `/customer/${customer.id}`,
        type:  'post',
        dataType:  'json',
        data: customer,
        success:  function (data) {
            if (data.ret == 0) {
                let customer = data.customer;
                let updatedRowElement = $('#tr_' + customer.id);
                row = `<tr id="tr_${customer.id}">
                    <td class="col-1">${customer.first_name} ${customer.last_name}</td>
                    <td class="col-3">${customer.gender}</td>
                    <td class="col-1">${customer.email}</td>
                    <td class="col-1">${customer.tel}</td>
                    <td class="col-3">
                        <button class="btn deleteBtn btn-primary" data-id="${customer.id}">Delete</button>
                        <button class="btn updateBtn btn-primary" data-id="${customer.id}">Update</button>
                        <button class="btn checkInBtn btn-primary" data-id="${customer.id}">Check-In</button>
                     </td>
                    </tr>`;
                updatedRowElement.replaceWith(row);
                $('#customerform').empty();
                bindBtn();
            } else {
                let errorRow = `<div id="errorDiv" class="alert alert-danger">${data.message}</div>`
                $('#errorDiv').replaceWith(errorRow)
            }

        }
    });
}

function cancelForm() {
    $('#customerform').empty();
}