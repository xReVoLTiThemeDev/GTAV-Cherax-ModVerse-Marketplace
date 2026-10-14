# ModVerse Cherax Shares - GitHub Publication Status

Last audited 2026-10-13. This is a **publication status**, not a promise that all content is live.

## Currently published

| Category | Public catalog entries | Status |
|---|---:|---|
| Cherax Themes | **196** | 8 original + 188 October Batch02, GitHub Release + SHA256 verified |
| Cherax Vehicles | **120** | Existing approved vehicle collection |
| Cherax Outfits | **0** | 2,832 unique items audited and packaged locally, not yet uploaded |
| Cherax DLCs | **0** | 15 RPF7 OPEN assets audited and staged locally, not yet uploaded |

## Outfits/DLC batch01 staging (2026-10-13)

The repository owner supplied all 13 collector ZIPs. File hashes verified; nested archives inspected. Inventory:
- Outfits: 1,046 recovered source attachments (985 JSON, 37 ZIP, 24 RAR). 981 standalone Cherax type-2 outfit saves; 3,818 valid outfit JSONs inside ZIP/RAR, yielding 4,799 recognizable saves; 2,832 **unique SHA256 content** after deduplication. Six catalog pages are prepared (500/500/500/500/500/332), size under 1 MiB/page. All unique outfit contents total about 7.7 MB.
- Cherax DLCs: 15 source attachments (8 direct RPF, 4 ZIP, 2 RAR, 1 7z). All 15 yielded unique ready-made RPF7 OPEN files with plausible directory headers. Total uncompressed RPF data about 321.5 MB. Public hosting planned as GitHub Release assets; the B093 Lua client allows only fixed-repository, pinned release URLs and verifies SHA256 before installation.
- Five additional outfit attachments and nine DLC attachments are oversized (>35 MiB) and outside this batch. No unsupported archives were silently published.
- Original source uploaders, message IDs, original filenames, and duplicate provenance retained in private publisher audit. Creator identity and public redistribution rights must be independently verified.

**Publishing is not done**: GitHub catalogs remain at 0 for Outfits and DLCs. The Build093 + unified publisher kit is prepared for the owner's local GitHub CLI workflow. First prepare/reverify on Windows, then confirm redistribution rights and publish. The publisher verifies all 15 GitHub Release SHA digests and sizes before committing Outfit files, six catalog pages, the DLC catalog, and updated CI validator. It does not modify Themes or Vehicles.

## Approved install locations

- Outfits: `Documents\Cherax\Outfits\mMV_<name>_<sha>.json`
- DLCs: `Documents\Cherax\DLCs\mMV_<name>_<sha>\dlc.rpf`
- Themes: `Documents\Cherax\Theme\ClickGUI\`

Catalog file verification and structural checks do not guarantee in-game compatibility. Test each model and required dependencies in Cherax. Community upload attribution is not proof of a license.
