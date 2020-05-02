Changelog
=========

`2.0a2`_
--------

New features
~~~~~~~~~~~~

* Add frontend-ased announcement management
* Auto-create Person on User creation
* Generel LDAP import/export interface
* Select primary group if unset
* Support multiple recipient object for one announcement
* Mich-Seite
* Add support for defining group types
* Add description to Person
* Add age_at method and age property
* Synchronise AlekSIS groups with Django groups
* Add celery worker celery-beat worker and celery broker to docker-compose.yml
* Re-add django-dbbackup
* Global search
* Add license information page
* Roles and permissions
* User preferences
* Additional fields for people per group
* Support global permission flags by LDAP group
* Remove legacy multi-tenant support
* Generalise announcements
* Allow custom menu entries (e.g. in footer)
* New logo for AlekSIS
* Two factor authentication with Yubikey or OTP

Minor changes
~~~~~~~~~~~~~

* Add some CSS helper classes for colours
* Show announcements on dashboard
* Mandate use of AlekSIS base model
* Make short_name for group optional
* Drop import_ref field(s)
* Generalised live loading of widgets for dashboard
* Turn into installable web app

Bug fixes
~~~~~~~~~

* DateTimeField Announcement.valid_from received a naive datetime
* Enable SASS processor in production
* Fix too short fields
* Load select2 externally

`2.0a1`_
--------

New features
~~~~~~~~~~~~

* Migrate to materialize.css
* Dashboard
* Notifications via SMS (Twilio), Email or on the dashboard
* Admin interface
* Devs: Background Tasks with Celery
* Turn into installable PWA

Minor changes
~~~~~~~~~~~~~

* Customisable save_button template
* Redesign error pages

Bug fixes
~~~~~~~~~

* setup_data no longer forces database connection

`1.0a4`_
--------

New features
~~~~~~~~~~~~

* Two-factor authentication with TOTP (Google Authenticator), Yubikey, SMS
  and phone call.
* Devs: CRUDMixin provides a crud_event relation that returns all CRUD
  events for an object

`1.0a2`_
--------

New features
~~~~~~~~~~~~

* Devs: Add ExtensibleModel to allow injection of methods and properties into models.


`1.0a1`_
--------

New features
~~~~~~~~~~~~

* Devs: Add API to get an audit trail for any school-related object
* Devs: Provide template snippet to display an audit trail
* Devs: Provide base template for views that allow browsing back/forth
* Add management command and Cron job for full backups
* Add system status overview page
* Allow enabling and disabling maintenance mode from frontend
* Allow editing the dates of the current school term
* Add logo to school information
* Allow editing school information
* Ensure all actions are reverted if something fails (atomic requests)

Bugfixes
~~~~~~~~

* Only show active persons in group and persons views
* Silence KeyError in get_dict template tag

Minor changes
~~~~~~~~~~~~~

* Use bootstrap buttons everywhere


_`1.0a1`: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a1
_`1.0a2`: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a2
_`1.0a4`: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/1.0a4
_`2.0a1`: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0a1
_`2.0a2`: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0a2
