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


function get_allocations() {
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
                let summary = `<div class="'container">
                            <div class="row">
                                <table  class="table table-sm table-striped table-hover"  id="billingTable">
                                    <thead class="thead-dark">
                                        <th class="col-2 text-left">Service</th>
                                        <th class="col-2 text-left">Allocation Start</th>
                                        <th class="col-2 text-left">Allocation End</th>
                                    </thead>
                                <tbody>`;

                for (let [service, allocations] of Object.entries(data.allocations)) {
                    allocations.forEach(allocation => {
                        summary += `<tr>
                                        <td>${service}</td>
                                        <td>${allocation.start}</td>
                                        <td>${allocation.end}</td>
                                    </tr>`;
                    });
                }
                summary += `</tbody>
                        </table>
                    </div>
                </div>`;
                $('#billDiv').append(summary);
            } else {

            }
        }
    });
}
