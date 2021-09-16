const checkImages = () => {
  const images = document.querySelectorAll('.post-img');
  images.forEach(image => {
    if (image.width > 600 || image.height > 400) {
      image.style.width = '600px';
      image.style.height = '400px';
      image.style.objectFit = 'scale-down';
    }
  });
}

const createOnClickModalImages = () => {
  const modal = new bootstrap.Modal(document.getElementById('imageModal'))
  const modalImgTag = document.getElementById('modal-body-img');
  const images = document.querySelectorAll('.modal-img');
  images.forEach(image => {
    image.addEventListener('click', () => {
      modalImgTag.src = image.src;
      modal.show()
    })
  })
}

const createFollowBtnsEventListeners = () => {
  const followForms = document.querySelectorAll('.follow-form');
  followForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault()
      const csrfToken = form.elements.namedItem('csrfmiddlewaretoken').value
      const targetUserId = form.elements.namedItem("user-id").value
      const targetUserFollowersCount = document.getElementById(`followers-count-${targetUserId}`)
      const targetUserFollowBtn = document.getElementById(`follow-btn-${targetUserId}`);

      fetch(form.action, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
        .then(response => {
          return response.json()
        })
        .then(data => {
          if (data.value === 'follow') {
            targetUserFollowBtn.innerHTML = "<span>Following</span>"
            targetUserFollowBtn.classList = "btn btn-outline-primary following-btn"
          }
          else {
            targetUserFollowBtn.innerHTML = "Follow"
            targetUserFollowBtn.classList = "btn btn-primary follow-btn"
          }

          targetUserFollowersCount.textContent = data.followers
        })
        .catch(error => {
          console.error('Error:', error)
        })
    })
  })
}

window.onload = () => {
  checkImages()
  createOnClickModalImages()
  createFollowBtnsEventListeners()
}
