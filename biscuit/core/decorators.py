from django.contrib.auth.decorators import user_passes_test


def student_required(function=None):
    actual_decorator = user_passes_test(lambda u: u.is_active and u.is_student)
    return actual_decorator(function)


def teacher_required(function=None):
    actual_decorator = user_passes_test(lambda u: u.is_active and u.is_teacher)
    return actual_decorator(function)
