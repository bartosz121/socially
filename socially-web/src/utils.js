import numeral from "numeral";

export const getCookie = (name) => {
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

export const formatNumberToDisplay = (value) => {
  let format = "0 a";

  if (1000 < value && value < 100000) {
    format = "0.0 a"
  }

  return numeral(value).format(format)
}

export const copyTextToClipboard = async (text) => {
  if ('clipboard' in navigator) {
    return await navigator.clipboard.writeText(text);
  } else {
    return document.execCommand('copy', true, text);
  }
}

export const getFormData = (event) => {
  const data = new FormData(event.currentTarget)
  return data;
}
