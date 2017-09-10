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

                    var clone = $("#template").clone();
                    clone.show();
                    clone.find("a").attr("data-id", item.id);

                    $("ul.collection").append(
                        $("<li>")
                            .append($("<a>").text(item.name))
                            .append($("<i>").append(clone))
                    );

                    $("#verifyShare").slideUp();
                    $("table").slideDown();
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
});

$("table").on("click", "a.download_file", function () {
    var id = $(this).data("id");

    $.ajax({
        type: 'POST',
        url: '/actions/downloadFile',
        data: JSON.stringify({
            "email": $("#email").val(),
            "share_key": $("#shareKey").val(),
            "file_id": id
        }),
        contentType: "application/json",
        dataType: 'json',
        success: function (response) {
            if (response.redirectUrl) {
                location.href = response.redirectUrl;
            }

        }
    });
    return false;
});
