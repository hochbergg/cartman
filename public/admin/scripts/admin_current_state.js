$(document).ready(function () {
    var tableBody = $('#log-table');
    var actionDropDownElem = $('#action-buttons');
    actionDropDownElem.show();
    var actionDropDown = actionDropDownElem.html();
    actionDropDownElem.hide();
    $.ajax({
        url: 'data/',
        data: [],
        success: function (data) {
            var res = data.msg;
            $('#log-title').html(data.title);
            for (var i = 0; i < res.length; i++) {
                tableBody.append("<tr data-cart=" + res[i]['cartId'] + "><td>" + res[i]['cartId'] + "</td> <td>" + res[i]['status'] + "</td> <td>" + res[i]['userId'] + "</td> <td>" + actionDropDown + "</td></tr>")
            }
        }

    });

    tableBody.on('click', '.btn-set-as', function (event) {
            var targetStatus = $(this).data('status');
            var cartId = $(this).parent().parent().data('cart');
            $.ajax({
                url: '/admin/change-status/',
                data: JSON.stringify({
                    cartId: cartId,
                    targetStatus: targetStatus
                }),
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data) {
                    console.log(data);
                    //    alert success of change
                    //    change in current state.
                },
                error: function(){
                    console.log('error')
                }
            })
        }
    )
});