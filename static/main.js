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

window.onload = () => {
  checkImages()
  createOnClickModalImages()
}

window.onresize = () => {
  checkImages()
}
