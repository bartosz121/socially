// https://animate.style/#javascript
const animateCSS = (element, animation, prefix = 'animate__') =>
  // We create a Promise and return it
  new Promise((resolve, reject) => {
    const animationName = `${prefix}${animation}`;

    element.classList.add(`${prefix}animated`, animationName);

    // When the animation ends, we clean the classes and resolve the Promise
    function handleAnimationEnd(event) {
      event.stopPropagation();
      element.classList.remove(`${prefix}animated`, animationName);
      resolve('Animation ended');
    }

    element.addEventListener('animationend', handleAnimationEnd, { once: true });
  });

const abbreviateNumber = (number) => {
  if (number > 999) {
    return (number / 1000).toFixed(1) + 'k';
  }
  return number;
}

const buildAbsoluteUrl = (path) => {
  return window.location.protocol + '//' + window.location.host + path
}

// Copy post URL to clipboard
const postsShareMenuClipboard = document.querySelectorAll('.post-share-menu')
postsShareMenuClipboard.forEach(menu => {
  copyBtn = menu.getElementsByClassName('copyUrl')[0]
  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(buildAbsoluteUrl(menu.children.namedItem('post-url').value))
      .then(() => {
        animateCSS(menu.parentElement, 'flip')
      })
      .catch(err => {
        console.error(err)
      })
  })
})

// Like
const likeForms = document.querySelectorAll('.like-form')

likeForms.forEach(form => {
  form.addEventListener('submit', (e) => {
    e.preventDefault()

    const postId = form.elements.namedItem("post-id").value
    const likeContainer = document.getElementById(`like-container-post-${postId}`)
    const likeIcon = document.getElementById(`like-icon-${postId}`)
    const likeCount = document.getElementById(`like-count-post-${postId}`)
    const csrfToken = form.elements.namedItem('csrfmiddlewaretoken').value

    fetch(form.action, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'X-CSRFToken': `${csrfToken}`,
      }
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
        if (data.value === 'like') {
          likeContainer.classList.add('liked')
          likeIcon.classList = "bi bi-heart-fill"
          animateCSS(likeContainer, 'heartBeat')
        }
        else if (data.value === 'dislike') {
          likeContainer.classList.remove('liked')
          likeIcon.className = "bi bi-heart"
          animateCSS(likeContainer, 'flash')
        }

        if (data.likes > 0) {
          likeCount.innerHTML = abbreviateNumber(data.likes)
        }
        else {
          likeCount.innerHTML = '&nbsp;'
        }
      }).catch((error) => {
        console.error('Error:', error)
      })
  })
})