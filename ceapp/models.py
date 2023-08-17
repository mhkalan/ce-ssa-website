from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username


class TA(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    teacher = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TAReport(models.Model):
    TA = models.ForeignKey(TA, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    report_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Report of {self.TA.name}'


class Member(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name


class SSA(models.Model):
    year = models.PositiveIntegerField()
    members = models.ManyToManyField(Member)

    def __str__(self):
        return f"Company {self.year}"


class QuestionText(models.Model):
    text = models.CharField(max_length=500)
    questionNumber = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.questionNumber} -----> {self.text}'


class QuestionOption(models.Model):
    optionText = models.CharField(max_length=255)
    optionPlace = models.IntegerField()
    question = models.ForeignKey(QuestionText, on_delete=models.CASCADE)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question.questionNumber} ---- {self.optionPlace}'


class Poll(models.Model):
    person = models.ForeignKey(TA, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionText, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.person.name} --> {self.question.text}'
