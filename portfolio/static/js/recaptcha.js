function onloadCallback() {
  renderRecaptcha();
}

function renderRecaptcha() {
  const sitekeyElement = document.getElementById('recaptha_site_key');
  if (!sitekeyElement) {
    console.warn('reCAPTCHA site key not found in the document.');
    return;
  }
  const sitekey = JSON.parse(sitekeyElement.textContent);
  const recaptchaElement = document.getElementById('g-recaptcha');
  if (recaptchaElement) {
    grecaptcha.render(recaptchaElement, {sitekey});
  }
}

document.addEventListener('htmx:afterSwap', function (e) {
  // Re-initialize reCAPTCHA after content swap
  if (e.detail.pathInfo.responsePath === '/contact/') {
    renderRecaptcha();
  }
});
