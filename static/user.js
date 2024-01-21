let followButton = document.getElementById('follow-button');

function followUser(followerID, followingID) {
    fetch('/follow', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "followerID": followerID, "followingID": followingID })
    }).then(response => {
        if(response.ok) {
            window.location.reload()
            followButton.classList.remove(...followButton.classList);
            followButton.classList.add("unfollow");
            followButton.onclick = () => unfollowUser(followerID, followingID);
        }
    });
}

function unfollowUser(followerID, followingID) {
    fetch('/unfollow', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "followerID": followerID, "followingID": followingID })
    }).then(response => {
        if(response.ok) {
            window.location.reload()
            followButton.classList.remove(...followButton.classList);
            followButton.classList.add("follow");
            followButton.onclick = () => followUser(followerID, followingID);
        }
    });
}