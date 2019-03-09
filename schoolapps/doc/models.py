from django.db import models

# Create your models here.
class Teacher(models.Model):
    abbreviation = models.CharField(max_length=5, primary_key=True, unique=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=40)


class Certificate(models.Model):
    teacher = models.ForeignKey(to=Teacher.abbreviation, on_delete=models.CASCADE)
    subject = models.ForeignKey(to=Subject.abbreviation, on_delete=models.CASCADE)


class WorkingTime(models.Model):
    teacher = models.ForeignKey(to=Teacher.abbreviation)
    term = models.ForeignKey('Term', on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=5, decimal_places=1)
    


class Subject(models.Model):
    abbreviation = models.CharField(max_length=5, primary_key=True, unique=True)
    name = models.CharField(max_length=30)


class SubjectTitle(models.Model):
    subject_title = models.CharField(max_length=6, primary_key=True, unique=True)
    abbreviation = models.ForeignKey(to=Subject.abbreviation, on_delete=models.CASCADE)


class Course(models.Model):
    grade = models.CharField(max_length=6)
    group = models.CharField(max_length=6)
    subject_title = models.ForeignKey(to=SubjectTitle.subject_title, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=Teacher.abbreviation, on_delete=models.CASCADE)


class NoLessons(models.Model):
    day = models.DateField()
    reason = models.CharField(max_length=50)


class Schoolyear(models.Model):
    begin = models.DateField()
    end = models.DateField()


class Term(models.Model):
    begin = models.DateField()
    end = models.DateField()



