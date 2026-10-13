# Publishing Cherax ClickGUI themes

Build 090 reuses the proven Build 079 ZIP theme installer and GitHub release-backed `modverse.distribution.v1` catalog. Themes install to `Documents\Cherax\Theme\ClickGUI` in isolated folders.

## Current status

Eight entries are currently public in [catalog.json](catalog.json). Their release assets are available under the existing `themes-2026-10-pilot01` GitHub release.

The available Discord HTML export contains references to additional theme attachments but **does not contain their bytes**. Do not add an entry merely from a filename or screenshot.

## Publishing a new theme

1. Recover the actual original theme ZIP, RAR, 7z, or JSON plus related backgrounds. Record the message ID, Discord uploader, independently established original creator credit, and public redistribution authorization.
2. Review the extracted archive for `Theme\ClickGUI` compatibility, archive traversal, executable payloads, ZIP bombs, and overlapping filenames. Do not flatten away required background paths.
3. Prefer a ZIP containing the theme JSON and assets. The current client auto-installs ZIP, uses a companion helper for RAR, and saves 7z for manual extraction.
4. Upload the reviewed archive to a GitHub Release. Record its **actual** release asset name, size in bytes and SHA-256 hash. Do not invent or guess direct URLs.
5. Upload an approved genuine JPEG thumbnail to `marketplace/themes/thumbnails/<id>.jpg`.
6. Add a `modverse.distribution.v1` entry to [catalog.json](catalog.json) with category `themes`, `install_mode: download_only`, correct `files[0].download_url` and `sha256`, release asset name, size, author credit, source provenance, and `thumbnail_url`.
7. Confirm the catalog displays in **Cherax → Themes** in ModVerse Build 090, and verify the ClickGUI theme loads after installation. Keep the original source archived privately.

GitHub hosting permission for the package and for the screenshot are separate. Discord posts alone do not establish either.

For high volume, batch the verified packages into additional GitHub Releases and incrementally merge their catalog records. Do not remove or overwrite the eight existing entries.
