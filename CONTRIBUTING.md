# Continuing the project

Keep the physical reminder prominent: **OUT → Map 1 → SO; IN → Map 2 → RC**, subject to verification on the connected controller.

For a new source or map version:

1. Preserve the original privately. Record its source and SHA-256 before editing anything.
2. Give the public artifact an unambiguous identity, family, parent, container information, and status. Do not reuse a version number for different fuel tables.
3. Review notes-buffer metadata before publication. Record any metadata-only derivative and new hash; never conceal a table modification as metadata cleanup.
4. Add the artifact to `manifest.json`, including its size, public SHA-256, source, and status. Archive superseded versions instead of replacing them.
5. Export a fuel comparison with `tools/pcv.py diff`. Check other tables and configuration independently. Tool support is restricted to the recovered format family.
6. Run the integrity checks and tests. Use `templates/SESSION.md` for official-software review, exact setup, device readback, and observations.
7. Promote a test version only when the acceptance evidence is recorded. The word “known good” needs a stated setup and source of acceptance.
8. Build a cumulative archive containing every recovered version, publish its checksum, and explain any still-missing source files.

Priorities are recovering the exact August 15 releases, validating the public derivatives in Dynojet software, verifying switch positions, and recording actual measurements. Readable documentation or successful binary parsing does not establish an engine calibration result.

Avoid publishing device identifiers, private backup paths, full chat exports, or unrelated personal data in issue reports. Include the relevant map hash, software version, and concise observations instead.
