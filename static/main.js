// https://animate.style/#javascript
const animateCSS = (element, animation, makeHidden = false, prefix = 'animate__') =>
  // We create a Promise and return it
  new Promise((resolve, reject) => {
    const animationName = `${prefix}${animation}`;

    element.classList.add(`${prefix}animated`, animationName);

    // When the animation ends, we clean the classes and resolve the Promise
    function handleAnimationEnd(event) {
      event.stopPropagation();
      element.classList.remove(`${prefix}animated`, animationName);
      if (makeHidden) {
        element.style.display = 'none';
      }
      resolve('Animation ended');
    }

    element.addEventListener('animationend', handleAnimationEnd, { once: true });
  });

const buildAbsoluteUrl = (path) => {
  return window.location.protocol + '//' + window.location.host + path
}

const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const likePost = (postId) => {
  let likeContainer = document.getElementById(`like-container-post-${postId}`)
  let likeCount = document.getElementById(`like-count-post-${postId}`)
  let likeIcon = document.getElementById(`like-icon-${postId}`)

  fetch(`${buildAbsoluteUrl("")}/handlelike/${postId}`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": `${getCookie('csrftoken')}`,
    },
  })
    .then((response) => {
      if (response.redirected) {
        window.location.replace(response.url)
      }
      return response.json()
    })
    .then((data) => {
      if (data.value === "like") {
        likeContainer.classList.add("liked")
        likeIcon.classList = "bi bi-heart-fill"
        animateCSS(likeContainer, "heartBeat")
      } else if (data.value === "dislike") {
        likeContainer.classList.remove("liked")
        likeIcon.className = "bi bi-heart"
        animateCSS(likeContainer, "flash")
      }

      if (likeCount !== null) {
        // likeCount may be null in post detail if there are no likes yet
        if (data.likes > 0) {
          likeCount.innerHTML = data.likes
        } else {
          likeCount.innerHTML = "&nbsp;"
        }
      }
    })
    .catch((error) => {
      // mute error if request redirected to login
      if (!(error instanceof DOMException)) {
        console.error("Error:", error)
      }
    });
}

const deletePost = (postId, redirect = false) => {
  const postDiv = document.getElementById(`post-${postId}`);

  let url = buildAbsoluteUrl(`/posts/delete/${postId}`);
  if (redirect) {
    url += '?redirect=True'
  }

  fetch(url, {
    method: "DELETE",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": `${getCookie('csrftoken')}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      animateCSS(postDiv, "fadeOutLeft", true);
      if (data.redirect) {
        window.location.href = buildAbsoluteUrl("/");
      }
    })
    .catch((err) => console.error(err));
}

const copyUrlPost = (postId) => {
  let animateTarget = document.getElementById(`icon-arrow-${postId}`)
  navigator.clipboard.writeText(buildAbsoluteUrl(`/posts/${postId}`))
    .then(() => {
      animateCSS(animateTarget, 'flip')
    })
    .catch(err => {
      console.error(err)
    })
}

const imageModal = (imgUrl) => {
  const modal = new bootstrap.Modal(document.getElementById('imageModal'))
  const modalImgTag = document.getElementById('modal-body-img');
  modalImgTag.src = imgUrl;
  modal.show()
}

// TODO
// - post detail js functions - same as in normal post
// - follow buttons in suggestions - js function
// - profile page, setup htmx to work there and image modal