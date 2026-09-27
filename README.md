# Documenso branding modifications — Tom of Finland Foundation

This repository is the complete set of changes the Tom of Finland Foundation applies to
[Documenso](https://github.com/documenso/documenso) **v2.18.0** (Docker image `documenso/documenso:v2.18.0`, unmodified otherwise)
for its signing service at **https://sign.tomoffinland.org**. It is published to meet the source-offer obligation of the
GNU Affero General Public License v3.0 (§13) for the modified version that users interact with over the network.

Licence: **AGPL-3.0** (see `LICENSE`), the same licence as Documenso. Documenso is © Documenso, Inc. and contributors.

## What is modified and why
The Foundation shows its own name and logo on the sign-in and app pages and fixes button contrast. Nothing in signing,
certificates, audit logs, email or the API is changed.

| File | Changes (applied to compiled files copied out of the v2.18.0 image) |
|---|---|
| `patch_brand.py` | Replaces the Documenso logo components (`branding-logo-*.js`, `BrandingLogo` in `server-build.js`) with the Foundation logo (black/white images); adds the logo above the sign-in title (`signin-*.js`); black/white primary-button contrast and the light/dark logo switch (CSS, from `logo-light-dark.css`); adds the sign-in footer linking to this repository (step 3b). |
| `patch_meta.py` | Page metadata (title, description, OpenGraph/Twitter tags and preview image), the server-rendered sign-in logo and footer (identical to the client, step 10), the client-side head tags in `meta-ClrBL2aA.js` (identical to the server's, step 11, so the page title stays "Sign with Tom"), keeps the `?v=` query on the root redirect. The `author` tag keeps the engine attribution: "powered by Documenso (AGPL-3.0)". |
| `logo-light-dark.css` | CSS block that shows the black logo in light mode and the white logo in dark mode. |

## How it is applied
1. Copy the named compiled files out of the `documenso/documenso:v2.18.0` image into a host folder
   (`/opt/isf/public/assets/`, with `server-build-*.js` saved as `server-build.js`).
2. `python3 patch_brand.py && python3 patch_meta.py` (idempotent: running them twice changes nothing).
3. Bind-mount the patched files read-only over the same paths in the container, then restart the Documenso container.

The filenames carry build hashes, so these patches work **only** on v2.18.0. Before any image upgrade the mounts are removed,
the upgrade is tested on plain upstream Documenso, and the patches are regenerated or dropped.

## Not included
The logo images (`branding-black.png`, `branding-white.png`, `apple-touch-icon.png`, `opengraph-image.jpg`) are trademarks of the
Tom of Finland Foundation and are not part of this repository or its licence.

## Contact
tech@tomoffinland.org

---
*Maintainers: this folder is mirrored from the Foundation's private deployment repository (`deploy/production-small/branding/`,
ADR-017). After every change to that folder, commit it and run `bash tools/mirror-branding.sh` from that repository's root.
Anything patched on the server by hand must be added to the folder the same day, or it is lost at the next rebuild.*
