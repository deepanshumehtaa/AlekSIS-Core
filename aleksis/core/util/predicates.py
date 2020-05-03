from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Model
from django.http import HttpRequest

from guardian.backends import ObjectPermissionBackend
from guardian.shortcuts import get_objects_for_user
from rules import predicate

from ..models import Group
from .core_helpers import get_site_preferences
from .core_helpers import has_person as has_person_helper


def permission_validator(request: HttpRequest, perm: str) -> bool:
    """Checks whether the request user has a permission."""
    if request.user:
        return request.user.has_perm(perm)
    return False


def check_global_permission(user: User, perm: str) -> bool:
    """Checks whether a user has a global permission."""
    return ModelBackend().has_perm(user, perm)


def check_object_permission(user: User, perm: str, obj: Model) -> bool:
    """Checks whether a user has a permission on a object."""
    return ObjectPermissionBackend().has_perm(user, perm, obj)


def has_global_perm(perm: str):
    """Builds predicate which checks whether a user has a global permission."""
    name = f"has_global_perm:{perm}"

    @predicate(name)
    def fn(user: User) -> bool:
        return check_global_permission(user, perm)

    return fn


def has_object_perm(perm: str):
    """Builds predicate which checks whether a user has a permission on a object."""
    name = f"has_global_perm:{perm}"

    @predicate(name)
    def fn(user: User, obj: Model) -> bool:
        if not obj:
            return False
        return check_object_permission(user, perm, obj)

    return fn


def has_any_object(perm: str, klass):
    """
    Build predicate which checks whether a user has access to objects with the provided permission.
    """
    name = f"has_any_object:{perm}"

    @predicate(name)
    def fn(user: User) -> bool:
        objs = get_objects_for_user(user, perm, klass)
        return len(objs) > 0

    return fn


def check_site_preference(section: str, pref: str):
    """Builds predicate which checks the boolean value of a given site preference"""
    name = f"check_site_preference:{section}__{pref}"

    @predicate(name)
    def fn() -> bool:
        if isinstance(get_site_preferences()[f"{section}__{pref}"], bool):
            return get_site_preferences()[f"{section}__{pref}"]
        return False

    return fn


@predicate
def has_person(user: User) -> bool:
    """Predicate which checks whether a user has a linked person."""
    return has_person_helper(user)


@predicate
def is_current_person(user: User, obj: Model) -> bool:
    """Predicate which checks if the provided object is the person linked to the user object."""
    return user.person == obj


@predicate
def is_group_owner(user: User, group: Group) -> bool:
    """Predicate which checks if the user is a owner of the provided group."""
    return group.owners.filter(owners=user.person).exists()


@predicate
def is_notification_recipient(user: User, obj: Model) -> bool:
    """
    Predicate which checks whether the recipient of the
    notification a user wants to mark read is this user.
    """
    return user == obj.recipient.user
