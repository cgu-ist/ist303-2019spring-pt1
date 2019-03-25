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


function get_billing() {
    let start = $('#form_startdate').val();
    let end = $('#form_enddate').val();
    let customer_id = $('#form_customer').val();

    $.ajax({
        url:  'billing/summary',
        type:  'post',
        data:{
            start: start,
            end: end,
            customer_id: customer_id
        },
        dataType:  'json',
        success: function  (data) {
            if (data.ret == 0) {
                let summary = `<h2 class="col-sm-12">Billing Summary</h2>
                    <p><span class="col-sm-6">Customer: ${data.customer_name}</span><span class="col-sm-6">Total Due: <span class="dollar">${data.total}</span></span></p>
                    <p><span class="col-sm-6">Start: ${data.start}</span><span class="col-sm-6">End: ${data.end}</span></p>
                `;
                console.log(data.reservations);
                summary += `<table  class="table table-sm table-striped table-hover"  id="billingTable">
                        <thead class="thead-dark">
                            <th class="col-2 text-left">Service</th>
                            <th class="col-2 text-left">Start Time</th>
                            <th class="col-2 text-left">Service Time</th>
                            <th class="col-3 text-left">Rate</th>
                            <th class="col-3 text-left">Amount</th>
                        </thead>
                        <tbody>`;
                data.reservations.forEach(reservation => {
                    summary += `<tr>
                        <td>${reservation.reservation_service.name}</td>
                        <td>${reservation.start_time}</td>
                        <td>${reservation.period}</td>
                        <td>${reservation.reservation_service.rate}</td>
                        <td>${reservation.amount}</td>
                        </tr>`;
                });
                summary += `</tbody></table>`;
                $('#billDiv').html(summary);
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
