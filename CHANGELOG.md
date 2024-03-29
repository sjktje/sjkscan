# Change Log

## [Unreleased]

- Use hatch to build package
- Update Wand and PyPDF2 dependencies

## [1.2.0] - 2016-02-27

### Added
- Utility function is_scan_name(name) which returns True if name matches config dir_format and otherwise False
- -V and --version now prints version and exits.
- Lots of debug/info logging
- Log level is settable through sjkscan.conf and command line switches -l and --loglevel

### Changed
- scand will now only process directories with names corresponding to dir_format

## [1.1.0] - 2016-02-25

### Added
- Change log
- Utility functions files(), move() and remove()

### Changed
- The name of the scanned directory (typically YYYY-MM-DD_HH-MM-SS) + '.pdf' is used as filename for merged pdf output, instead of 'output.pdf'.
- Merged pdf files are moved to inbox
- Directory of other files (pnms, pdfs) is moved to archive. The idea here is to keep the files in case sjkscan improperly removes non-blank pages. Once sjkscan has undergone more testing this should not be an issue.
- Config logic is now in its own module


### Fixed
- Configuration file interpolation. Setting inbox to '%(data)s/INBOX' in the config file will now expand to /whatever/data/is/INBOX.

[Unreleased]: https://github.com/sjktje/sjkscan/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/sjktje/sjkscan/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/sjktje/sjkscan/compare/v1.0.0...v1.1.0
