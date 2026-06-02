# Orbital Catalog

Source URL: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Catalog.htm

Source title: Catalog

Retrieved: 2026-06-02

Import type: Structured summary from Cisco Orbital help page and browser page evidence. This file is not a verbatim copy of the page.

## Summary

The Orbital Catalog contains predefined queries and scripts that can be used to investigate possible security breaches and mitigate incidents.

The Catalog contains two broad categories of query and script content:

- Stock content: queries and scripts created by the Orbital team and Cisco Talos.
- Custom content: user-created custom queries and scripts.

## Access Formats

The Orbital Catalog is available in two formats:

- Authenticated product UI
- Orbital API

The UI and API represent the same product domain, but they may expose catalog metadata with different labels, structure, routes, or schema fields.

Use the UI context files to understand product terminology and how users see catalog entries. Use the API context files to understand automation, request/response schemas, and programmatic access.

For query-specific source mapping, use `Orbital_Query_Catalog_Source_Map.md`. It links upstream osquery structure, Catalog API access, and authenticated UI metadata.

## Project Mapping

In this project, the Orbital repo source folder uses these folders:

- `01_Source_Files/Orbital_Repo_Source/Catalog_queries`: 1:1 copy of Cisco-managed catalog query templates.
- `01_Source_Files/Orbital_Repo_Source/Catalog_scripts`: 1:1 copy of Cisco-managed catalog script templates.
- `01_Source_Files/Orbital_Repo_Source/custom_queries`: user's personal Orbital query work.
- `01_Source_Files/Orbital_Repo_Source/custom_scripts`: user's personal Orbital script work.

## Handling Rules

Treat `Catalog_queries` and `Catalog_scripts` as read-only source references. Do not edit these files directly.

Treat `custom_queries` and `custom_scripts` as user-owned source material maintained through VS Code and GitHub. Do not modify these files unless explicitly asked to update the GitHub-tracked work.

When adapting catalog content, copy the relevant file into `02_Working_Files` first.

## Notes

The Catalog help page notes that custom queries and scripts are not automatically saved to the catalog. Saving behavior should be checked in the relevant Cisco Orbital help topics before assuming persistence.
