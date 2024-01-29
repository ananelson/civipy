### 0.0.3 [pending release]

- Add CiviCRM v4 API usage and make it the default
- Drop allowing `CiviCRMBase` to be used directly (must subclass to access a CiviCRM entity)
- Update settings to automatically search for a `.civipy` or `pyproject.toml` file
- "Drop" Python 3.8 "support"

### 0.0.2 January 13, 2024

- Add `Contribution`, `ContributionRecur`, `Membership`, `Country`, and User Framework entities
- Replace `Exception` with package-specific exceptions
- Fix bug in HTTP request body structure
  - This worked in CiviCRM 3.3 on Drupal, but failed in CiviCRM 5.46.3 on WordPress.
The old behavior was consistent with the v3 API explorer in CiviCRM but not with
[the v3 REST API documentation](https://docs.civicrm.org/dev/en/latest/api/v3/usage/#rest).
- Make settings by environment variables optional, add options for file config or passing in options explicitly
- Fix bug in creating `Address` without `country_iso_code`
- Replaces `requests` dependency with `urllib3`

### 0.0.1 June 29, 2020

- Initial release
