$.ajax({
    url:  '/service/list',
    type:  'get',
    dataType:  'json',
    success: function  (data) {
        if (data.ret == 0) {
            let rows =  '';
            data.services.forEach(service => {
                rows += `<tr id="tr_${service.id}">
                        <td class="col-1">${service.name}</td>
                        <td class="col-3">${service.description}</td>
                        <td class="col-1">${service.min_service_time}</td>
                        <td class="col-1">${service.max_service_time}</td>
                        <td class="col-1"><span>&#36;</span>${service.rate}</td>
                        <td class="col-2">${service.limit}</td>
                        <td class="col-3">
                            <button class="btn deleteBtn btn-primary" data-id="${service.id}">Delete</button>
                            <button class="btn updateBtn btn-primary" data-id="${service.id}">Update</button>
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
            deleteService($(elm))
        })
    })
    $('.updateBtn').each((i, elm) => {
        $(elm).on("click",  (e) => {
            updateService($(elm))
        })
    })
}

function deleteService(el){
    let customerId  =  $(el).data('id')
    $.ajax({
        url:  `/service/${customerId}`,
        type:  'delete',
        dataType:  'json',
        success:  function (data) {
            $(el).parents()[1].remove()
        }
    });
}

function newService(){
    let form = `<br><br>
           <div>
                <div id="errorDiv" class="alert alert-danger hidden"></div>
                <label for="name">Name: </label>
                <input id="form_name" type="text" class="form-control required" name="name" required="true"><br>
                <label for="name">Description: </label>
                <input id="form_description" type="text" class="form-control required" name="description" required="true"><br>
                <label for="min_service_time">Min Time Allow: </label>
                <input id="form_min_service_time" type="number" class="form-control required" name="time_type" required="true"><br>
                <label for="max_service_time">Max Time Allow: </label>
                <input id="form_max_service_time" type="number" class="form-control required" name="time_type" required="true"><br>
                <label for="rate">Rate:</label>
                <input id="form_rate" type="text" class="form-control required" name="rate" required="true"><br>
                <label for="limit">Limit:</label>
                <input id="form_limit" type="number" class="form-control" name="limit" min="1" max="65535" value="unlimited"><br>
                <button class="btn submitBtn btn-primary">New</button>&nbsp;
                <button type="reset" class="btn btn-primary">Clear</button>&nbsp;
                <button class="btn btn-primary" onclick="cancelForm()">Cancel</button>
            </div>`;
    $('#serviceform').empty();
    $('#serviceform').append(form);
    $('.submitBtn').bind("click", () => {
        let name = $('#form_name').val();
        let description = $('#form_description').val();
        let min_service_time = $('#form_min_service_time').val();
        let max_service_time = $('#form_max_service_time').val();
        let rate = $('#form_rate').val();
        let limit = $('#form_limit').val();
        ajaxNewService({
            'name': name,
            'description': description,
            'min_service_time': min_service_time,
            'max_service_time': max_service_time,
            'rate': rate,
            'limit': limit
        })
    });
}

function ajaxNewService(service) {
    $.ajax({
        url:  '/service/list',
        type:  'post',
        dataType:  'json',
        data: service,
        success:  function (data) {
            if (data.ret == 0) {
                let service = data.service;
                let row = `<tr id="tr_${service.id}">
                                <td class="col-1">${service.name}</td>
                                <td class="col-2">${service.description}</td>
                                <td class="col-2">${service.min_service_time}</td>
                                <td class="col-2">${service.max_service_time}</td>
                                <td class="col-1"><span>&#36;</span>${service.rate}</td>
                                <td class="col-2">${service.limit}</td>
                                <td class="col-2">
                                    <button class="btn deleteBtn btn-primary" data-id="${service.id}">Delete</button>
                                    <button class="btn updateBtn btn-primary" data-id="${service.id}">Update</button>
                                </td>
                            </tr>`;
                $('#myTable tbody').append(row);
                $('#serviceform').empty();
                bindBtn();
            } else {
                let errorRow = `<div id="errorDiv" class="alert alert-danger">${data.message}</div>`
                $('#errorDiv').replaceWith(errorRow)
            }

        }
    });
}

function updateService(el){
    let customerId  =  $(el).data('id')
    $.ajax({
        url:  `/service/${customerId}`,
        type:  'get',
        dataType:  'json',
        success:  function (data) {
            if (data.ret == 0) {
                let service = data.service;
                let form = `<br><br>
                       <div>
                            <div id="errorDiv" class="alert alert-danger hidden"></div>
                            <input id="form_id" type="hidden" value="${service.id}">
                            <label for="name">Name: </label>
                            <input id="form_name" type="text" class="form-control required" name="name" value="${service.name}" required="true"><br>
                            <label for="name">Description: </label>
                            <input id="form_description" type="text" class="form-control required" name="description" value="${service.description}" required="true"><br>
                            <label for="min_service_time">Min Time Allow: </label>
                            <input id="form_min_service_time" type="number" class="form-control required" name="time_type" value="${service.min_service_time}" required="true"><br>
                            <label for="max_service_time">Max Time Allow: </label>
                            <input id="form_max_service_time" type="number" class="form-control required" name="time_type" value="${service.max_service_time}" required="true"><br>
                            <label for="rate">Rate:</label>
                            <input id="form_rate" type="text" class="form-control required" name="rate" value="${service.rate}" required="true"><br>
                            <label for="limit">Limit:</label>
                            <input id="form_limit" type="number" class="form-control" name="limit" min="1" max="65535" value="${service.limit}"><br>
                            <button class="btn submitBtn btn-primary">Update</button>&nbsp;<button type="reset" class="btn btn-primary">Clear</button>&nbsp;<button class="btn btn-primary" onclick="cancelForm()" >Cancel</button>
                        </div>`;
                $('#serviceform').empty()
                $('#serviceform').append(form)
                $('.submitBtn').bind("click", () => {
                    let id = $('#form_id').val();
                    let name = $('#form_name').val();
                    let description = $('#form_description').val();
                    let min_service_time = $('#form_min_service_time').val();
                    let max_service_time = $('#form_max_service_time').val();
                    let rate = $('#form_rate').val();
                    let limit = $('#form_limit').val();
                    ajaxUpdateService({
                        'id': id,
                        'name': name,
                        'description': description,
                        'min_service_time': min_service_time,
                        'max_service_time': max_service_time,
                        'rate': rate,
                        'limit': limit
                    }, el)
                });
            }
        }
    });
}


function ajaxUpdateService(service, elm) {
    $.ajax({
        url:  `/service/${service.id}`,
        type:  'post',
        dataType:  'json',
        data: service,
        success:  function (data) {
            if (data.ret == 0) {
                let service = data.service;
                let updatedRowElement = $('#tr_' + service.id);
                row = `<tr id="tr_${service.id}">
                    <td class="col-1">${service.name}</td>
                    <td class="col-3">${service.description}</td>
                    <td class="col-1">${service.min_service_time}</td>
                    <td class="col-1">${service.max_service_time}</td>
                    <td class="col-1"><span>&#36;</span>${service.rate}</td>
                    <td class="col-2">${service.limit}</td>
                    <td class="col-3">
                        <button class="btn deleteBtn btn-primary" data-id="${service.id}"">Delete</button>
                        <button class="btn updateBtn btn-primary" data-id="${service.id}"">Update</button>
                     </td>
                    </tr>`;
                updatedRowElement.replaceWith(row);
                $('#serviceform').empty();
                bindBtn();
            } else {
                let errorRow = `<div id="errorDiv" class="alert alert-danger">${data.message}</div>`
                $('#errorDiv').replaceWith(errorRow)
            }

        }
    });
}

function cancelForm() {
    $('#serviceform').empty();
}