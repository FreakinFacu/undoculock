$(function () {

    function checkLoginState() {
        FB.getLoginStatus(function (response) {

                if (response.status === "connected") {

                    FB.api('/me', function (response) {
                        $.ajax({
                            type: 'POST',
                            url: '/actions/login',
                            data: JSON.stringify(response),
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
                    })
                    ;
                }
            }
        );


    }

    window.checkLoginState = checkLoginState;
})
;
