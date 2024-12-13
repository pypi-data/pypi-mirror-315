====================
Breeze Email Reports
====================
The Breeze Church Management System (CHMS) is used by many churches to manage
their operations. Breeze has modules to support (not necessarily a complete list):

* A database of church members, with flexibility on data to keep on members
* Tracking giving, including pledges, and preparing giving statements
* Creating events, with volunteer management and attendance tracking
* Online giving
* Emails and texts to members
* Online forms

Breeze also has a network REST Application Programming Interface (API) that provides remote applications access
to a church's Breeze data. While the interface is pretty obtuse, the API
makes it possible to retrieve and update a church's data outside of
Breeze's normal web interface. The command-line
utilities in this package do not update any data, but they can be used to
email periodic reports on Breeze.

The current release includes two utilities. Each will mail a report to selected recipients
based on command parameters. Typically, you'd set up a system that automatically runs these periodically
(every week? day?). Any reasonable operating system has a way to
do that, but it's out of scope to describe details there. Best practice is to
create a python virtual environment and install this package there. Then your
periodic script should enter the virtual environment and run a command with
appropriate parameters.

There are currently two commands:

* ``email_profile_report`` emails a report detailing changes
  in your church's member database between runs.
* ``email_giver_report`` emails a report with details of who gave
  to a given set of funds for a range of dates.

Using these facilities requires some configuration to provide
the credentials needed to access the Breeze API and to allow
sending emails. Both of these are implemented in dependent packages,
but to make it easier for users some basic detail is included in the documentation.

See DOCUMENTATION_ for details on use how to set up and use these reports.

.. _DOCUMENTATION: https://github.com/dawillcox/breeze_email_reports/blob/main/DOCUMENTATION.rst
