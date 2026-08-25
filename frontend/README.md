# Project Olly frontend build tooling

This directory is the build source for the site's bundled JavaScript.

## Setup

Requires Node.js + npm (node >= 18 recommended).

```sh
npm install
```

## Build

```sh
npm run build
```

This runs `esbuild frontend/src/main.js --bundle --minify --outfile=project-static/js/app.min.js`,
producing the minified bundle that `base.html` and `staff/staffbase.html` load as
`{% static "js/app.min.js" %}`.

A watch mode is also available:

```sh
npm run watch
```

## Notes

- The current bundle is intentionally near-empty: the site's inline template
  scripts (document.write date rendering, DataTables/Chart/datetimepicker init,
  etc.) are kept in the templates themselves. New shared JavaScript should be
  written as modules imported from `src/main.js`.
- Commit the built `project-static/js/app.min.js` so deployments do not need
  Node installed; rebuild it whenever `frontend/src/` changes.
- `node_modules/` is git-ignored.