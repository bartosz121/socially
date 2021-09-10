window.onload = () => {
  const alerts = document.querySelectorAll('.alert,.invalid-feedback')
  if (alerts.length === 0) {
    console.log('no alerts')
    return;
  }
  console.log('alerts present')
  Array.from(alerts).forEach(alert => {
    let collapseElement = alert.parentElement;
    while (!collapseElement.classList.contains('collapse')) {
      collapseElement = collapseElement.parentElement
      // failsafe if something goes wrong
      if (collapseElement.localName === 'body') {
        return;
      }
    }
    collapseElement.classList.add('show')
  });
}
