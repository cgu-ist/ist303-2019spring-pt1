$.ajax({
    url:  '/reservations',
    type:  'get',
    dataType:  'json',
    success: function  (data) {
        if (data.ret == 0) {
                console.log(data.reservations);
            // let rows =  '';
            // data.customers.forEach(customer => {
            //     rows += `<tr id="tr_${customer.id}">
            //             <td class="col-1">${customer.first_name} ${customer.last_name}</td>
            //             <td class="col-3">${customer.gender}</td>
            //             <td class="col-1">${customer.email}</td>
            //             <td class="col-1">${customer.tel}</td>
            //             <td class="col-3">
            //                 <button class="btn deleteBtn btn-primary" data-id="${customer.id}"">Delete</button>
            //                 <button class="btn updateBtn btn-primary" data-id="${customer.id}"">Update</button>
            //             </td>
            //         </tr>`;
            // });
            //
            // $('#myTable tbody').append(rows);
            // bindBtn();
        } else {
            // do something
        }
    }
});

var calendar = $("#calendar").calendar({
    tmpl_path: "/reservation/calendar/",
    view: 'month',
    events_source: function () { return []; },
    onAfterViewLoad: function(view) {
        $('.page-header h3').text(this.getTitle());
        $('.btn-group button').removeClass('active');
        $('button[data-calendar-view="' + view + '"]').addClass('active');
    },
    classes: {
        months: {
            general: 'label'
        }
    },
    time_start: '08:00',
    time_end: '20:00',
    events_url: '/reservation/new'
});

$('.btn-group button[data-calendar-nav]').each(function() {
    var $this = $(this);
    $this.click(function() {
        calendar.navigate($this.data('calendar-nav'));
    });
});

$('.btn-group button[data-calendar-view]').each(function() {
    var $this = $(this);
    $this.click(function() {
        calendar.view($this.data('calendar-view'));
    });
});

$('#first_day').change(function(){
    var value = $(this).val();
    value = value.length ? parseInt(value) : null;
    calendar.setOptions({first_day: value});
    calendar.view();
});

$('#language').change(function(){
    calendar.setLanguage($(this).val());
    calendar.view();
});

$('#events-in-modal').change(function(){
    var val = $(this).is(':checked') ? $(this).val() : null;
    calendar.setOptions({modal: val});
});
$('#format-12-hours').change(function(){
    var val = $(this).is(':checked') ? true : false;
    calendar.setOptions({format12: val});
    calendar.view();
});
$('#show_wbn').change(function(){
    var val = $(this).is(':checked') ? true : false;
    calendar.setOptions({display_week_numbers: val});
    calendar.view();
});
$('#show_wb').change(function(){
    var val = $(this).is(':checked') ? true : false;
    calendar.setOptions({weekbox: val});
    calendar.view();
});
$('#events-modal .modal-header, #events-modal .modal-footer').click(function(e){
    //e.preventDefault();
    //e.stopPropagation();
});

$('#newEventModal').on('show.bs.modal', function (event) {
    $.ajax({
        url:  '/service/list',
        type:  'get',
        dataType:  'json',
        success: function  (data) {
            if (data.ret == 0) {
                let time_rows = {}
                data.services.forEach(service => {
                    let time = service.time_type.split(",")
                    time_rows[service.id] = time
                })

                $('#serviceSelect').change(function(){
                    console.log(time_rows)
                    let val = $(this).val()
                    let options = time_rows[val].map(t => {
                        return `<option value='${t}'>${t}</option>`
                    })
                    $('#spanSelect').html(options)
                });

                rows = data.services.map(service => {
                    return `<option value='${service.id}'>${service.description}</option>`;
                })
                $('#serviceSelect').append(rows);
                let options = time_rows[data.services[0].id].map(t => {
                    return `<option value='${t}'>${t}</option>`
                })
                $('#spanSelect').html(options)


            } else {

            }
        }
    })

    $.ajax({
        url:  '/customer/list',
        type:  'get',
        dataType:  'json',
        success: function  (data) {
            if (data.ret == 0) {
                rows = data.customers.map(customer => {
                    return `<option value='${customer.id}'>${customer.first_name} ${customer.last_name}</option>`;
                })
                $('#customerSelect').append(rows);
            } else {

            }
        }
    })
  // var button = $(event.relatedTarget) // Button that triggered the modal
  // var recipient = button.data('whatever') // Extract info from data-* attributes
  // // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  // var modal = $(this)
  // modal.find('.modal-title').text('New message to ' + recipient)
  // modal.find('.modal-body input').val(recipient)
})