$(document).ready(function() {
    const InputForm = document.getElementById("input-form")
    const Terminal = document.getElementById("terminal-history")
    InputForm.onsubmit = function(event) {
        event.preventDefault();
        fetch("/demo/morse-code-converter", {
        method: "GET"
        })
        .then(() => {
        fetch("/demo/morse-code-converter/input-recieve", {
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
            url: '/demo/morse-code-converter',
            data: $('form').serialize(),
            success: function() {
            $('user_input').val('');
            }
        });
    });
});

$("#user_input").keypress(function (e) {
    if(e.which === 13 && !e.shiftKey) {
        e.preventDefault();
        $(this).closest("form").submit();
    }
});
