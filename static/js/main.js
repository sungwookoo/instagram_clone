$(document).ready(function () {
            getFeed();
        })


// 댓글 작성(POST) API
function saveComment() {
    let content = $('#comment_content').val()
    if (content === '') {
        alert("입력하지 않은 항목이 존재합니다.");
        return;
    }
    $.ajax({
            type: "POST",
            url: "/api/comment",
            data: {content: content, write_id: write_id, feed_idx: feed_idx},
            success: function (response) {
                alert(response["msg"]);
                window.location.reload();
            }
        }
    )
}

// 댓글 보여주기
function getComment() {
    $.ajax({
        type: "GET",
        url: "/api/comment",
        data: {},
        success: function (response) {
            let comments = response['all_comments'];
            for (let i = 0; i < comments.length; i++) {
                let writer = comments[i]['writer_id'];
                let feed_idx = comments[i]['feed_idx'];
                let content = comments[i]['content'];
                let created_at = comments[i]['created_at'];
                let temp_html =
                    '<li><span><span class="point-span userID">${writer}</span>${content}</span></li>'
                $('#comment_list').append(temp_html);
            }
        }
    })
}

// feed 작성(POST) API
function saveFeed() {
    $.ajax({
            type: "POST",
            url: "/api/feed",
            data: {user_id: user_id},
            success: function (response) {
                alert(response["msg"]);
                window.location.reload();
            }
        }
    )
}

// 피드 작성(GET) API
function getFeed() {
    $.ajax({
        type: "GET",
        url: "/api/feed",
        data: {},
        success: function (response) {
            let users = response['all_users'];
            let feeds = response['all_feeds'];
            for (let i = 0; i < feeds.length; i++) {
                let created_at = feeds[i]['created_at'];
                let content = feeds[i]['content'];
                let user_id = feeds[i]['user_id'];
                for (let j = 0; j < users.length; j++) {
                    if (user_id===users[j]['user_id']) {
                        let profile_img_src = users[i]['profile_img_src'];
                        let temp_html =
                            `<article>
            <header>
                <div class="profile-of-article">
                    <img class="img-profile pic"
                         src="${profile_img_src}"
                         alt="">
                    <span class="userID main-id point-span">${user_id}</span>
                </div>
                <img class="icon-react icon-more"
                     src="https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bearu/more.png" alt="more">
            </header>
            <div class="main-image">
                <img src="${content}"
                     alt="" class="mainPic">
            </div>
            <div class="icons-react">
                <div class="icons-left">
                    <img class="icon-react"
                         src="https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bearu/heart.png" alt="하트">
                    <img class="icon-react"
                         src="https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bearu/comment.png" alt="말풍선">
                    <img class="icon-react" src="../static/img/dm.png" alt="DM">
                </div>
                <img class="icon-react"
                     src="https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bearu/bookmark.png" alt="북마크">
            </div>
            <!-- article text data -->
            <div class="reaction">
                <div class="liked-people">
                    <img class="pic"
                         src="https://teamsparta.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fe998903e-bca5-4c55-9487-ae69c8224c92%2F%E3%85%87.heic?table=block&id=13935d17-fbbd-4173-8729-2f6540ca1818&spaceId=83c75a39-3aba-4ba4-a792-7aefe4b07895&width=1440&userId=&cache=v2"
                         alt="hwi_ssu님의 프로필 사진">
                    <p><span class="point-span">hwi_ssu</span>님 <span class="point-span">외 2,412,751명</span>이 좋아합니다</p>
                </div>
                <div class="description">
                    <p><span class="point-span userID">dlwlrma</span><span class="at-tag">@wkorea @gucci</span> 🌱</p>
                </div>
                <div class="comment-section">
                    <ul class="comments" id="comment_list">
                        <li>
                            <span><span class="point-span userID">postmalone</span>내가 입으면 더 잘어울릴 것 같아</span>
                        </li>
                        <!-- input 값 여기에 추가 -->
                    </ul>
                    <div class="time-log">
                        <span>${created_at}</span>
                    </div>
                </div>
            </div>
            <div class="hl"></div>
            <div class="comment">
                <input id="input-comment" class="input-comment" type="text" placeholder="댓글 달기...">
                <button type="submit" class="submit-comment" disabled>게시</button>
            </div>
        </article>`
                        $('#feeds').append(temp_html);

                    }

                }
            }
        }
    })
}

