$(function () {
    $("#shareEmail").submit(function () {
        $.ajax({
            type: 'POST',
            url: '/actions/shareEmail',
            data: JSON.stringify({
                "email": $("#email").val()
            }),
            contentType: "application/json",
            dataType: 'json',
            success: function (response) {
                if (response.redirectUrl) {
                    location.href = response.redirectUrl;
                }
            },
            error: function (response) {
                if (response.responseJSON.errorMessage) {
                    $("#fbError").text(response.responseJSON.errorMessage).show()
                }
            }
        });
        return false;
    });

    $("#verifyShare").submit(function () {
        $.ajax({
            type: 'POST',
            url: '/actions/verifyEmail',
            data: JSON.stringify({
                "email": $("#email").val(),
                "share_key": $("#shareKey").val()
            }),
            contentType: "application/json",
            dataType: 'json',
            success: function (response) {
                $("#list").empty();

                if (response['results']) {
                    for (var i = 0; i < response['results'].length; i++) {
                        var item = response['results'][i];

                        $("#list").append(
                            $("<p>").text(item.id + " " + item.name)
                        )
                    }
                }
            },
            error: function (response) {
                if (response.responseJSON.errorMessage) {
                    $("#fbError").text(response.responseJSON.errorMessage).show()
                }
            }
        });
        return false;
    })
});