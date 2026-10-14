# ModVerse theme shares: 24-part audit and GitHub publishing status

**Date:** 2026-10-13. **Current public catalog:** 8 themes (preserved).  
**New candidate release:** `themes-2026-10-approved-batch02` (release not yet uploaded).

The original Discord HTML attachment bundles supplied to the maintainer were recovered into 24 ZIP batches. The 24-part SHA-256 audit covered **286 actual original files**.

| Finding | Count |
| --- | ---: |
| Source attachments hashed and verified | 286 |
| Contained recognizable Cherax ClickGUI configurations | 196 |
| Existing GitHub themes among those candidates | 5 |
| Distinct new assets normalized into safe ZIPs for Build 092 | **189** |
| Previously identified ClickGUI candidates needing special review | 2 |
| Other files not approved as ClickGUI themes (unrelated or manual-review) | 90 |
| Original theme-share attachments above the collector's 35 MiB limit | 5 |

The new 189 ZIP assets total **582,439,553 bytes**. A corresponding set of 189 separate thumbnails was produced from source archive artwork where possible, or explicitly labeled generated placeholders otherwise. Thumbnails are **not** represented as in-game screenshots.

## Publication gate

The new release ZIPs have **not yet been uploaded to GitHub Releases**, so `catalog.json` must **not** be expanded prematurely. The live catalog remains at 8 until all 189 actual assets are uploaded, verified against their normalized SHA-256 hashes, and the JPEG thumbnails are committed. Publishing automation must:

1. Preserve the eight existing catalog entries.
2. Upload 189 normalized ZIP assets to GitHub Release `themes-2026-10-approved-batch02`.
3. Verify the published GitHub Release asset sizes and SHA-256 digests.
4. Commit 189 corresponding JPEG previews into `marketplace/themes/thumbnails/`.
5. Merge 189 entries into `marketplace/themes/catalog.json` using the current `modverse.distribution.v1` format.
6. Confirm **197** visible theme entries in ModVerse and check the catalog validator.

The original Discord uploader is retained in `shared_by`. Do not infer original creator from an uploader name. Public distribution rights and authentic creator credit require independent review and correction where necessary.

Ineligible resources include vehicle/track and saved-player JSONs, RPF/DLC archives, non-Cherax theme formats, and any unsupported archive contents. No unreviewed package should enter the catalog.

ModVerse Build 092's existing ZIP auto-installer remains unchanged. New downloads are only catalog-listed after their GitHub Release bytes are available and SHA-pinned.
