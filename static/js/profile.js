$(document).ready(function () {
    getProfile();
})

// 로그아웃
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
        url: "/api/get_profile",
        data: {user_id: current_user_id},
        success: function (response) {

            let users = response['all_users'];
            let feeds = response['all_feeds'];
            let followers = response['all_followers'];

            let feed_count = feeds.length
            let follower_count = 0
            let following_count = 0

            for (let j = 0; j < followers.length; j++) {
                if (followers[j]['following'] === current_user_id){following_count ++}
                if (followers[j]['follower'] === current_user_id){follower_count ++}
            }
            console.log(following_count)
// 마이 프로필
            for (let i = 0; i < users.length; i++) {
                if (current_user_id === users[i]['user_id']) {
                    let profile_img = users[i]['profile_img_src'];
                    let name = users[i]['name'];
                    let user_id = users[i]['user_id'];
                    let temp_myprofile = `
                        <div class="profile_img">
                        <img class="profile_pic" src="${profile_img}" alt="프로필"></div>
                        <div class="profile_word">
                            <div class="profile_nickname_box">
                                <div class="profile_nickname">${user_id}</div>
                                <div class="profile_setting">
                                    <button class="setting_button" data-bs-toggle="modal" data-bs-target="#editprofileimg">프로필 편집</button>
                                </div>
                            </div>
                            <div class="profile_post_box">
                                <div class="profile_post">게시물 ${feed_count}</div>
                                <div class="profile_follower">팔로워 ${follower_count}</div>
                                <div class="profile_follow">팔로우 ${following_count}</div>
                            </div>
                            <div class="profile_name"><strong>${name}</strong></div>
                        </div>
                    `
                    $('#myprofileimg').append(temp_myprofile);

                    let temp_myprofilebar = `
                    <img class="pic" src="${profile_img}" alt="마이프로필">
                    `
                    $('#profilebar').append(temp_myprofilebar);
                }
            }
// 마이 피드
            console.log('a')
            for (let k = 0; k < feeds.length; k++) {
                if (current_user_id === feeds[k]['user_id']) {
                    let feed_img_src = feeds[k]['feed_img_src'];
                    let temp_myfeed = `
                        <div class="feed"><img src="${feed_img_src}" width="300" height="300"></div>
                        `
                    $('#myfeedimg').append(temp_myfeed);
                }
            }
        }
    })
}
