function login() {
    if(!checkNotEmpty()) {
        alert('잘못된 입력입니다.')
        return;
    }
     $.ajax({
                type: "POST",
                url: "/api/login",
                data: {id_give: $('#user_id').val(), pw_give: $('#password').val()},
                success: function (response) {
                    if(response['result'] === 'success') {
                        $.cookie('token', response['token'])
                        window.location.href = '/';
                    }
                    else {
                        alert(response['msg'])
                    }
                }
            })
}

function checkNotEmpty() {
    return $('#password').val().length >= 5 && $('#user_id').val().length > 0;
}

$('.container').keyup('keyup', function(event) {
    let completedInput = checkNotEmpty();
    $('#btn_login').attr('disabled',!completedInput);

    if(event.keyCode === 13) {
        if(checkNotEmpty()) {
            $('#btn_login').click();
        }
    }
});