var options = {
    tmpl_path: "/reservation/calendar/",
    // tmpl_cache: false,
    view: 'month',
    events_source: () => [],
    onAfterEventsLoad: function(events) {
        if(!events) {
            return;
        }
        // let list = $('#eventlist');
        // list.html('');
        //
        // $.each(events, function(key, val) {
        //     $(document.createElement('li'))
        //         // .html('<a href="' + val.url + '">' + val.title + '</a>')
        //         .html('<span>' + val.title + '</span><button class="btn deleteBtn btn-primary" data-id="' + val.id + '">Delete</button>')
        //         .appendTo(list);
        // });
    },
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
    show_events_which_fits_time: true,
    time_start: '08:00',
    time_end: '20:00',
    events_url: '/reservation/new'
};

var calendar = $("#calendar").calendar(options);

getEvents();

function getEvents() {
    $.ajax({
        url:  '/reservations',
        type:  'get',
        dataType:  'json',
        success: function  (data) {
            if (data.ret == 0) {
                var event_sources = []
                data.reservations.forEach(reservation => {
                    event_sources.push({
                        "id": reservation.id,
                        "person": reservation.customer.first_name + ' ' + reservation.customer.last_name,
                        "title": reservation.reservation_service.name,
                        "description": reservation.reservation_service.description,
                        "url": '/reservation/' + reservation.id,
                        "start": reservation.datetime_start_ms,
                        "end": reservation.datetime_end_ms
                    })
                });

                let options = calendar.options
                calendar = $("#calendar").calendar(Object.assign({}, options, {
                    events_source:  () => event_sources
                }))
            } else {
                // do something
            }
        }
    });
}


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
    $('#errorDiv').html('');
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

                let rows = data.services.map(service => {
                    return `<option value='${service.id}'>${service.name}</option>`;
                })
                $('#serviceSelect').html(rows);
                let options = time_rows[data.services[0].id].map(t => {
                    return `<option value='${t}'>${t}</option>`
                })
                $('#spanSelect').html(options);


                $('#serviceSelect').change(function(){
                    let val = $(this).val()
                    let options = time_rows[val].map(t => {
                        return `<option value='${t}'>${t}</option>`
                    })
                    $('#spanSelect').html(options)
                });

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
                $('#customerSelect').html(rows);
            } else {

            }
        }
    })

    $('#btnNewReservation').on("click", (e) => {
        e.stopImmediatePropagation();
        createReservation();
    });
  // var button = $(event.relatedTarget) // Button that triggered the modal
  // var recipient = button.data('whatever') // Extract info from data-* attributes
  // // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  // var modal = $(this)
  // modal.find('.modal-title').text('New message to ' + recipient)
  // modal.find('.modal-body input').val(recipient)
})

function createReservation() {
    let reservation_date = $('#selectDate').text();
    let reservation_time = $('#selectTime').text();
    let service_id = $('#serviceSelect').val() ;
    let reservation_length = $('#spanSelect').val() ;
    let customer_id = $('#customerSelect').val() ;
    $.ajax({
    url:  '/reservation/new',
    type:  'post',
    data: {
        'reservation_date': reservation_date,
        'reservation_time': reservation_time,
        'service_id': service_id,
        'reservation_length': reservation_length,
        'customer_id': customer_id
    },
    dataType:  'json',
        success: function (data) {
            if (data.ret == 0) {
                $('#newEventModal').modal('hide');
                getEvents();

            } else {
                let errorMsg = `${data.message}`
                $('#errorDiv').html(errorMsg);
            }
        }
    })
}

function deleteReservation(id) {
    $.ajax({
    url:  '/reservation/delete',
    type:  'post',
    data: {
        'id': id,
    },
    dataType:  'json',
        success: function (data) {

            if (data.ret == 0) {
                getEvents();
            } else {
                let errorMsg = `${data.message}`
            }
        }
    })
}