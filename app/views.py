import random
from django.shortcuts import get_object_or_404, render
from django.http import Http404, JsonResponse
from .models import Test, Answer, CustomUser, Question
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count




def main_page(request):
    tests = Test.objects.all()

    return render(request, 'index.html', context={'tests': tests})

@csrf_exempt
def get_allow_tests(request):
    code = request.POST.get('code', None)
    user = get_object_or_404(CustomUser, code=code)
    tests = (Test.objects.filter(user=user) | Test.objects.filter(user_for=user)).distinct()
    tests_data = [{'id': test.id, 'name': test.name, 'image': tests[0].image.url} for test in tests]
    return JsonResponse({'tests': tests_data}, safe=False)


def auth_page(request):
    return render(request, 'auth.html')


@csrf_exempt
def auth_data(request):
    code = request.POST.get('code', None)
    try:
        CustomUser.objects.get(code=code)
    except:
        return JsonResponse({'response': code, 'success': False})

    return JsonResponse({'response': code, 'success': True})


@csrf_exempt
def save_user_answer(request):
    user_id = request.POST.get('user_id', None)
    answer_id = request.POST.get('answer_id', None)

    user = CustomUser.objects.get(code=user_id)
    answer = Answer.objects.get(id=answer_id)
    answer.user = user
    answer.save()
        
    return JsonResponse({'response': 'success'})


@csrf_exempt
def save_user_test(request):
    user_id = request.POST.get('userId', None)
    test_id = request.POST.get('testId', None)

    user = CustomUser.objects.get(code=user_id)
    test = Test.objects.get(id=test_id)
    test.user.set([user])

    test = Test.objects.get(id=test_id)
    questions = test.question_set.all()
    all_answers = [answer for question in questions for answer in question.answer_set.all()]
    valid_answers = [answer for answer in all_answers if answer.valid]
    len_valid_answers = len(valid_answers)
    len_user_valid_answers = len([i for i in valid_answers if i.user == user])

    # Процент правильных ответов
    percentage = (len_user_valid_answers / len_valid_answers) * 100
    score = ''
    if percentage >= 70:
        score = "Отлично, вы справились с тестом!"
    elif percentage >= 50:
        score = "Получился средний результат, вам есть куда расти!"
    else:
        score = "Плохой результат, вам стоит углубиться в эту тему :("

    # Вопросы в которых была ошибка
    invalid_question = []
    for question in questions:
        answers = question.answer_set.filter(user=user, valid=False)
        if answers.exists():
            invalid_question.append(question)

    data = {
        'percentage': percentage,
        'score': score,
        'invalid_question': [i.question_text for i in invalid_question]
    }

    return JsonResponse(data) 
    

def get_shuffled_question_ids(test):
    questions = list(test.question_set.all())
    random.shuffle(questions)
    return [q.id for q in questions]

def question_page(request, id, question_number):
    test = get_object_or_404(Test, id=id)

    if 'shuffled_questions' not in request.session or request.session['test_id'] != id:
        shuffled_question_ids = get_shuffled_question_ids(test)
        request.session['shuffled_questions'] = shuffled_question_ids
        request.session['test_id'] = id
    else:
        shuffled_question_ids = request.session['shuffled_questions']

    question_number = int(question_number)

    if question_number >= len(shuffled_question_ids):
        raise Http404("Question does not exist")

    question_id = shuffled_question_ids[question_number]
    question = get_object_or_404(Question, id=question_id)
    answers = question.answer_set.all()

    next_question = question_number + 1 < len(shuffled_question_ids)

    if question_number == 19:
        next_question = False

    context = {
        'answers': answers,
        'question': question,
        'question_number': question_number + 1,
        'next_question': next_question,
        'test_id': id,
    }

    return render(request, 'question.html', context=context)


@csrf_exempt
def report_by_code(request):
    user_code = request.POST.get('code', None)
    try:
        user = CustomUser.objects.get(code=user_code)
    except:
        return JsonResponse({'success': False})
    else:
        data = {
            'tests': ['Пройденных тестов нет'],
            'count_errors': 0,
            'questions_with_errors': ['Таких вопросов нет']
        }

        # Тест и процент прохождения
        tests = Test.objects.filter(user=user)
        all_answers = Answer.objects.filter(question__test__in=tests, user=user)
        valid_answers_per_test = all_answers.filter(valid=True).values('question__test').annotate(valid_count=Count('id'))
        total_answers_per_test = all_answers.values('question__test').annotate(total_count=Count('id'))
        percentages = {}
        for test_data in total_answers_per_test:
            test_id = test_data['question__test']
            total_count = test_data['total_count']
            valid_count = next((item['valid_count'] for item in valid_answers_per_test if item['question__test'] == test_id), 0)
            percentage = (valid_count / total_count) * 100 if total_count > 0 else 0
            percentages[test_id] = percentage
        if tests:
            data['tests'].pop(0)
            for test in tests:
                percentage = percentages.get(test.id, 0)
                data['tests'].append([test.name, percentage])
            

        # Количество ошибок
        data['count_errors'] = Answer.objects.filter(user=user, valid=False).count()
        
        # Вопросы с ошибками
        questions_with_invalid_answers = Question.objects.filter(answer__valid=False, answer__user=user).distinct()
        if questions_with_invalid_answers:
            data['questions_with_errors'] = [i.question_text for i in questions_with_invalid_answers]

        return JsonResponse({'success': True, 'data': data})


@csrf_exempt
def check_success_test(request):
    user_code = request.POST.get('code', None)
    test_id = request.POST.get('test_id', None)
    user = CustomUser.objects.get(code=user_code)
    test = Test.objects.get(id=test_id)

    if user in test.user.all():
        return JsonResponse({'next': False})
    
    return JsonResponse({'next': True})
    

    



