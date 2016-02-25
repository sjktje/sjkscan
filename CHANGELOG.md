# Change Log

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