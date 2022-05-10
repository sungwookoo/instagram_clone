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
        url: "/api/get_profile",
        data: {user_id: current_user_id},
        success: function (response) {
            console.log(response)

            let users = response['all_users'];
            let feeds = response['all_feeds'];
            // let followers = response['all_followers'];
            // let followings = response['all_followings'];

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
                                    <button class="setting_button">프로필 편집</button>
                                </div>
                            </div>
                            <div class="profile_post_box">
                                <div class="profile_post">게시물{feed_count}</div>
                                <div class="profile_follower">팔로워{temp}</div>
                                <div class="profile_follow">팔로우{temp}</div>
                            </div>
                            <div class="profile_name"><strong>${name}</strong></div>
                        </div>
                    `
                    $('#myprofileimg').append(temp_myprofile);
                }
            }
            for (let k = 0; k < feeds.length; k++) {
                if (current_user_id === feeds[k]['user_id']) {
                    let feed_img_src = feeds[k]['feed_img_src'];
                    let temp_myfeed = `
                        <div class="feed"><img src="${feed_img_src}" width="300" height="300"></div>
                        </div>
                        `
                    $('#myfeedimg').append(temp_myfeed);
                }
            }
        }
    })
}
