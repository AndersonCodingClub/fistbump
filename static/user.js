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
            window.location.reload();
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
            window.location.reload();
        }
    });
}

function openStatModal(modalType) {
    let data;
    if (modalType === 'followers') {
        data = followers;
    } else {
        data = following;
    }

    const expandedContainer = document.createElement('div');
    expandedContainer.className = 'stat-modal-container';
    document.body.appendChild(expandedContainer);
    expandedContainer.style.display = 'flex';
    expandedContainer.innerHTML = '';

    const statModal = document.createElement('div');
    statModal.className = 'stat-modal';
    expandedContainer.appendChild(statModal);

    const titleRow = document.createElement('div');
    titleRow.className = 'modal-title-row';
    const followerTitle = document.createElement('p');
    followerTitle.className = 'modal-title';
    followerTitle.textContent = modalType.charAt(0).toUpperCase() + modalType.slice(1);
    titleRow.appendChild(followerTitle);
    statModal.appendChild(titleRow);

    data.forEach(function(row) {
        const modalRowUserID = row[0];
        const modalRowName = row[1];
        const modalRowUsername = row[2];

        const modalRow = document.createElement('div');
        modalRow.className = 'modal-row';

        const modalProfilePicture = document.createElement('img');
        modalProfilePicture.src = '/static/media/blank_pfp.jpeg';
        modalProfilePicture.className = 'modal-profile-picture';
        modalRow.appendChild(modalProfilePicture);

        const modalInfoContainer = document.createElement('div');
        modalInfoContainer.className = 'modal-info-container';

        const modalName = document.createElement('p');
        modalName.className = 'modal-name';
        modalName.textContent = modalRowName;

        const modalUsername = document.createElement('p');
        modalUsername.className = 'modal-username';
        modalUsername.textContent = modalRowUsername;

        modalInfoContainer.appendChild(modalName);
        modalInfoContainer.appendChild(modalUsername);

        const modalFollowButtonContainer = document.createElement('div');
        modalFollowButtonContainer.className = 'modal-follow-container';
        const followActionButton = document.createElement('button');
        followActionButton.setAttribute('data-following-id', modalRowUserID);

        if (viewerFollowers.includes(modalRowUserID)) {
            followActionButton.className = 'modal-unfollow-button';
            followActionButton.textContent = 'Unfollow';
        } else {
            followActionButton.className = 'modal-follow-button';
            followActionButton.textContent = 'Follow';
        }

        modalFollowButtonContainer.appendChild(followActionButton);

        modalRow.appendChild(modalInfoContainer);
        modalRow.appendChild(modalFollowButtonContainer);
        statModal.appendChild(modalRow);
    });

    expandedContainer.addEventListener('click', function(event) {
        if (event.target === this) {
            this.style.display = 'none';
        }
    });

    document.addEventListener('keydown', function(event){
        if (event.key === 'Escape' && expandedContainer.style.display !== 'none') {
            expandedContainer.style.display = 'none';
        }
    });
}

document.body.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal-follow-button')) {
        const followingID = event.target.getAttribute('data-following-id');
        followUser(viewerUserID, followingID);
    } else if (event.target.classList.contains('modal-unfollow-button')) {
        const followingID = event.target.getAttribute('data-following-id');
        unfollowUser(viewerUserID, followingID);
    }
});