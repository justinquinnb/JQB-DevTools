# Development Guide
*Mostly for myself as I sporadically return to this project from other language workflows.*

## Setup Virtual Environment
`.\.venv\Scripts\activate` to enable venv from project root
`deactivate` to disable venv

## Build Wheel for Distribution
`uv build`

## Install Wheel for Testing
### As Standalone Package
`pip install --force-reinstall --user ./dist/<wheel-name>` to install JQB-DevTools for the current user
Note that `--force-reinstall` is required to overwrite the existing installation during testing of the same project version

### Synced with Local Development
`pip install -e --user ./dist/<wheel-name>` to install JQB-DevTools for the current user, synced with local development
