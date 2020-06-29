## Getting Started

This is a brand-new project and code is subject to change at any time.

Reading the source code is the primary documentation for now. There are also
some tests which document usage. Author is hanging out in CiviCRM mattermost.

Store your credentials in environment variables `CIVI_REST_BASE`,
`CIVI_USER_KEY`, `CIVI_SITE_KEY`.

To log to a file instead of the screen, set the `CIVIPY_LOG_FILE` environment
variable to the file path you want to log to.

You can either use subclasses of CiviCRMBase, e.g.

```python
    CiviContact._get(primary_email="ana@ananelson.com")
    CiviEmail.find_or_create(search_key_name=["contact_id", "email"], **kwargs)
```

Or directly call CiviCRMBase:

```python
    CiviCRMBase._get("Contact", primary_email="ana@ananelson.com")
```

Functions which directly call CiviCRM API methods, with a minimum of
processing, start with an underscore, e.g. `_get`. Convenience methods which do
more processing do not start with an underscore, e.g. `find_or_create`

## REST_BASE

The `CIVI_REST_BASE` setting lets you specify the URL of your REST API, OR it
can now refer to the `cv` or `drush` executable on your file system. If "http"
is found in CIVI_REST_BASE, the system will use http calls to the REST API. If
the string "drush" is found in CIVI_REST_BASE, it will use drush. And if
neither of these are found, it will attempt to call the cv command line API.

## Copyright & License

civipy Copyright (c) 2020 Ana Nelson

Licensed under the GPL v3

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

<https://www.gnu.org/licenses/gpl-3.0.txt>
