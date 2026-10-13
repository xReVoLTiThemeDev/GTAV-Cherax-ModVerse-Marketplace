# ModVerse Community Vehicles

This directory hosts the **public, permission-approved** JSON vehicle catalog for the ModVerse Cherax marketplace. The existing private testing collection (20 Pilot 01 + 99 Batch 02 Cherax-format files) is **not** automatically a public release. The first approved vehicle is **ZentornoGalaxyPink**, developed by **Public_Urinal**.

## Catalog
- `catalog.json`: `modverse.vehicles.v1`, `published: true`, max 500 entries per catalog revision.
- Each approved vehicle is stored unchanged at `files/<catalog-id>.json` (source-post ID or allocated first-party ID).
- Each approved JPG thumbnail is stored at `thumbnails/<catalog-id>.jpg`.
- The client derives URLs from validated numerical IDs and this repository's HTTPS raw base.
- The client verifies vehicle JSON byte size and SHA-256 before installing to `Documents\\Cherax\\Vehicles\\mMV_*.json`. Thumbnails are SHA-256 pinned too.
- An empty `items` array is valid, but the current public catalog contains **1 creator-submitted vehicle**. The private 119 candidate files are awaiting rights review; **21** have recorded in-game test results.

## Example catalog item (documentation only, do not add without authorization)

```json
{
  "id": "123456789012345678-234567890123456789",
  "name": "Example Vehicle",
  "creator": "Example Creator",
  "post_date": "Tuesday, October 12, 2026",
  "model": 1234567890,
  "filename": "mMV_Example_Vehicle_abcdef12.json",
  "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "size_bytes": 4096,
  "thumbnail_sha256": "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"
}
```

## Contribute vehicles

Use [the vehicle submission guide](SUBMIT_A_VEHICLE.md) or open a **Vehicle submission** issue in this repository. We welcome original Cherax vehicle builds with matching in-game screenshots, clear developer credit, and permission to host both files on GitHub.

## Publishing gate

Before adding a vehicle or thumbnail to this public GitHub repository, obtain and record **affirmative redistribution permission** from the creator/rightsholder for the JSON and screenshot, or another verified license permitting this use. A Discord upload, server membership, a working Cherax spawn, or an accurate preview alone does not establish that permission. Retain provenance, permission evidence, author attribution, in-game test findings, SHA-256 checks and a takedown/contact path.

The private local review set and in-game tests are useful compatibility evidence, but not a rights grant. Exclude incompatible foreign formats such as the detected Chairhax record. Do not edit vehicle JSON bytes before publication; stable hashes and filenames allow non-destructive installs.
