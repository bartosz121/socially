import { animateCSS, buildAbsoluteUrl } from "./utils.js"

// Copy post URL to clipboard
const postsShareMenuClipboard = document.querySelectorAll('.post-share-menu')
postsShareMenuClipboard.forEach(menu => {
  const copyBtn = menu.getElementsByClassName('copyUrl')[0]
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
