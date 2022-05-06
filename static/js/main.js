$(document).ready(function () {
    getFeed();

})


// 댓글 작성(POST) API
function saveComment(i, feed_idx) {
    let content = $('#input-comment'+i).val()
    if (content === '') {
        alert("입력하지 않은 항목이 존재합니다.");
        return;
    }
    $.ajax({
            type: "POST",
            url: "/api/comment",
            data: {content: content, feed_idx: feed_idx},
            success: function (response) {
                alert(response["msg"]);
                window.location.reload();
            }
        }
    )
}

// 좋아요 기능(POST) API
function saveLike(feed_idx) {
    $.ajax({
            type: "POST",
            url: "/api/like",
            data: {feed_idx: feed_idx},
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
            let comments = response['all_comments'];
            let likes = response['all_likes'];
            for (let i = 0; i < feeds.length; i++) {
                let created_at = feeds[i]['created_at'];
                let content = feeds[i]['content'];
                let feed_img_src = feeds[i]['feed_img_src'];
                let user_id = feeds[i]['user_id'];
                let feed_idx = feeds[i]['_id'];
                let like_count = 0;
                for (let k = 0; k < likes.length; k++) {
                    if (likes[k]['feed_idx']===feed_idx) {
                        like_count++
                    }

                }
                for (let j = 0; j < users.length; j++) {
                    if (user_id === users[j]['user_id']) {
                        let profile_img_src = users[j]['profile_img_src'];
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
                    <img src="${feed_img_src}"
                         alt="" class="mainPic">
                </div>
                <div class="icons-react">
                    <div class="icons-left">
                        <button class="like_button" onclick="saveLike('${feed_idx}')"></button>
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
                        <p><span class="point-span">좋아요</span> <span class="point-span">${like_count}개</span></p>
                    </div>
                    <div class="description">
                        <p><span class="point-span userID">${user_id}</span>${content}</p>
                    </div>
                    <div class="comment-section">
                        <ul class="comments" id="comment_list${i}">
                            <!-- input 값 여기에 추가 -->
                        </ul>
                        <div class="time-log">
                            <span>${created_at}</span>
                        </div>
                    </div>
                </div>
                <div class="hl"></div>
                <div class="comment">
                    <input id="input-comment${i}" class="input-comment" type="text" placeholder="댓글 달기...">
                    <button type="submit" class="submit-comment" onclick="saveComment('${i}', '${feed_idx}')">게시</button>
                </div>
            </article>`
                        $('#feeds').append(temp_html);

                    }

                }

                for (let x = 0; x < comments.length; x++) {
                    if (feed_idx === comments[x]['feed_idx']) {
                        let writer = comments[x]['writer_id'];
                        let comment_content = comments[x]['content'];
                        let temp_comment =
                            `<li>
                                <span><span class="point-span userID">${writer}</span>${comment_content}</span>
                            </li>`
                        $('#comment_list'+i).append(temp_comment);
                    }
                }

            }
        }
    })
}

