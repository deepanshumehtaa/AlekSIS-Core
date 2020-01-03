Changelog
=========

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


_`1.0a1`: https://edugit.org/Teckids/AlekSIS/AlekSIS/-/tags/1.0a1
_`1.0a2`: https://edugit.org/Teckids/AlekSIS/AlekSIS/-/tags/1.0a2
_`1.0a4`: https://edugit.org/Teckids/AlekSIS/AlekSIS/-/tags/1.0a4
