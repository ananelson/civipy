## Getting Started
This is a brand-new project and code is subject to change at any time.

Install with `python3 -m pip install civipy`. If you are using a Python version
older than 3.11 and want to use `pyproject.toml` configuration, install with
`python3 -m pip install civipy[pyproject]`.

## Configuration

Configure your credentials in environment variables, a `.civipy` file, or in
`pyproject.toml` in a `tools.civipy` section. By default CiviPy will read a `.civipy`
file anywhere in the current working directory up to your project root, or your
project's `pyproject.toml` file, or a `.civipy` file in the user's home folder.
Settings in environment variables will overwrite any file settings. Alternatively,
you can call `civipy.config.SETTINGS.init()` to set the configuration values.

| Setting                   | Environment Variable | `.civipy` File             | `pyproject.toml` File          |
|---------------------------|----------------------|----------------------------|--------------------------------|
|                           |                      |                            | `[tool.civipy]`                |
| Connection *(required)*   | `CIVI_REST_BASE`     | `rest_base=http://civi.py` | `rest-base = "http://civi.py"` |
| API Version               | `CIVI_API_VERSION`   | `api_version=4`            | `api-version = "4"`            |
| Access Token *(required)* | `CIVI_USER_KEY`      | `user_key=...`             | `user-key = "..."`             |
| Site Token *(required)*   | `CIVI_SITE_KEY`      | `site_key=...`             | `site-key = "..."`             |
| Log File                  | `CIVI_LOG_FILE`      | `log_file=/tmp/civipy.log` | `log-file = "/tmp/civipy.log"` |
| Log Level                 | `CIVI_LOG_LEVEL`     | `log_level=WARNING`        | `log-level = "WARNING"`        |
| Config File               | `CIVI_CONFIG`        |                            |                                |

### Connection
The Connection setting lets you specify the URL of your REST API, or the `cv` or
`drush` or `wp-cli` executable on your file system. If "http" is found in the setting,
the system will use http calls to the REST API. If the string "drush" is found, it
will use drush. If the string "wp" is found, it will use wp-cli. And if none of these
are found, it will attempt to call the cv command line API.

### API Version
Set to "3" to use the CiviCRM v3 API, or "4" (the default) to use the CiviCRM v4 API.

### Log File
To log to a file instead of the screen, set the Log File setting to the file path
you want to log to.

### Config File
You can specify in an environment variable either a directory to find a `.civipy`
configuration file in, or a file to read as a `.civipy` configuration file.

## Usage
There are class methods for retrieving and creating records and instance methods
for working with them.

```python
from civipy import CiviContact, CiviEmail

contact = CiviContact.action("get", primary_email="ana@ananelson.com")
email = CiviEmail.find_or_create(search_key=["contact_id", "email"], **kwargs)
contact.update(nick_name="Ana")
```

Each CiviCRM Entity is represented by a subclass of CiviCRMBase; if you need an entity
that is not in the project, you can easily add it by subclassing CiviCRMBase and naming
it the entity name prepended with "Civi", e.g.

```python
import civipy

class CiviNewEntity(civipy.CiviCRMBase):
    pass
```

Many CiviCRM Actions have a corresponding method (e.g. `get`, `create`), and there are
also a number of convenience methods which do more processing (e.g. `find_or_create`).

## Copyright & License
civipy Copyright &copy; 2020 Ana Nelson

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
