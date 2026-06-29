// remove line breaks from text to better fit the table format
if (document.documentElement.getAttribute("lang") === "Traditional-Chinese") {
  document.querySelectorAll('[data-format="strip-br-zhtw"]').forEach(element => {
    element.textContent = element.textContent.replaceAll('\n', '')
  })
}
