document.addEventListener('DOMContentLoaded', function() {

    console.log("DOM Content Loaded Successfully")
    // Toggle between views when clicking on the links
    
    // By default, load the all posts view
    load_all_posts_view();

    document.querySelector('#all-posts').addEventListener('click', () => load_all_posts_view());

    // These 2 views are only available when the user is logged in
    try {
        document.querySelector('#following').addEventListener('click', () => load_following_posts_view());
        const userProfileLink = document.querySelector('#user-profile')
        const username = userProfileLink.innerHTML;
        console.log(username);
        userProfileLink.addEventListener('click', () => load_profile_view(username));
    } catch (error) {
        console.log(error);
    }
  });

  function load_all_posts_view() {
  
    // Load all posts view
    document.querySelector('#all-posts-view').style.display = 'block';
    // Hide other views
    document.querySelector('#following-posts-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'none';

    // If the user is logged in, create the New Post components
    if (document.getElementById('log-out')) {
      console.log("User logged in.")
      create_new_post_components();

      document.querySelector('#submit-post-btn').disabled = true;
      document.querySelector('#new-post-content').onkeyup = () => {
        if (document.querySelector('#new-post-content').value.length >0) {
            document.querySelector('#submit-post-btn').disabled = false;
        } else {
            document.querySelector('#submit-post-btn').disabled = true
        }
      }

      submitBtn = document.getElementById("submit-post-btn");
      submitBtn.addEventListener('click', () => {
        console.log("New Post button clicked.")
        const content = document.getElementById("new-post-content").value;
        console.log(content)
        fetch('/add', {
          method: 'POST',
          body: JSON.stringify({
            content: content
          })
        })
      })
    }
    get_posts("all");
}

  function load_following_posts_view() {
    // Hide other views
    document.querySelector('#all-posts-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'none';
  
    // Load following posts view
    document.querySelector('#following-posts-view').style.display = 'block';

    get_posts("following");
    
  }

  function load_profile_view(username) {
  
    // Load profile view
    document.querySelector('#profile-view').style.display = 'block';

    // Hide other views
    document.querySelector('#following-posts-view').style.display = 'none';
    document.querySelector('#all-posts-view').style.display = 'none';
    
    console.log("Profile loaded successfully")
    

    document.querySelector('#profile-header').innerHTML = `User Profile: <strong>${username}</strong>`;

    console.log("Before generating posts.")
    const parent = document.querySelector("#profile-posts-container")
    while (parent.firstChild) {
      parent.removeChild(parent.lastChild);
    }
    get_profile_posts(username);

    if ((document.querySelector("#follow-btn") == null) && (document.querySelector("#followers-p") == null)) {
      const followBtn = document.createElement('button');
      followBtn.id = "follow-btn";
      followBtn.className = "btn btn-primary";

      const numberFollowers = document.createElement('p');
      numberFollowers.id = "followers-p";
      const numberFollowing = document.createElement('p');
      numberFollowing.id = "following-p";
      
      fetch(`/profile/${username}/getprofiledata`)
      .then(response => response.json())
      .then(response => {
        numberFollowers.innerHTML = `Followers: ${response.followers}`;
        numberFollowing.innerHTML = `Following: ${response.following}`;
        console.log(response)
      })


      fetch(`/profile/${username}/getstatus`)
      .then(response => response.json())
      .then(response => {
        if (response.follower) {
          followBtn.innerHTML = "Unfollow"
        } else {
          followBtn.innerHTML = "Follow"
        }
        
      })

      if ((document.getElementById('log-out')) 
      && (document.querySelector("#user-profile").innerHTML != document.querySelector(`#post-author-${username}`).innerHTML)) {
        document.querySelector('#follow-container').append(followBtn);
      }

      document.querySelector('#follow-container').append(numberFollowers);
      document.querySelector('#follow-container').append(numberFollowing);

      followBtn.addEventListener('click', () => update_follow_status(username))
    }

    console.log("After generating posts.")
  }

  async function update_follow_status(username) {
    fetch(`/profile/${username}/follow`)
    .then(response => response.json())
    .then(response => {
        console.log("Follow status updated successfully.");
        console.log(response);
        })
    .then(() => {
      const followBtn = document.querySelector("#follow-btn");
      fetch(`/profile/${username}/getstatus`)
    .then(response => response.json())
    .then(response => {
      if (response.follower) {
        followBtn.innerHTML = "Unfollow"
      } else {
        followBtn.innerHTML = "Follow"
      }
    })
    .then(() => {
      const numberFollowers = document.querySelector("#followers-p");
      const numberFollowing = document.querySelector("#following-p");
      fetch(`/profile/${username}/getprofiledata`)
      .then(response => response.json())
      .then(response => {
        numberFollowers.innerHTML = `Followers: ${response.followers}`;
        numberFollowing.innerHTML = `Following: ${response.following}`;
        console.log(response)
      })
    })
  })
}

  function create_new_post_components() {
    const container = document.createElement('div');
    container.className = "container";

    const header = document.createElement('h4');
    header.innerHTML = "New Post";
    container.append(header);

    const form = document.createElement('form');
    container.append(form);

    const formGroup = document.createElement('div');
    formGroup.className = "form-group";
    form.append(formGroup);

    const textArea = document.createElement('textarea');
    textArea.id = "new-post-content";
    textArea.className = "form-control";
    textArea.autofocus = "autofocus";
    textArea.cols = "20";
    textArea.rows = "4";
    textArea.placeholder = "What are you thinking about?";
    textArea.maxLength = "280";
    formGroup.append(textArea);

    const submit = document.createElement('input');
    submit.id = "submit-post-btn";
    submit.className = "btn btn-primary";
    submit.type = "submit";
    submit.value = "Post";
    form.append(submit);

    document.querySelector('#new-post').append(container);
  }

  function get_posts(page) {
    fetch(`/posts/${page}`)
    .then(response => response.json())
    .then(posts => {
        console.log("All posts fetched successfully.");
        console.log(posts);
        posts.forEach(post => load(post, page));
        });
  }

  function get_profile_posts(username) {
    console.log("Getting posts...")
    fetch(`/profile/${username}`)
    .then(response => response.json())
    .then(posts => {
        console.log("Profile posts fetched successfully.");
        console.log(posts);
        posts.forEach(post => load(post, "profile"));
        });
  }

  function load(post, page) {
    const cardDiv = document.createElement('div')
    cardDiv.className = "card mb-1"

    const rowDiv = document.createElement('div')
    rowDiv.className = "row no-gutter"
    cardDiv.append(rowDiv)

    const colDiv = document.createElement('div')
    colDiv.className = "col-md-11"
    rowDiv.append(colDiv)

    const cardBodyDiv = document.createElement('div')
    cardBodyDiv.className = "card-body"
    colDiv.append(cardBodyDiv)

    const postAuthor = document.createElement('a')
    postAuthor.id = `post-author-${post.author_username}`;
    postAuthor.className = "card-author";
    postAuthor.href = "#";
    postAuthor.innerHTML = post.author_username;
    postAuthor.addEventListener('click', () => load_profile_view(post.author_username));
    cardBodyDiv.append(postAuthor)

    const postContent = document.createElement('p')
    postContent.id = `post-content-${post.id}`
    postContent.className = "card-content"
    postContent.innerHTML = post.content
    cardBodyDiv.append(postContent)

    const postDateTime = document.createElement('p')
    postDateTime.className = "card-datetime"
    postDateTime.innerHTML = post.datetime
    cardBodyDiv.append(postDateTime)

    if (page === "all") {
      document.querySelector('#all-posts-container').append(cardDiv);
    } else if (page === "profile") {
      document.querySelector('#profile-posts-container').append(cardDiv);
    } else if (page === "following") {
      document.querySelector('#following-posts-container').append(cardDiv);
    }

  }
