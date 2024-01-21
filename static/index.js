let currentFeedType = feedType;
console.log(currentFeedType);
let globalToggleButton = document.getElementById('global-toggle');
let fypToggleButton = document.getElementById('fyp-toggle');

document.addEventListener('DOMContentLoaded', () => {
    if (currentFeedType === 'global') {
        globalToggleButton.classList.add('active');
    } else {
        fypToggleButton.classList.add('active');
    }
});

function switchFeed(newFeedType) {
    if (currentFeedType !== newFeedType) {
        globalToggleButton.classList.toggle('active');
        fypToggleButton.classList.toggle('active');

        currentFeedType = newFeedType;

        if (currentFeedType === 'global') {
            window.location.href = '/?feed-type=global'
        } else {
            window.location.href = '/?feed-type=fyp'
        }
    }
}