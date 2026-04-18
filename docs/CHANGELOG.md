# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-04-19
### Added
- Official package name `videocut-cli` for PyPI distribution.
- New `videocut doctor` command for system dependency health checks (FFmpeg, Node.js, etc.).
- Dynamic filename formatting: `{slug}_{id}_{resolution}.mp4`.
- Support for `--metadata-only` mode (downloads metadata & thumbnail only).
- Support for `--extract-audio` mode (direct conversion to MP3).
- **Cookie Persistence** system: automatic saving and reuse of cookies in `~/.videocut/stored_cookies.txt`.
- **Smart Skip** logic: automatically skips processing if the target file already exists.
- Clean CLI output by suppressing SABR and Deprecation warnings.

### Changed
- Metadata file naming updated to `metadata_{id}.md`.
- Improved Shorts URL transformation logic.

## [0.1.0] - 2026-04-18
### Added
- Initial project structure.
- Basic `download` command using `yt-dlp`.
- Basic `edit` command with text/image watermarking.
- MIT License.
