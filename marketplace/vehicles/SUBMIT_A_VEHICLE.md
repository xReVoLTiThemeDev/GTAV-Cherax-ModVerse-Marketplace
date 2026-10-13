# Submit a saved Cherax vehicle to ModVerse

ModVerse accepts original **Cherax Entity** vehicle JSONs and matching in-game JPEG screenshots.

## How to submit
1. Save your vehicle in Cherax. Its JSON must contain `"format":"Cherax Entity"`, `"type":1`, and a numeric `"model"`.
2. Take a genuine screenshot of the exact saved vehicle in GTA V.
3. Open a **Vehicle submission** issue in this repository, attaching or linking the JSON and JPEG.
4. Identify the **original configuration developer**, plus the uploader if different. Include other required credits.
5. Confirm your authority to allow **public GitHub hosting and downloading** of the JSON and screenshot, separately. If they belong to someone else, include evidence of the creator's grant or redistribution license.

**Only submit files you are authorized to publish publicly.** A Discord upload or attribution alone does not establish redistribution permission.

## Review and publishing
Maintainers verify SHA-256 hashes, Cherax format, filename safety, rights, developer credit, duplicates, and in-game compatibility. Structural validation alone is not an in-game test.

Approved assets use `marketplace/vehicles/files/<catalog-id>.json` and `marketplace/vehicles/thumbnails/<catalog-id>.jpg`. The maintainer adds each row to `marketplace/vehicles/catalog.json` **only after** both assets have been uploaded and verified. The in-game installer gives the downloaded file a different `mMV_<name>_<hash>.json` filename.

Build 088 uses the confirmed DriftGod-style stock-first spawn and staged modification restore; each new model still needs testing.

See [Attribution and Rights](ATTRIBUTION_AND_RIGHTS.md) and [Takedown and Corrections](TAKEDOWN_AND_CORRECTIONS.md).
