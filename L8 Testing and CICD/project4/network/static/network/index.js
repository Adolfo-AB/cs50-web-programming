document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Content Loaded Successfully")

    document.querySelector('#profile').style.display = 'none';
    if(document.getElementById('following')) {
        document.getElementById('following').addEventListener('click', () => loadPosts("/following",1));
    }
    loadPosts("",1);
});

function loadPosts(page, pageNum) {
    if (page.includes("?")) {
        page += `&page=${pageNum}`;
    } else {
        document.querySelector('#profile').style.display = 'none';
        page += `?page=${pageNum}`;
    }

    console.log(`Accessing ${page} Page`);

    fetch(`/load${page}`)
    .then(response => response.json())
    .then(response => {
        document.getElementById('posts').innerHTML="";
        buildPaginator(page, pageNum, response.num_pages);
        response.posts.forEach(post => buildPost(post));
    })
}

function buildPaginator(page, pageNum, totalPageNum) {
    pageList = document.getElementById('pagination');
    pageList.innerHTML = "";

    const prev = document.createElement('li');
    if (pageNum == 1) {
        prev.className = "pageitem disabled";
    } else {
        prev.className = "page-item";
        prev.addEventListener('click', () =D loadPosts(page, pageNum-1));
    }

    const aPrevPage = document.createElement('a');
    aPrevPage.className = "page-link";
    aPrevPage.href = "#";
    aPrevPage.innerHTML = "Older";
    prev.append(aPrevPage);
    pageList.append(prev);

    for (let i=1; i<=totalPageNum; i++) {
        const pageIcon = document.createElement('li');

        if (i == pageNum) {
            pageIcon.className = "page-item active";
        } else {
            pageIcon.className = "page-item";
            pageIcon.addEventListener('click', () => loadPosts(page,i));
        }

        const aPage = document.createElement('a');
        aPage.className = "page-link";
        aPage.href = "#";
        aPage.innerHTML = i;
        pageIcon.append(aPage);
        pageList.append(pageIcon);
    }

    const next = document.createElement('li');
    if (pageNum == totalPageNum) {
        next.className = "page-item disabled";
    } else {
        next.className = "page-item";
        next.addEventListener('click', () => loadPosts(page, pageNum+1));
    }

    aNextPage = document.createElement('a');
    aNextPage.className = "page-link";
    aNextPage.href = "#";
    aNextPage.innerHTML = "Newer";
    next.append(aNextPage);
    pageList.append(next);

}

function buildPost(post) {
    const postCard = document.createElement('div');
    postCard.className = "card mb-3";

    const rowNoGutters = document.createElement('div');
    rowNoGutters.className = "row no-gutters";
    
    const innerDiv = document.createElement('div');
    innerDiv.className = "col-md-8";

    const cardBody = document.createElement('div');
    cardBody.className = "card-body";
    cardBody.id = `post-body-${post.id}`;

    const cardAuthor = document.createElement('a');
    cardAuthor.className = "card-author";
    cardAuthor.innerHTML = post.author_username;
    cardBody.append(cardAuthor);
    cardAuthor.addEventListener('click', () => displayProfile(post.author_id));

    const cardContent = document.createElement('p');
    cardContent.className = "card-content";
    cardContent.id = `content-${post.id}`;
    cardContent.innerHTML = post.content;
    cardBody.append(cardContent);

    const cardDateTime = document.createElement('p');
    cardDateTime.className = "card-datetime";
    cardDateTime.innerHTML = post.datetime;
    cardBody.append(cardDateTime);

    const likesRow = document.createElement('div');
    likesRow.id = `likes-row-${post.id}`;
    likesRow.className = "row align-items-center";

    const likeIcon = document.createElement('i');
    likeIcon.id = `like-icon-${post.id}`;
    
    let heart_bg;
    if (post.liked) {
        heart_bg = "";
    } else {
        heart_bg = "-empty";
    }

    likeIcon.className = `icon-heart-${heart_bg} col-auto`;
    if (document.getElementById('following')) {
        likeIcon.addEventListener('click', () => updateLike(post));
    }

    likesRow.append(likeIcon);

    const likes = document.createElement('div');
    likes.id = `number-likes-${post.id}`;
    likes.className = "card-text likes col-auto";
    likes.innerHTML = post.likes;
    likesRow.append(likes);

    const likeText = document.createElement('div');
    likeText.className = "card-text likes_text col-auto";
    likeText.innerHTML = "Likes";
    likesRow.append(likeText);

    if (post.editable) {
        const edit = document.createElement('button');
        edit.className = "card-text col-auto btn btn-link";
        edit.innerHTML = "Edit";
        edit.addEventListener('click', () => editPost(post));
        likesRow.append(edit);
    }

    cardBody.append(likesRow);
    postCard.append(cardBody);

    const row = document.createElement('div');
    row.className = "row justify-content-center";
    row.append(postCard);

    document.querySelector('#posts').append(row);
}

function editPost(post) {
    const likesRow = document.getElementById(`likes-row-${post.id}`);
    const content = document.getElementById(`content-${post.id}`);

    const postBody = content.parentNode;
    const editBtnRow = document.createElement('div');
    editBtnRow.className = "row";

    const saveBtn = document.createElement('button');
    saveBtn.className = "btn btn-sm btn-outline-primary";
    saveBtn.type = "button";
    saveBtn.innerHTML = "Save Changes";
    saveBtn.addEventListener('click', () => {
        const newContent = document.getElementById(`new-content-${post.id}`).value;
        fetch(`/save_post`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': getCookie("csrftoken")
            },
            body: bod = JSON.stringify({
                post_id: post.id,
                newContent: new_content
            })
        })
        .then(response => response.json())
        .then(response => {
            
        })
    })
}

function updateLike(post) {
    fetch(`/post/${post.id}/update_like`)
    .then(response => response.json())
    .then(response => {
        if (response.liked) {
            document.getElementById(`like-icon-${post.id}`).className = "icon-heart col-auto";
        } else {
            document.getElementById(`like-icon-${post.id}`).className = "icon-heart-empty col-auto";
        }
        document.getElementById(`number-likes-${post.id}`).innerHTML = response.newAmount;
    })
}

function updateFollowStatus(userProfileId) {
    fetch(`/profile/${userProfileId}/update_follow`)
    .then(response => response.json())
    .then(response => {
        followBtn = document.getElementById('follow-button');
        if (response.newFollower) {
            newStatus = False
        }
    })
}



function displayProfile(authorId) {
    loadPosts(`?profile=${authorId}`, 1);
    document.querySelector('#new-post').style.display = 'none';
    followButton = document.getElementById('follow-button');
    followButton.style.display = 'none';
    document.querySelector('#profile').style.display = 'block';

    fetch(`/profile/${authorId}`)
    .then(response => response.json())
    .then(profile => {
        document.getElementById('num-following').innerHTML = profile.following;
        document.getElementById('num-followers').innerHTML = profile.followers;
        document.getElementById('profile-username').innerHTML = profile.username;

        if(profile.can_follow) {
            followButton.style.display = 'unset';
            if (profile.follow_status) {
                followButton.innerHTML = "Unfollow";
            } else {
                followButton.innerHTML = "Follow";
            }

            followButton.addEventListener('click', () => updateFollowStatus(authorId));

        }
    })

}
