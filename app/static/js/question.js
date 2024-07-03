if (localStorage.getItem('authLavrId')) {
    $('.topHeader-btn').after(`<button class="topHeader-btn exit">Выйти</button>`)
}


$('.exit').on('click', function() {
    localStorage.removeItem('lavrUserRole')
    localStorage.removeItem('authLavrId')
    window.location.replace('/')
})


// Галочка при нажатии на ответ
$('.variantRow').on('click', function() {
    $('.variantCheck').removeClass('check');
    $(this).find('.variantCheck').addClass('check');
});


// Переход к следующему вопросу
$('.nextQuestion').on('click', function() {
    if ($('.check').length <= 0) {
        alert('Чтобы продолжить тест, выберите вариант')
    }
    else {
        var testId = $(this).data('test-id');
        var questionNumber = $(this).data('question-number');
        window.location.href[-1] = questionNumber

        var newUrl = window.location.href.replace(/\/(\d+)\/(\d+)$/, '/' + testId + '/' + questionNumber);
        send_answer_to_server(newUrl)
    }
});


// Отправка ответа на сервер
function send_answer_to_server(newUrl=false) {
    $.ajax({
        url: '/save_user_answer',
        method: 'POST',
        data: {
            'user_id': localStorage.getItem('authLavrId'),
            'answer_id': $('.check').parent().find('.variantText').attr('data-answer-id'),
        },
        success: function(response) {
            if (newUrl) {window.location.href = newUrl;}
        },
        error: function(xhr, errmsg, err) {
            console.error(err)
            alert('Какая-то ошибка')
        }
    });
}



// Модальное окно для показа результатов теста
function createModal(data) {
    var modal = $('<div>').addClass('modal');
    var modalContent = $('<div>').addClass('modal-content');
    var closeBtn = $('<span>').addClass('close').html('&times;');
    // var score = $('<p>').attr('id', 'score').text(data.score + ' - ' + data.percentage);
    var invalidQuestionsList = $('<ul>').attr('id', 'invalidQuestions');
    
    data.invalid_question.forEach(function(question) {
      invalidQuestionsList.append($('<li>').text(question));
    });
    
    if (data.invalid_question.length > 0) {
        modalContent.append(closeBtn, $('<p>').text('Неверные вопросы:'), invalidQuestionsList);
    }
    else {
        modalContent.append(closeBtn);
    }
    
    modal.append(modalContent);
    
    $('body').append(modal);
    
    $('.close').click(function() {
      $('.modal').remove();
      window.location.replace('/');
    });
}

// Отправка результатов
$('.sendTest').on('click', function() {
    if ($('.check').length <= 0) {
        alert('Чтобы отправить тест, выберите вариант')
    }
    else {
       send_answer_to_server()

       // Завершение теста
       let testId = window.location.href.split('/').slice(-2, -1)[0];
       let userId = localStorage.getItem('authLavrId')

       setTimeout(() => {
            $.ajax({
                url: '/save_user_test',
                method: 'POST',
                data: {
                    'userId': userId,
                    'testId': testId,
                },
                success: function(response) {
                    // Результаты тестирования
                    createModal(response)
                },
                error: function(xhr, errmsg, err) {
                    console.error(err)
                    alert('Какая-то ошибка')
                }
            });
       }, 500)
       
    }
});