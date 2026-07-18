// remove line breaks from text to better fit the table format
$(document).ready(() => {
  if ($('html').attr('lang') === "zh-TW") {
    $('[data-format="strip-br-zhtw"]').each(function() {
      this.textContent = this.textContent.replaceAll('\n', '')
    })
  }
})
