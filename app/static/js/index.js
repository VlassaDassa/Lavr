if (localStorage.getItem('authLavrId')) {
    $('.topHeader-btn').after(`<button class="topHeader-btn exit">Выйти</button>`)
    }
    else {
    $('.topHeader-btn').after(`<a href="/auth" class="topHeader-btn">Войти</a>`)
}


$('.exit').on('click', function() {
    localStorage.removeItem('lavrUserRole')
    localStorage.removeItem('authLavrId')
    window.location.replace('/')
})

$(document).on('click', '.testItem', function() {
    user_id = localStorage.getItem('authLavrId')
    if (user_id) {
        var testId = $(this).attr('data-test-id');
        var questionNumber = $(this).attr('data-question-number');

        $.ajax({
            url: '/check_success_test',
            method: 'POST',
            data: {
                'code': localStorage.getItem('authLavrId'),
                'test_id': testId
            },
            success: function(response) {
                if (response.next) {
                    window.location.href = '/question/' + testId + '/' + questionNumber
                }
                else {
                    alert('Вы уже проходили этот тест')
                }
            },
            error: function(xhr, errmsg, err) {
                alert('Какая-то ошибка')
                console.error(err)
            }
        });
    }
    else {
        window.location.href = '/auth'
    }
})

// Закрыть отчёт
$('.closeReport').on('click', function() {
    $('.overlay').hide()
    $('.reportWrapper').hide()
    $('.reportWrapperData').hide()
})


// Открыть отчёт
$('.reportttt').on('click', function() {
    $('.overlay').show()
    $('.reportWrapper').show()
})


// Поиск
$('.inputBtn').on('click', function() {
    if ($('.reportInput').val().length > 0) {
        $.ajax({
            url: '/report_by_code',
            method: 'POST',
            data: {
                'code': $('.reportInput').val()
            },
            success: function(response) {
                if (response.success) {
                    // Перерисовка с новыми данными
                    renderReport(response.data, $('.reportInput').val())
                }
                else {
                    alert('Пользователь не найден')
                }
                
            },
            error: function(xhr, errmsg, err) {
                alert('Какая-то ошибка')
                console.error(err)
            }
        });
    }
    else {
        alert('Введите код')
    }
})


function renderReport(data, code) {
    $('.reportWrapper').hide()
    $('.reportWrapperData').show()

    $('.reportTitle').html(`Пользователь - ${code}`)

    $('.userTest').remove()
    if (data.tests[0] == 'Пройденных тестов нет') {
        data.tests.forEach((element) => {
            $('.successTestsTitle').after($(`<div class="userTest">${element}</div>`));
        })
    }
    else {
        data.tests.forEach((element) => {
            $('.successTestsTitle').after($(`<div class="userTest">${element[0]} - ${element[1]}%</div>`));
        })
    }
    

    $('.erorrCount').html(data['count_errors'])

    $('.questionsWithErrorItems').remove()
    data.questions_with_errors.forEach((element) => {
        $('.questionsWithErrorTitle').after($(`<div class="questionsWithErrorItems">${element}</div>`));
    })
    
}



// Показ только тех тестов, которые определены для пользователя
function displayAllowTests() {
    $('.testsRow').remove() 
    const code = localStorage.getItem('authLavrId')

    if (code) {
        $.ajax({
            url: '/get_allow_tests',
            method: 'POST',
            data: {
                'code': code,
            },
            success: function(response) {
                const tests = response.tests
                console.log(tests);
                tests.forEach(function(test) {
                    var testHtml = `
                        <div class="testsRow">
                            <button data-test-id="${test.id}" data-question-number="0" class="testItem">${test.name}</button>
                            <div class="testItem-imgWrapper">
                                <img src="${test.image}" class="testItem-img" />
                            </div>
                        </div>
                    `;
            
                    $('.testsWrapper').append(testHtml);
                })
            },
            error: function(xhr, errmsg, err) {
                alert('Какая-то ошибка')
                console.error(err)
            }
        });
    }

}

displayAllowTests()