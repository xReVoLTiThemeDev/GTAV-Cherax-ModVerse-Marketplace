# Approved vehicle batch inbox

Upload one file here, using the **exact filename**:

`modverse-approved-119.zip`

Go to [this folder](https://github.com/xReVoLTiThemeDev/GTAV-Cherax-ModVerse-Marketplace/tree/main/marketplace/vehicles/inbox) and choose **Add file → Upload files**, then commit directly to the `main` branch.

The [GitHub Actions importer](../../../.github/workflows/import-approved-vehicle-batch.yml) automatically checks the batch manifest, every SHA-256, the expected Cherax Entity JSON structure, JPEG integrity, duplicate IDs and installer filenames. It writes the 238 approved files and merges the public catalog **after** all checks pass. It then deletes the inbox ZIP from the current working tree.

The existing ZentornoGalaxyPink entry is preserved. The expected new total is **120 vehicles**.

**Credits:** The original Discord uploader remains explicitly credited as `shared_by`. Where the underlying original developer is not verified, the creator field states that attribution is unverified. Correct it whenever reliable creator information becomes available.

**Compatibility:** The release archive contains 21 records previously tested in-game and 98 JSONs validated for Cherax format and SHA-256 only. Community testing remains important.

**Publication rights:** This batch is being processed based on the repository owner's confirmation that the relevant rights holders approved public GitHub redistribution of every vehicle JSON and matching preview. The importer cannot independently audit private permission correspondence.
