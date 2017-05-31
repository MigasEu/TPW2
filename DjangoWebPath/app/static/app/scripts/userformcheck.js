

$(document).ready(function () {
    $("#user-form").validate({
        rules: {
            username: { pattern: /^[A-Za-z0-9]{5,30}$/ },
            password: { pattern: /^[A-Za-z0-9]{8,30}$/ },
            password1: { pattern: /^[A-Za-z0-9]{8,30}$/ },
            password2: { pattern: /^[A-Za-z0-9]{8,30}$/ }
        },
        messages: {
            username: "Incorrect username (5-30 numbers and letters)",
            password: "Incorrect password (8-30 numbers and letters)",
            password1: "Incorrect password (8-30 numbers and letters)",
            password2: "Incorrect password (8-30 numbers and letters)"
        }
    })
});