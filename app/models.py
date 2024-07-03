from django.db import models




class CustomUser(models.Model):
    code = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code)


class Test(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to='test_images')
    user = models.ManyToManyField(CustomUser, null=True, blank=True, related_name='user', verbose_name='Прошли тест')
    user_for = models.ManyToManyField(CustomUser, null=True, blank=True, verbose_name='Для кого тест')

    def __str__(self):
        return str(self.name)

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.question_text)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    valid = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.answer_text)
    

    