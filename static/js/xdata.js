//// SFACEBOOK MODEULE ////
$('#s_fb').bind('change', function (e) {
    console.log($(this).prop('checked'));
    if ($(this).prop('checked')) {
        // if the switch is turn onn then put code here!
        //             Materialize.toast('Activating share via facebook',3000);
        var user_fb = prompt("Please Enter the user name");

        //            ## if cancell, change the value to dissable
        if (user_fb === null) {
            //                This string will grab the current value
            _val = $('#s_fb').value;
            console.log(_val);
            x = _val ? false : true;
            console.log(x);
            if (x === true) {
                console.log("Cancelled");
            } else {
                console.log("null error on input");
            };

        } else if (user_fb === "") {
            alert("You have not entered a valid email. ");
            $(this).prop('checked', false);
            return false;
        } else {
            console.log("user selected " + user_fb)
            Materialize.toast('Activating share via facebook', 3000);
        };

    } else {
        //if switch is deactivated then put code here!
        Materialize.toast('Deactivating share via facebook', 3000);
        //            Materialize.toast('Deactivating share via facebook', 3000);
    }
});


//// SHARE EMAIL MODULE ////

$('#s_email').bind('change', function (e) {
    console.log($(this).prop('checked'));
    if ($(this).prop('checked')) {
        // if the switch is turn onn then put code here!
        //             Materialize.toast('Activating share via facebook',3000);
        var user_m = prompt("Please Enter an Email");

        //            ## if cancell, change the value to dissable
        if (user_m === null) {
            //                This string will grab the current value
            _val = $('#s_email').value;
            console.log(_val);
            x = _val ? false : true;
            console.log(x);
            if (x === true) {
                console.log("Cancelled");
            } else {
                console.log("null error on email input");
            };

        } else if (user_m === "") {
            alert("You have not entered a valid email. ");
            $(this).prop('checked', false);
            return false;
        } else {
            console.log("user selected " + user_m)
            Materialize.toast('Activating share via email', 3000);
        };

    } else {
        //if switch is deactivated then put code here!
        Materialize.toast('Deactivating share via email', 3000);
        //            Materialize.toast('Deactivating share via facebook', 3000);
    }
});


//// SHARE SMS MODULE ////

$('#sms').bind('change', function (e) {
    console.log($(this).prop('checked'));
    if ($(this).prop('checked')) {
        // if the switch is turn onn then put code here!
        //             Materialize.toast('Activating share via facebook',3000);
        var sms = prompt("Please Enter the phone number");

        //            ## if cancell, change the value to dissable
        if (sms === null) {
            //                This string will grab the current value
            _val = $('#sms').value;
            console.log(_val);
            x = _val ? false : true;
            console.log(x);
            if (x === true) {
                console.log("Cancelled");
            } else {
                console.log("null error on SMS input");
            };

        } else if (sms === "") {
            alert("You have not entered a valid phone number. ");
            $(this).prop('checked', false);
            return false;
        } else {
            console.log("user selected " + sms)
            Materialize.toast('Activating share via SMS', 3000);
        };

    } else {
        //if switch is deactivated then put code here!
        Materialize.toast('Deactivating share via SMS', 3000);
        //            Materialize.toast('Deactivating share via facebook', 3000);
    }
});
