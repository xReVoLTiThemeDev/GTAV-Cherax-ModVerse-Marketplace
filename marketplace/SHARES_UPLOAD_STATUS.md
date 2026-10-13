# ModVerse Cherax Shares: Upload status

Last reviewed: 2026-10-13.

## Currently live
- **Cherax Vehicles:** 120 GitHub catalog entries, 120 vehicle previews
- **Cherax Themes:** 8 catalog entries backed by actual GitHub Release assets; GitHub's release SHA-256 digests match the 8 catalog-pinned hashes
- **Cherax Outfits:** 0 public packages, but catalog and the Build 090+ installer are ready
- **Cherax DLCs:** 0 public packages, but catalog and the Build 090+ RPF7 installer are ready

## Awaiting original attachment files

The available Discord HTML exports and their inventory CSVs identify:
- **Themes:** 291 attachment references (122 ZIP, 100 RAR, 66 JSON, 3 7z)
- **Outfits:** 1,051 attachment references (985 JSON, 40 ZIP, 26 RAR)
- **DLCs:** 24 attachment references (11 RPF, 8 ZIP, 4 RAR, 1 7z)

These counts describe **references, not unique or installable mods**. The HTML exports alone do not contain the original bytes. The corresponding folders ending in `.html_Files` are needed for matching and validation. Only actual, inspected source packages will enter public catalogs. Zip/RAR/7z attachments may contain multiple mods or irrelevant formats and need individual inspection.

To submit directly from GitHub use the [Cherax asset submission issue](https://github.com/xReVoLTiThemeDev/GTAV-Cherax-ModVerse-Marketplace/issues/new/choose). Creator permission, reliable credit, actual file bytes, and SHA-256 validation are required before publication.

## Destination paths
- Outfits: `Documents\Cherax\Outfits\`
- DLCs: `Documents\Cherax\DLCs\<package-name>\dlc.rpf`
- Themes: `Documents\Cherax\Theme\ClickGUI\`

Use the existing `scripts/validate_cherax_assets.py` before approving new Outfit/DLC catalog entries; the GitHub Actions validation workflow checks those catalogs and the Vehicle catalog on push and PR.

**Known-good vehicle spawning** is unaffected by content publication. Build 092 specifically fixes the repeated Installed/GTA5-Mods registry scan loop.
