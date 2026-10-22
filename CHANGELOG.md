# `batterway` Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Adding an incompatible type to a `Quantity` or `ProductInstance` now raises `TypeError`
  instead of silently passing.
- Printing a `ProcessLCI`, checking a `RecyclingRoute` and fetching data in `RecyclingModel` no
  longer fail on attributes that do not exist.
- `pytest` now finds and runs the test suite.
