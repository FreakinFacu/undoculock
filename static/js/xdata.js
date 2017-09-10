//// SFACEBOOK MODEULE ////
var prev_val;
$(document).ready(function () {
    $('#s_fb').click(function () {
        prev_val = $(this).val();
    }).change(function () {
        $(this).unbind('click');
        if ($(this).prop('checked') === true) {
            //            if the switch is turn onn then put code here!
            //            Materialize.toast('Activating share via facebook',3000);
            var user_fb = prompt("Please Enter the user name");

            //            ## if cancell, change the value to dissable
            if (user_fb === null) {
                //                This string will grab the current value
                _val = $('#s_fb').value;
                x = _val ? false : true;
                if (x === true) {
                    console.log("Cancelled");
                } else {
                    console.log("null error on like switch");
                };

            } else if (user_fb === "") {
                alert("You have not entered a valid email. ");
                $(this).val(prev_val);
                $(this).bind('click');
                return false;
            } else {
                console.log("user selected " + user_fb)
                Materialize.toast('Activating share via facebook', 3000);
            };

        } else {
            //            if switch is deactivated then put code here!
            Materialize.toast('Facebook shared has been deactivated', 3000);
        }
    });
});


//// SHARE EMAIL MODULE ////

$(document).ready(function () {
    $('#s_email').change(function () {
        if ($(this).prop('checked') === true) {
            Materialize.toast('Activating share via email', 3000);
            let user_input
        }

    })
})
