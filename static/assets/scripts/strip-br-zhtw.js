// remove line breaks from text to better fit the table format
(() => {
  if (document.documentElement.getAttribute("lang") === "zh-TW") {
    document.querySelectorAll('[data-format="strip-br-zhtw"]').forEach(element => {
      element.textContent = element.textContent.replaceAll('\n', '')
    })
  }
})()
