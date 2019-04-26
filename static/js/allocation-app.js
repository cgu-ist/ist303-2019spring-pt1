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
                $('#allocationDiv').empty();
                let summary = `<div class="row resultdiv">
                                    <div class="col-sm-12" style="padding: 10px 160px 2px 160px;">
                                        <div class="col-sm-2"> Not available : </div>
                                        <div class="col-sm-1"> 
                                            <div class="unavailable-block"/>
                                        </div>
                                        <div class="col-sm-2"> Available : </div>
                                        <div class="col-sm-1"> 
                                            <div class="available-block"/>
                                        </div>
                                        <div class="col-sm-2"> Past : </div>
                                        <div class="col-sm-1"> 
                                            <div class="past-block"/>
                                        </div>
                                    </div>`;
                const moment_start = moment(data.start, "YYYY-MM-DD");
                console.log(moment_start);
                for (let [service, allocations] of Object.entries(data.allocations)) {
                    summary += `<div class="col-sm-12" style="padding: 4px 10px;">
                                    <h5 style="padding: 5px;">${service}</h5>
                                </div>`;
                    allocations.forEach((day_allocation, day) => {
                        let m = moment_start.clone().add(day, 'days').add(8, 'hours');
                        summary += `<div class="col-sm-12">`
                        day_allocation.forEach((b, h) => {
                            let moment_block_start = m.add(h === 0 ? 0 : 15, 'minutes');

                            if (moment_block_start >= moment()) {
                                 let placeholder_text = (b === 1 ? "Available" : "Not available") + " at " + moment_block_start.local().format('MMM DD HH:mm');
                                 let div_class = b === 1 ? "available" : "unavailable";
                                 summary += `<div class="${div_class}">
                                                <span class="tooltiptext">${placeholder_text}</span>    
                                            </div>`
                            } else {
                                 summary += `<div class="past"></div>`
                            }
                        })
                        summary += `</div>`
                    });
                }
                summary += `</div>`;
                $('#allocationDiv').append(summary);
            } else {
                $('#allocationDiv').empty();
            }
        }
    });
}
