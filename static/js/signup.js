let phone = '';
let email = '';

function checkEmailOrPhone() {
    let phone_or_email = $('#phone_or_email').val()
    if (phone_or_email !== ''){
        if(phone_or_email.indexOf(('@')) !== -1) {
            // 이메일 주소
            let regEmail = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/;
            if (regEmail.test(phone_or_email) === true) {
                email = phone_or_email;
                return 'email'
            }
            else {
                return 'wrong';
            }
        }
        else {
            // 휴대폰 번호
            let regPhone = /^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$/;
            if (regPhone.test(phone_or_email) === true) {
                // 숫자가 아닌 문자를 빈 문자로 변경
                let regNumber = /[^0-9]/g;
		        phone_or_email = phone_or_email.replace(regNumber, "");
                phone = phone_or_email;
                return 'phone';
            }
            else {
                return 'wrong';
            }
        }
    }
    else{
        return 'empty';
    }
}

function checkNotEmpty() {
    return $('#password').val().length >= 5 && $('#phone_or_email').val().length > 0 && $('#name').length > 0 && $('#user_id').length > 0;
}

function checkForm() {
    if(checkEmailOrPhone() === 'wrong') {
        alert("잘못된 형식의 휴대폰 번호 또는 이메일 주소 입니다.");
        $('#phone_or_email').focus();
        return false;
    }

    if(!($('#password').val().length >= 5)) {
        alert("비밀번호는 최소 5자 이상이여야 합니다.");
        $('#password').focus();
        return false;
    }

    return true
}

function signup() {
    if(!checkForm()){
        return;
    }
    let user_id = $('#user_id').val();
    let password = $('#password').val();
    let name = $('#name').val();

    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {id_give: user_id, pw_give: password, name_give: name, phone_give: phone, email_give: email},
        success: function (response) {
                alert(response['msg'])
                window.location.href = '/login';
        }
    })
}

$('.container').keyup("keyup", function() {
    let completedInput = checkNotEmpty();
    $('#btn_signup').attr('disabled',!completedInput);
});

document.addEventListener('keyup', function (event) {
    // 임시 - 엔터 입력 시 메인 페이지 이동
    if (event.keyCode === 13) {
        window.location.href = "http://localhost:5000/main";
        // loginBtn.click();
    }
})