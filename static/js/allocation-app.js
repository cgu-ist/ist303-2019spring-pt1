$.ajax({
    url:  '/customer/list',
    type:  'get',
    dataType:  'json',
    success: function  (data) {
        if (data.ret == 0) {
            rows = data.customers.map(customer => {
                return `<option value='${customer.id}'>${customer.first_name} ${customer.last_name}</option>`;
            })
            $('#form_customer').html(rows);
        } else {

        }
    }
});


function get_allocation() {
    let end = $('#form_enddate').val();
    let customer_id = $('#form_customer').val();

    $.ajax({
        url:  'allocation/summary',
        type:  'post',
        data:{
            end: end,
            customer_id: customer_id
        },
        dataType:  'json',
        success: function  (data) {
            if (data.ret == 0) {
                $('#billDiv').empty();
                let summary = `<div class="'container"><div class="row"><h2>Billing Summary</h2></div>
                    <div class="row">
                        <div class="col-sm-2">Customer : </div>
                        <div class="col-sm-4">${data.customer_name}</div>
                        <div class="col-sm-2">Total Due : </div>
                        <div class="col-sm-4"><span class="dollar">${data.total}</span><</div>
                    </div>
                    <div class="row">
                        <div class="col-sm-2">Start : </div>
                        <div class="col-sm-4">${data.start}</div>
                        <div class="col-sm-2">End : </div>
                        <div class="col-sm-4">${data.end}<</div>
                    </div>
                `;
                summary += `<div class="row">
                                <table  class="table table-sm table-striped table-hover"  id="billingTable">
                                    <thead class="thead-dark">
                                        <th class="col-2 text-left">Service</th>
                                        <th class="col-2 text-left">Service Date</th>
                                        <th class="col-2 text-left">Start Time</th>
                                        <th class="col-2 text-left">Service Time</th>
                                        <th class="col-2 text-left">Rate</th>
                                        <th class="col-2 text-left">Amount</th>
                                    </thead>
                                <tbody>`;
                data.reservations.forEach(reservation => {
                    summary += `<tr>
                                    <td>${reservation.reservation_service.name}</td>
                                    <td>${reservation.date}</td>
                                    <td>${reservation.start_time}</td>
                                    <td>${reservation.period} minutes</td>
                                    <td>${reservation.reservation_service.rate}</td>
                                    <td>${reservation.amount}</td>
                                </tr>`;
                });
                summary += `</tbody>
                        </table>
                    </div>
                </div>`;
                $('#billDiv').append(summary);

                let cancelled = `<h2 class="col-sm-12" style="margin-top: 10px;">Cancelled Reservations</h2>`;
                cancelled += `<table  class="table table-sm table-striped table-hover"  id="billingTable">
                        <thead class="thead-dark">
                            <th class="col-2 text-left">Service</th>
                            <th class="col-2 text-left">Service Date</th>
                            <th class="col-2 text-left">Start Time</th>
                            <th class="col-2 text-left">Service Time</th>
                        </thead>
                        <tbody>`;
                data.cancelled_reservations.forEach(reservation => {
                    cancelled += `<tr>
                        <td>${reservation.reservation_service.name}</td>
                        <td>${reservation.date}</td>
                        <td>${reservation.start_time}</td>
                        <td>${reservation.period} minutes</td>
                        </tr>`;
                });
                cancelled += `</tbody></table></div>`;
                $('#billDiv').append(cancelled);

                $('#btnPrint').removeClass('btn-secondary');
                $('#btnPrint').addClass('btn-primary');
                $('#btnPrint').removeAttr('disabled')
            } else {

            }
        }
    });
}

function print_billing() {
     $('<iframe>', {
        name: 'billingSummary',
        class: 'printFrame'
      })
      .appendTo('body')
      .contents().find('body')
      .append($('#billDiv').html());
     window.frames['billingSummary'].focus();
     window.frames['billingSummary'].print();
}
