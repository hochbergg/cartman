$(document).ready(function () {
    var tableBody = $('#log-table');
    $.ajax({
        url: '/auth/login/',
        data: JSON.stringify({
            username: 'admin',
            password: 'Password1'
        }),
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            console.log(data);
            $.ajax({
                url: '/api/admin/log/data/?access_token=' + data['access_token'],
                data: [],
                success: function (data) {
                    var res = data.msg;
                    $('#log-title').html(data.title);
                    for (var i = 0; i < res.length; i++) {
                        console.log(res[i]);
                        console.log(tableBody);
                        tableBody.append("<tr><td>" + res[i]['createdAt'] + "</td> <td>" + res[i]['eventId'] + "</td> <td>" + res[i]['user'] + "</td> <td>" + res[i]['cart'] + "</td> <td>" + res[i]['name'] + "</td></tr>")
                    }
                }

            })
        }
    });

});