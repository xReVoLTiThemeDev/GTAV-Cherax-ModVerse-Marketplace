# Vehicle publication checklist (GitHub)

The ModVerse Build 084 client reads `marketplace/vehicles/catalog.json` from this repository. The client shows only entries actually present in that public catalog.

Before adding each item:
- [ ] Verify that it is a Cherax Entity vehicle save and the content passes JSON parsing, model and SHA-256 checks.
- [ ] Verify the vehicle spawns and looks correct in the target Cherax/GTA V version. Parsing and download alone do not count.
- [ ] Establish original developer identity, separately from the Discord uploader's account name.
- [ ] Record affirmative redistribution basis for the saved-vehicle JSON and thumbnail image. Retain evidence privately.
- [ ] Confirm creator-required credit text and whether external/public GitHub redistribution is covered.
- [ ] Record original Discord channel/message provenance without fabricating a Discord server link.
- [ ] Keep original JSON bytes and SHA-256 hashes unchanged.
- [ ] Use the stable asset paths `marketplace/vehicles/files/<channel>-<post>.json` and `marketplace/vehicles/thumbnails/<channel>-<post>.jpg`.
- [ ] Upload file and thumbnail **before** adding the corresponding catalog row.
- [ ] Run `python scripts/validate_vehicles_catalog.py` in a checked-out repository and confirm GitHub Actions passes.
- [ ] Validate HTTPS raw URLs, creator credit, `mMV_` installation, SHA-256, duplicate detection, and in-game spawning in ModVerse.
- [ ] Keep an accessible removal/correction process.

**Do not upload the private Build 084 release preparation ZIP, review gallery, permission evidence file or source archive to this public repository.** The published catalog begins empty until a human has reviewed actual permissions.
