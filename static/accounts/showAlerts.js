window.onload = () => {
  const alerts = document.querySelectorAll('.alert,.invalid-feedback')
  if (alerts.length === 0) {
    return;
  }
  Array.from(alerts).forEach(alert => {
    let element = alert.parentElement;
    while (!element.classList.contains('collapse')) {
      element = element.parentElement
      // failsafe if something goes wrong
      if (element.localName === 'body') {
        return;
      }
    }
    element.classList.add('show')
  });
}
