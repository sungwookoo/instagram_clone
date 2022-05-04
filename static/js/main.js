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


// 모달 버튼에 이벤트를 건다.
$('.downloadimg').on('click', function(){
$('#modalBox').modal('hide');
});