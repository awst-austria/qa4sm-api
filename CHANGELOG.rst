=========
Changelog
=========

Version X.X.X
=============
-

Version 0.2.1
=============
- Code styling with yapf; meta-package updated
- Added a CLI to list validation runs (`PR #5 <https://github.com/awst-austria/qa4sm-api/pull/5>`_)
- A bug was fixed that led to an error when using the "qa4sm validate" CLI command.

Version 0.2
===========
- Delete validation run via API
- Add pytest warning filters for expected authentication warnings
- Improve CLI documentation and fix docstrings
- Remove unnecessary tornado dependency (replaced with requests.exceptions.HTTPError)

Version 0.1
===========
- First version of Client API package
- Allows triggering validation runs and downloading results
- Used for the automated validation reports application
