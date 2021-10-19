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

            followButton.addEventListener('click', () => updateFollowStatus(authorId))

        }
    })

}

<div class="card mb-3">
                <div class="row no-gutters">
                <div class="col-md-8">
                    <div class="card-body">
                    <a class="card-author" href="{% url 'profile' post.author.username %}">{{ post.author }}<a>
                    <p class="card-content" id="post-content-{{ post.id }}">{{ post.content }}</p>
                    <p class="card-datetime">{{ post.datetime }}</p>
                    {% if request.user == post.author %}
                        <button class="btn btn-sm btn-outline-primary" id="edit-post-btn-{{ post.id }}">Edit</button>
                    {% endif %}