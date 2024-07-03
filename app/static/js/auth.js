if (localStorage.getItem('authLavrId')) {
    $('.topHeader-btn').after(`<button class="topHeader-btn exit">Выйти</button>`)
}


$('.exit').on('click', function() {
    localStorage.removeItem('lavrUserRole')
    localStorage.removeItem('authLavrId')
    window.location.replace('/')
})

$('.authFormBtn').click(function() {
    var code = $('.authFormField').val();

    $.ajax({
        url: '/auth_data',
        method: 'POST',
        data: {
            'code': code
        },
        success: function(response) {
            if (response.success) {
                window.location.replace('/')
                localStorage.setItem('lavrUserRole', 'user')
                localStorage.setItem('authLavrId', code)
            }
            else {
                alert('Такого пользователя не существует')
            }
            
        },
        error: function(xhr, errmsg, err) {
            alert('Какая-то ошибка')
            console.error(err)
        }
    });
});