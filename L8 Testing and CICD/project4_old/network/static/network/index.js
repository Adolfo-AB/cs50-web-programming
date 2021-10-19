
document.addEventListener('DOMContentLoaded', function() {
    console.log("Content loaded")
    // Use "Edit" button to edit posts
    var buttons = document.querySelectorAll(".btn.btn-sm.btn-outline-primary")

    for (var i=buttons.length-1; i>=0; i--) {
        var btn = buttons[i]
        btn.addEventListener('click', () => {
            console.log(btn);
            console.log("Post edited");
            var postBody = btn.parentNode.children[0];
            console.log(postBody.innerHTML);
            btn.parentNode.children[0].innerHTML = "<strong>Pepe</strong>";
        })}})

/*
function edit_post() {
    console.log(buttons[i])
    console.log("Post edited")
    buttons[i].innerHTML = "<strong>Pepe</strong>";
    /*
    var postContentValue = postContent.innerHTML;

    const editableText = document.createElement('textarea');
    editableText.innerHTML = "pepepe";

    postContent.parentNode.replaceChild(editableText, postContent);
    */

