import { animateCSS, buildAbsoluteUrl, abbreviateNumber } from "./utils.js"

const csrfToken = document.getElementById('csrfToken').value;

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

// Delete post
const deleteForms = document.querySelectorAll('.delete-post-form')
// TODO GRAB CSRF TOKEN ONCE
deleteForms.forEach(form => {
  form.addEventListener('submit', (e) => {
    e.preventDefault()
    const postId = form.elements.namedItem('post-id').value
    const postDiv = document.getElementById(`post-${postId}`)

    fetch(form.action, {
      method: 'DELETE',
      credentials: 'same-origin',
      headers: {
        'X-CSRFToken': `${csrfToken}`,
      }
    })
      .then(response => response.json())
      .then(data => {
        animateCSS(postDiv, 'fadeOutLeft', true)
        if (data.redirect) {
          window.location.href = buildAbsoluteUrl("/")
        }
      })
      .catch(err => console.error(err))
  })
})