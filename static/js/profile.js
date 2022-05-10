$(document).ready(function () {
    getProfile();
})

function logout() {
    $.ajax({
        type: "GET",
        url: "/api/logout",
        data: {},
        success: function (response) {
            if (response['result'] === 'success') {
                $.removeCookie('token', response['token'])
                alert(response['msg'])
                window.location.href = '/';
            } else {
                alert(response['msg'])
                window.location.href = '/';
            }
        }
    })
}

function getProfile() {
    $.ajax({
        type: "GET",
        url: "/api/profile",
        data: {'user_id'},
        success: function (response) {
        let users = response['all_users'];
        }
    })
}
