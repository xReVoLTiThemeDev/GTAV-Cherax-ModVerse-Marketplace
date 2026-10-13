# ModVerse Cherax dlcs

This is the public, integrity-checked dlcs marketplace for Cherax. The client installs to `Documents\\Cherax\\DLCs/<safe-id>/dlc.rpf`.

**Current status:** the catalog is initialized with no downloadable items. Discord HTML archives contain attachment names, not the actual file bytes. An item is made public only when its original file has been obtained, its GitHub bytes and SHA-256 verified, and redistribution permission and credit recorded.

## Format

Catalog: `marketplace/dlcs/catalog.json`, schema `modverse.cherax.assets.v1`. One catalog item includes:

```json
{
  "id": "123456789012345678-123456789012345678",
  "name": "Example",
  "creator": "Original creator name or Original developer unverified",
  "shared_by": "Discord uploader",
  "filename": "dlc.rpf",
  "sha256": "64 lowercase hexadecimal characters",
  "size_bytes": 12345,
  "thumbnail_sha256": "64 lowercase hexadecimal characters (optional)",
  "source_message_id": "123456789012345678"
}
```

File storage: `marketplace/dlcs/files/<id>.rpf`. Optional preview: `marketplace/dlcs/thumbnails/<id>.jpg`. The client derives raw GitHub URLs; no arbitrary external host links are permitted. Use matching file checksums; no silent overwrites. Only already-built, unencrypted OPEN RPF7 DLCs are supported. A valid DLC must pass Cherax DLC manager header validation. No automatic RPF construction or mounting is attempted.

See `scripts/validate_cherax_assets.py` for checks. Attribution and redistribution must be reviewed separately; Discord upload alone is not a license.
