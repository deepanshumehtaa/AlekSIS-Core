Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`2.0a2`_ - 2020-05-04
--------

Added
~~~~~

* Frontend-ased announcement management.
* Auto-create Person on User creation.
* Select primary group by pattern if unset.
* Shortcut to personal information page.
* Support for defining group types.
* Add description to Person.
* age_at method and age property to Person.
* Synchronise AlekSIS groups with Django groups.
* Add celery worker, celery-beat worker and celery broker to docker-compose setup.
* Global search.
* License information page.
* Roles and permissions.
* User preferences.
* Additional fields for people per group.
* Support global permission flags by LDAP group.
* Persistent announcements.
* Custom menu entries (e.g. in footer).
* New logo for AlekSIS.
* Two factor authentication with Yubikey, OTP or SMS.
* Devs: Add ExtensibleModel to allow apps to add fields, properties.
* Devs: Support multiple recipient object for one announcement.

Changes
~~~~~~~

* Make short_name for group optional.
* Generalised live loading of widgets for dashboard.
* Devs: Add some CSS helper classes for colours.
* Devs: Mandate use of AlekSIS base model.
* Devs: Drop import_ref field(s); apps shold now define their own reference fields.

Fixed
~~~~~

* DateTimeField Announcement.valid_from received a naive datetime.
* Enable SASS processor in production.
* Fix too short fields.
* Load select2 locally.

`2.0a1`_ - 2020-02-01
---------------------

Added
~~~~~

* Migrate to MaterializeCSS.
* Dashboard.
* Notifications via SMS (Twilio), Email or on the dashboard.
* Admin interface.
* Turn into installable, progressive web app.
* Devs: Background Tasks with Celery.

Changed
~~~~~~~

* Customisable save_button template.
* Redesign error pages.

Fixed
~~~~~

* setup_data no longer forces database connection.

`1.0a4`_ - 2019-11-25
---------------------

Added
~~~~~

* Two-factor authentication with TOTP (Google Authenticator), Yubikey, SMS
  and phone call.
* Devs: CRUDMixin provides a crud_event relation that returns all CRUD
  events for an object.

`1.0a2`_ - 2019-11-11
---------------------

Added
~~~~~

* Devs: Add ExtensibleModel to allow injection of methods and properties into models.


`1.0a1`_ - 2019-09-17
---------------------

Added
~~~~~

* Devs: Add API to get an audit trail for any school-related object.
* Devs: Provide template snippet to display an audit trail.
* Devs: Provide base template for views that allow browsing back/forth.
* Add management command and Cron job for full backups.
* Add system status overview page.
* Allow enabling and disabling maintenance mode from frontend.
* Allow editing the dates of the current school term.
* Add logo to school information.
* Allow editing school information.
* Ensure all actions are reverted if something fails (atomic requests).

Fixed
~~~~~

* Only show active persons in group and persons views.
* Silence KeyError in get_dict template tag.
* Use bootstrap buttons everywhere.

.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

.. _1.0a1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a1
.. _1.0a2: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a2
.. _1.0a4: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a4
.. _2.0a1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0a1
.. _2.0a2: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0a2
.. _2.0b0: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0b0
