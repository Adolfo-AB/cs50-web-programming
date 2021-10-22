document.addEventListener('DOMContentLoaded', function() {

    console.log("DOM Content Loaded Successfully")
    // Toggle between views when clicking on the links
    document.querySelector('#all-posts').addEventListener('click', () => load_all_posts_view());

    // These 2 views are only available when the user is logged in
    try {
        document.querySelector('#following').addEventListener('click', () => load_following_posts_view());
        document.querySelector('#user-profile').addEventListener('click', () => load_profile_view());
    } catch (error) {
        console.log(error);
    }
  
    //document.querySelector('form').onsubmit = send;
  
    // By default, load the all posts view
    load_all_posts_view('all-posts-view');
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

        submitBtn = document.getElementById("submit-post-btn");
        submitBtn.addEventListener('click', () => {
            const content = document.getElementById("new-post-content").value;
            fetch('/save_post', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': ""//getCookie("csrftoken")"
                },
                body: bod = JSON.stringify({
                    content: content
                })
            })
            .then(response => response.json())
            .then(response => {})

    })
  }}

  function load_following_posts_view() {
  
    // Load following posts view
    document.querySelector('#following-posts-view').style.display = 'block';
    // Hide other views
    document.querySelector('#all-posts-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'none';
  }

  function load_profile_view() {
  
    // Load profile view
    document.querySelector('#profile-view').style.display = 'block';
    // Hide other views
    document.querySelector('#following-posts-view').style.display = 'none';
    document.querySelector('#all-posts-view').style.display = 'none';
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