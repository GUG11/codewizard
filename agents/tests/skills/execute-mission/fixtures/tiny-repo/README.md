# Tiny Repo

This fixture is used by the `execute-mission` skill tests.

## Configuration

- `syncIntervalMs`: interval for user synchronization, in milliseconds.

## Commands

- `node scripts/test.js`: run fixture behavior checks.
- `node scripts/build.js`: load all source modules.

`package.json` also defines `npm test` and `npm run build` for environments where `npm` is available.
