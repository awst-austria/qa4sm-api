=========
Changelog
=========

Version 0.3.0
=============
- Reuse HTTP connections and retry transient errors (connection errors,
  429, 5xx) with exponential backoff instead of 10 quick retries. Client
  errors (4xx) are no longer retried and POST requests are not re-sent once
  they reached the server.
- Close streamed download connections after use.
- CI: log in once per test class and limit parallel test jobs to avoid
  connection timeouts against the test server.
- Code styling with yapf; meta-package updated
- Added a CLI to list validation runs (`PR #5 <https://github.com/awst-austria/qa4sm-api/pull/5>`_)
- A bug was fixed that led to an error when using the "qa4sm validate" CLI command.

Version 0.2.0
=============
- Delete validation run via API
- Add pytest warning filters for expected authentication warnings
- Improve CLI documentation and fix docstrings
- Remove unnecessary tornado dependency (replaced with requests.exceptions.HTTPError)

Version 0.1.0
=============
- First version of Client API package
- Allows triggering validation runs and downloading results
- Used for the automated validation reports application
