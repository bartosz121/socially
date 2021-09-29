// https://animate.style/#javascript
export const animateCSS = (element, animation, makeHidden = false, prefix = 'animate__') =>
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

export const abbreviateNumber = (number) => {
  if (number > 999) {
    return (number / 1000).toFixed(1) + 'k';
  }
  return number;
}

export const buildAbsoluteUrl = (path) => {
  return window.location.protocol + '//' + window.location.host + path
}