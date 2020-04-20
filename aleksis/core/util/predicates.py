from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Model
from django.http import HttpRequest
from guardian.backends import ObjectPermissionBackend
from guardian.shortcuts import get_objects_for_user
from rules import predicate

from .core_helpers import has_person as has_person_helper

# 1. Global permissions (view all, add, change all, delete all)
# 2. Object permissions (view, change, delete)
# 3. Rules


def permission_validator(request: HttpRequest, perm: str) -> bool:
    """ Checks whether the request user has a permission """

    if request.user:
        return request.user.has_perm(perm)
    return False


def check_global_permission(user: User, perm: str) -> bool:
    """ Checks whether a user has a global permission """

    return ModelBackend().has_perm(user, perm)


def check_object_permission(user: User, perm: str, obj: Model) -> bool:
    """ Checks whether a user has a permission on a object """

    return ObjectPermissionBackend().has_perm(user, perm, obj)


def has_global_perm(perm: str):
    """ Builds predicate which checks whether a user has a global permission """

    name = "has_global_perm:{}".format(perm)

    @predicate(name)
    def fn(user: User) -> bool:
        return check_global_permission(user, perm)

    return fn


def has_object_perm(perm: str):
    """ Builds predicate which checks whether a user has a permission on a object """

    name = "has_global_perm:{}".format(perm)

    @predicate(name)
    def fn(user: User, obj: Model) -> bool:
        if not obj:
            return False
        return check_object_permission(user, perm, obj)

    return fn


def has_any_object(perm: str, klass):
    """ Build predicate which checks whether a user has access to objects with the provided permission """

    name = "has_any_object:{}".format(perm)

    @predicate(name)
    def fn(user: User) -> bool:
        objs = get_objects_for_user(user, perm, klass)
        return len(objs) > 0

    return fn


@predicate
def has_person(user: User) -> bool:
    """ Predicate which checks whether a user has a linked person """

    return has_person_helper(user)


@predicate
def is_current_person(user: User, obj: Model) -> bool:
    """ Predicate which checks if the provided object is the person linked to the user object """

    return user.person == obj
