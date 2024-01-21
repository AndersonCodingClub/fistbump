document.addEventListener('DOMContentLoaded', () => {
    bindGalleryImages();
});

function bindGalleryImages() {
    const expandedContainer = document.createElement('div');
    expandedContainer.className = 'expanded-image-container';
    document.body.appendChild(expandedContainer);

    document.querySelectorAll('.gallery-image').forEach(img => { 
        img.id = 'image-' + decodeURIComponent(img.src.split('_').pop().split('.')[0]);

        img.addEventListener('click', () => {
            expandedContainer.style.display = 'flex';
            expandedContainer.innerHTML = '';

            const creatorName = document.createElement('p');
            creatorName.className = 'creator-name';

            const creatorNameTag = `<a href="/user/${img.getAttribute('data-creator-id')}" style="font-weight: 600;" class="underline-hover">${img.getAttribute('data-creator')}</a>`;
            const matchNameTag = `<a href="/user/${img.getAttribute('data-match-id')}" style="font-weight: 600;" class="underline-hover">${img.getAttribute('data-match')}</a>`;

            creatorName.innerHTML = creatorNameTag + ' <span style="font-weight: 300;">&</span> ' + matchNameTag;
            expandedContainer.appendChild(creatorName);

            const datePublished = document.createElement('p');
            datePublished.className = 'date-published';
            datePublished.textContent = img.getAttribute('data-date-created');
            expandedContainer.appendChild(datePublished);

            const imageWrapper = document.createElement('div');
            imageWrapper.className = 'image-wrapper';
            expandedContainer.appendChild(imageWrapper);

            const expandedImg = img.cloneNode(true);
            expandedImg.className = 'expanded-image';
            expandedImg.style.maxWidth = img.naturalWidth + 'px';
            expandedImg.style.maxHeight = img.naturalHeight + 'px';
            expandedImg.style.borderRadius = '25px';

            imageWrapper.appendChild(expandedImg);
        });
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