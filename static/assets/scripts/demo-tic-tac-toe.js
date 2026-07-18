$(document).ready(() => {
    const inputForm = $("#input-form")
    const terminal = $("#terminal-history")

    inputForm.on('submit', event => {
        event.preventDefault()
        $.ajax({
            type: 'POST',
            url: '/demo/tic-tac-toe',
            data: inputForm.serialize(),
            success: () => {
                $.get("/demo/tic-tac-toe/input-receive", html => {
                    terminal.html(html)
                    inputForm[0].reset()
                })
            }
        })
    })
})
