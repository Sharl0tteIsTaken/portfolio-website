$(document).ready(function() {
    const InputForm = document.getElementById("input-form")
    const Terminal = document.getElementById("terminal-history")
    InputForm.onsubmit = function(event) {
        event.preventDefault();
        fetch("/demo/tic-tac-toe", {
        method: "GET"
        })
        .then(() => {
        fetch("/demo/tic-tac-toe/input-receive", {
            method: "GET"
        })
        .then(response => {
            return response.text();
        })
        .then(html =>{
            Terminal.innerHTML = html;
        })
        .then(InputForm.reset())
        })
    }
});

$(document).ready(function() {
    $('form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: "/demo/tic-tac-toe",
            data: $('form').serialize(),
            success: function() {
            $('user_input').val('');
            }
        });
    });
});
