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

window.onload = () => {
  createOnClickModalImages()
}
