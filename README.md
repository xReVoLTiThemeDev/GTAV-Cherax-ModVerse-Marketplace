# ModVerse Community Marketplace

ModVerse is a Cherax GTA V marketplace for community vehicles, themes, outfits, and DLCs, alongside GTA5-Mods ASIs and addon vehicles.

## Build 090 storefront layout

- **GTA5-Mods:** ASIs / DLCs (existing external GTA5-Mods browsing and staging)
- **Cherax:** Outfits / Vehicles / DLCs / Themes
- **Library:** Favorites / Installed / Downloads
- **Tools:** Diagnostics / Test Runner / Settings

## Live public catalogs

| Category | Status | Catalog |
| --- | --- | --- |
| Cherax Vehicles | 120 SHA-256-pinned public JSONs | [Vehicle catalog](marketplace/vehicles/catalog.json) |
| Cherax Themes | 8 published release-backed themes | [Theme catalog](marketplace/themes/catalog.json) |
| Cherax Outfits | GitHub endpoint and installer ready; no uploaded approved outfit bytes yet | [Outfits catalog](marketplace/outfits/catalog.json) |
| Cherax DLCs | GitHub endpoint and RPF7 installer ready; no uploaded approved RPF bytes yet | [DLCs catalog](marketplace/dlcs/catalog.json) |

The outfit and Cherax DLC catalogs intentionally begin with no items. Archived Discord HTML lists attachments but is **not** a substitute for the original JSON/RPF bytes.

## Install destinations

- `Documents\Cherax\Outfits\mMV_<name>_<hash>.json`
- `Documents\Cherax\Vehicles\mMV_<name>_<hash>.json`
- `Documents\Cherax\DLCs\mMV_<name>_<hash>\dlc.rpf`
- `Documents\Cherax\Theme\ClickGUI\` (existing isolated theme installer)

All direct Cherax downloads are verified with catalog-pinned SHA-256 before installation. The client refuses to replace different existing files and stores thumbnails persistently. DLCs must be ready-made, unencrypted RPF7 OPEN files and use the existing Cherax DLC layout; ModVerse does not build or mount RPFs from loose assets.

## Source archives and contributor attribution

Original uploader attribution and source IDs are kept separate from verified creator identity. Creator permission to publicly redistribute both the package and preview image must be established before public hosting. Consult [vehicle rights](marketplace/vehicles/ATTRIBUTION_AND_RIGHTS.md), [vehicle contribution guide](marketplace/vehicles/SUBMIT_A_VEHICLE.md), and the [Cherax catalog specs](marketplace/outfits/README.md).

New Cherax Outfit and DLC catalogs support paginated `catalog-2.json`, `catalog-3.json`, etc. An explicit sequential `pages` field on the main catalog enables up to 10 catalog pages of 500 entries, with validation across pages.

`python scripts/validate_vehicles_catalog.py` validates vehicles and `python scripts/validate_cherax_assets.py` validates outfit and DLC catalogs. GitHub Actions runs these checks when corresponding public files change.

## Safety

Only distribute files whose authors authorized the public hosting. Mods and custom assets may be incompatible with some GTA versions or BattlEye restrictions. ModVerse is unaffiliated with Rockstar Games, Cherax, or GTA5-Mods.
