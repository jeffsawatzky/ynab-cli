# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.4.0 (2025-06-06)

### Feat

- **budgets**: added a command to list all budgets

## v0.3.0 (2025-06-06)

### BREAKING CHANGE

- changes the way the commands need to be run. You now need to specify the "run" command before any of the subcommands

### Feat

- added a feature to prefix unused payees to make them easier to find and delete in ynab
- added a list all command to payees
- add a textual based tui
- use rich for better user feedback
- implement initial cli

### Refactor

- cleaned up some code, sorted lists, and improved the file selector
