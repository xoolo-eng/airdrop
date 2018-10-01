function add_balance(data, element) {
    var object = $("#"+element).get(0);
    old_value = $(object).html();
    new_value = old_value + " | balance: " + data;
    $(object).html(new_value)
}

function check_payment(address) {
    $.ajax({
        url: '/rest/check_payment/',
        type: 'post',
        dataType: 'json',
        data: {
            "address": address,
            "order_id": order_id
        },
    })
    .done(function(data) {
        if (data["reload"]) {
            location.reload();
        }
        else {
            if (data["result"] !== undefined) {
                add_balance(data["result"], "payment");
            }
        }
    })
    .fail(function(data) {
        console.log(data);
    })  
}


function check_token(address, contract, order_id) {
    $.ajax({
        url: '/rest/check_token/',
        type: 'post',
        dataType: 'json',
        data: {
            "address": address,
            "contract": contract,
            "order_id": order_id
        },
    })
    .done(function(data) {
        if (data["reload"]) {
            location.reload();
        }
        else {
            if (data["result"] !== undefined) {
                add_balance(data["result"], "tokens");
            }
        }
    })
    .fail(function() {
        console.log();
        add_balance(0, "tokens");
    }) 
}


$(document).ready(function(){
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    check_payment(address);
    check_token(address, contract, order_id);
    setInterval(function (address) {
        check_payment(address);
    }, 60000)

    setInterval(function (address, contract, order_id) {
        check_token(address, contract, order_id);
    }, 60000)
});