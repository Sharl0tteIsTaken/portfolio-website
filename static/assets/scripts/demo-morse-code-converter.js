$(document).ready(() => {
  const inputForm = $("#input-form")
  const terminal = $("#terminal-history")

  inputForm.on('submit', event => {
    event.preventDefault()
    $.ajax({
      type: 'POST',
      url: '/demo/morse-code-converter',
      data: inputForm.serialize(),
      success: () => {
        $.get("/demo/morse-code-converter/input-receive", html => {
          terminal.html(html)
          inputForm[0].reset()
        })
      }
    })
  })

  $("#user_input").on('keydown', function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault()
      $(this).closest("form").submit()
    }
  })
})
