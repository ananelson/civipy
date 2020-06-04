## Getting Started

This is a brand-new project and code is subject to change at any time.

Reading the source code is the primary documentation for now.

Store your credentails in environment variables `CIVI_REST_BASE`,
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

## Copyright & License

civipy Copyright (c) 2020 Ana Nelson

Licnsed under the GPL v3

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
