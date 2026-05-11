const toggleAllSwitch = state => {
  document.querySelectorAll(".form-check-input")
    .forEach(element => {
      if (element.checked !== state) {
        element.checked = state
        element.dispatchEvent(new Event('change'))
      }
    }
  )
}

window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll(".cookie-banner ul .dropdown-item")
    .forEach(element => {
      element.addEventListener('click', click => {
        if (click.target.tagName !== "INPUT" && click.target.tagName !== "LABEL") {
          const checkbox = element.querySelector(".form-check-input")
          checkbox.checked = !checkbox.checked
          checkbox.dispatchEvent(new Event('change'))
        }
      })
    })

})
