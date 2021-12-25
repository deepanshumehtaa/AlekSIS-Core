import pytest

from aleksis.core.models import Group

pytestmark = pytest.mark.django_db


def test_child_groups_recursive():
    g_1st_grade = Group.objects.create(name="1st grade")
    g_1a = Group.objects.create(name="1a")
    g_1b = Group.objects.create(name="1b")
    g_2nd_grade = Group.objects.create(name="2nd grade")
    g_2a = Group.objects.create(name="2a")
    g_2b = Group.objects.create(name="2b")
    g_2c = Group.objects.create(name="2c")
    g_2nd_grade_french = Group.objects.create(name="2nd grade French")

    g_1a.parent_groups.set([g_1st_grade])
    g_1b.parent_groups.set([g_1st_grade])
    g_2a.parent_groups.set([g_2nd_grade])
    g_2b.parent_groups.set([g_2nd_grade])
    g_2c.parent_groups.set([g_2nd_grade])
    g_2nd_grade_french.parent_groups.set([g_2b, g_2c])

    assert g_2nd_grade_french in g_2nd_grade.child_groups_recursive
    assert g_2nd_grade_french in g_2b.child_groups_recursive
    assert g_2nd_grade_french in g_2c.child_groups_recursive
    assert g_2nd_grade_french not in g_2a.child_groups_recursive
    assert g_2nd_grade_french not in g_1st_grade.child_groups_recursive


def test_parent_groups_recursive():
    g_1st_grade = Group.objects.create(name="1st grade")
    g_1a = Group.objects.create(name="1a")
    g_1b = Group.objects.create(name="1b")
    g_2nd_grade = Group.objects.create(name="2nd grade")
    g_2a = Group.objects.create(name="2a")
    g_2b = Group.objects.create(name="2b")
    g_2c = Group.objects.create(name="2c")
    g_2nd_grade_french = Group.objects.create(name="2nd grade French")

    g_1a.parent_groups.set([g_1st_grade])
    g_1b.parent_groups.set([g_1st_grade])
    g_2a.parent_groups.set([g_2nd_grade])
    g_2b.parent_groups.set([g_2nd_grade])
    g_2c.parent_groups.set([g_2nd_grade])
    g_2nd_grade_french.parent_groups.set([g_2b, g_2c])

    assert g_1st_grade in g_1a.parent_groups_recursive
    assert g_2nd_grade in g_2a.parent_groups_recursive
    assert g_2nd_grade in g_2nd_grade_french.parent_groups_recursive
    assert g_1st_grade not in g_2nd_grade_french.parent_groups_recursive
