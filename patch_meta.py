#!/usr/bin/env python3
"""Branding metadata patch for the pinned Documenso v2.18.0 image (ADR-017). Rewrites page metadata, the root redirect and the
server-rendered sign-in logo in /opt/isf/public/assets/server-build.js (bind-mounted over the image).

History: written on the server on 2026-09-27 (Nolan via Gemini); imported into git the same day with HUMAN-TODO Q3 decided:
the Foundation owns the title, but the `author` tag keeps the engine attribution (hard rule 9, AGPL-3.0 appropriate notices).
Idempotent: safe to re-run. Run after patch_brand.py, then `docker compose ... up -d documenso` (the module is loaded at start).
"""
import re

path = "/opt/isf/public/assets/server-build.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

AUTHOR = "Tom of Finland Foundation — powered by Documenso (AGPL-3.0)"

# 1. og:title
content = re.sub(
    r'property:\s*"og:title",\s*content:\s*"Documenso - The Open Source DocuSign Alternative"',
    'property: "og:title",\n    content: "Sign with Tom - Secure and Private"',
    content
)
content = re.sub(
    r'property:\s*"og:title",\s*content:\s*"Documenso - Join the open source signing revolution"',
    'property: "og:title",\n    content: "Sign with Tom - Secure and Private"',
    content
)

# 2. author — keep the engine attribution (Q3, 2026-09-27). Matches the upstream value and the earlier bare-Foundation value.
content = re.sub(
    r'name:\s*"author",\s*content:\s*"(Documenso, Inc\.|Tom of Finland Foundation)"',
    'name: "author",\n    content: "' + AUTHOR + '"',
    content
)

# 3. twitter:site
content = re.sub(
    r'name:\s*"twitter:site",\s*content:\s*"@documenso"',
    'name: "twitter:site",\n    content: "@tomoffinland"',
    content
)

# 4. default description
old_desc = 'const description = "Join Documenso, the open signing infrastructure, and get a 10x better signing experience. Pricing starts at $30/mo. forever! Sign in now and enjoy a faster, smarter, and more beautiful document signing process. Integrates with your favorite tools, customizable, and expandable. Support our mission and become a part of our open-source community.";'
new_desc = 'const description = "Sign with Tom - Secure and private institutional signing for the Tom of Finland Foundation.";'
if old_desc in content:
    content = content.replace(old_desc, new_desc)

# 5. default title
content = re.sub(
    r'title:\s*title\s*\?\s*`\$\{i18n\._\(title\)\}\s*-\s*Documenso`\s*:\s*"Documenso"',
    'title: title ? `${i18n._(title)} - Sign with Tom` : "Sign with Tom - Secure and Private"',
    content
)

# 6. twitter:title
if 'name: "twitter:title"' not in content:
    content = re.sub(
        r'(name:\s*"twitter:card",\s*content:\s*"summary_large_image"\s*},)',
        r'\1 {\n    name: "twitter:title",\n    content: "Sign with Tom - Secure and Private"\n  },',
        content,
        count=1
    )

# 7. full OpenGraph image metadata
old_og = """  }, {
    property: "og:image",
    content: `${NEXT_PUBLIC_WEBAPP_URL()}/opengraph-image.jpg`
  }, {"""
new_og = """  }, {
    property: "og:image",
    content: `${NEXT_PUBLIC_WEBAPP_URL()}/opengraph-image.jpg`
  }, {
    property: "og:image:secure_url",
    content: `${NEXT_PUBLIC_WEBAPP_URL()}/opengraph-image.jpg`
  }, {
    property: "og:image:type",
    content: "image/jpeg"
  }, {
    property: "og:image:width",
    content: "1200"
  }, {
    property: "og:image:height",
    content: "675"
  }, {
    property: "og:image:alt",
    content: "Tom of Finland Foundation"
  }, {"""
if old_og in content and "og:image:secure_url" not in content:
    content = content.replace(old_og, new_og, 1)

# 8. preserve the search query in the root redirect (routes/_index)
old_redir = """    throw redirect(formatDocumentsPath(currentTeam.url));
  }
  throw redirect("/signin");
}"""
new_redir = """    throw redirect(formatDocumentsPath(currentTeam.url));
  }
  const _u80 = new URL(request.url);
  throw redirect(`/signin${_u80.search}`);
}"""
if old_redir in content:
    content = content.replace(old_redir, new_redir, 1)

# 9. server-rendered sign-in logo (hydration must match the client patch in signin-R1dgLAzA.js)
target_signin = """      children: [signupError && /* @__PURE__ */ jsx(Alert, {
        variant: "destructive",
        className: "mb-4",
        children: /* @__PURE__ */ jsx(AlertDescription, {
          children: _(signupError)
        })
      }), /* @__PURE__ */ jsx("h1", {"""
replacement_signin = """      children: [signupError && /* @__PURE__ */ jsx(Alert, {
        variant: "destructive",
        className: "mb-4",
        children: /* @__PURE__ */ jsx(AlertDescription, {
          children: _(signupError)
        })
      }), /* @__PURE__ */ jsx("div", {
        className: "mb-6 flex justify-start",
        children: /* @__PURE__ */ jsxs("span", {
          className: "inline-flex items-center",
          children: [/* @__PURE__ */ jsx("img", {
            src: "/branding-black.png",
            alt: "Tom of Finland Foundation",
            className: "block dark:hidden h-8 w-auto object-contain"
          }), /* @__PURE__ */ jsx("img", {
            src: "/branding-white.png",
            alt: "Tom of Finland Foundation",
            className: "hidden dark:block h-8 w-auto object-contain"
          })]
        })
      }), /* @__PURE__ */ jsx("h1", {"""
if target_signin in content:
    content = content.replace(target_signin, replacement_signin, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("patch_meta: server-build.js written; author =", AUTHOR)
