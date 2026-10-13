# ModVerse Vehicles: Attribution and redistribution

ModVerse is a community marketplace for Cherax saved-vehicle JSONs. The public catalog is permission-gated.

## What is credited

- **Original Developer**: the person or team established as the creator of the saved-vehicle configuration. This is shown as the catalog `creator` field.
- **Shared by**: the Discord account that originally posted the file. The uploader may not be the developer. This is recorded in `shared_by`.
- **Source**: retain the Discord channel ID, source message ID, original filename, post date when known, and (when verified) a link to the original message.
- Preserve the original JSON bytes and publish SHA-256 hashes so the game client can verify installations.
- Credit for an image/screenshot must also be supported by permission to redistribute that image. A JSON-only grant does not automatically cover its thumbnail.

## Eligibility for public distribution

Before any JSON or thumbnail is added, a human maintainer must document the applicable redistribution authorization, such as a specific grant from the appropriate creator/rightsholder, a verified license, or channel rules actually accepted by the relevant rights holders and broad enough to cover public GitHub redistribution. Record the evidence privately. Discord uploads, attribution alone, lack of prior complaints, or successful in-game tests do not independently establish publication rights.

If the uploader's creator status is unknown, do not present that account as the original developer. Hold the entry for review, or obtain reliable attribution. Respect creator-specified credit language.

Public catalog entries may retain `shared_by`, `source_channel_id`, `source_message_id`, and `creator_credit_basis` alongside the established `creator` field. These fields do not authorize distribution by themselves.

## Private testing versus public catalog

The initial 119 private review candidates are not public assets: 20 Pilot 01 files were user-confirmed in-game, and the Batch 02 Eleggy was additionally user-confirmed. The remaining Batch 02 files require individual in-game checks. All items require publication-rights review.

The public `catalog.json` may legitimately have `items: []`; this keeps ModVerse's GitHub endpoint functional without prematurely distributing third-party uploads.
