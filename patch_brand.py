import os

ASSETS_DIR = "/opt/isf/public/assets"

# 1. branding-logo-ZrpwA0gU.js
logo_content = 'import{j as c}from"./jsx-runtime-u17CrQMm.js";const h=({className:s,style:y,...l})=>c.jsxs("span",{className:"inline-flex items-center",style:y,children:[c.jsx("img",{src:"/branding-black.png",alt:"Tom of Finland Foundation",className:`block dark:hidden ${s||"h-6 w-auto"} object-contain`,...l}),c.jsx("img",{src:"/branding-white.png",alt:"Tom of Finland Foundation",className:`hidden dark:block ${s||"h-6 w-auto"} object-contain`,...l})]});export{h as B};'
with open(os.path.join(ASSETS_DIR, "branding-logo-ZrpwA0gU.js"), "w") as f:
    f.write(logo_content)
print("1. branding-logo-ZrpwA0gU.js written")

# 2. branding-logo-icon-jFsUaD8n.js
icon_content = 'import{j as c}from"./jsx-runtime-u17CrQMm.js";const s=({className:e,style:y,...l})=>c.jsx("img",{src:"/apple-touch-icon.png",alt:"Tom of Finland Foundation",className:`${e||"h-6 w-6"} object-contain`,style:y,...l});export{s as B};'
with open(os.path.join(ASSETS_DIR, "branding-logo-icon-jFsUaD8n.js"), "w") as f:
    f.write(icon_content)
print("2. branding-logo-icon-jFsUaD8n.js written")

# 3. signin-R1dgLAzA.js
signin_path = os.path.join(ASSETS_DIR, "signin-R1dgLAzA.js")
with open(signin_path, "r") as f:
    signin_js = f.read()

target = 'r.jsx("h1",{className:"font-semibold text-2xl"'
replacement = 'r.jsx("div",{className:"mb-6 flex justify-start",children:r.jsxs("span",{className:"inline-flex items-center",children:[r.jsx("img",{src:"/branding-black.png",alt:"Tom of Finland Foundation",className:"block dark:hidden h-8 w-auto object-contain"}),r.jsx("img",{src:"/branding-white.png",alt:"Tom of Finland Foundation",className:"hidden dark:block h-8 w-auto object-contain"})]})}),' + target

if target in signin_js and "/branding-black.png" not in signin_js:
    signin_js = signin_js.replace(target, replacement)
    with open(signin_path, "w") as f:
        f.write(signin_js)
    print("3. signin-R1dgLAzA.js updated with logo")
else:
    print("3. signin-R1dgLAzA.js already patched or target not found")

# 3b. sign-in footer: "Powered by Documenso (AGPL-3.0)", linking to this change set — the AGPL-3.0 §13 source offer
#     (ADR-017, WB-4B). Must stay identical to step 10 in patch_meta.py (SSR), otherwise React hydration fails and the
#     sign-in page goes dead (INC-ISF-0006). Replaces the earlier two-part footer if present. Idempotent.
SOURCE_URL = "https://github.com/tomoffinland-foundation/documenso-branding"
with open(signin_path, "r") as f:
    signin_js = f.read()
footer_target = 'className:"text-documenso-700 duration-200 hover:opacity-70"})}})})]})})});'
footer_old = ('r.jsxs("p",{className:"mt-6 text-center text-muted-foreground text-xs",children:["Powered by Documenso (AGPL-3.0) \u00b7 ",'
              'r.jsx("a",{href:"' + SOURCE_URL + '",target:"_blank",rel:"noopener noreferrer",className:"underline",'
              'children:"Source of this deployment\u2019s modifications"})]})')
footer_js = ('r.jsx("p",{className:"mt-6 text-center text-muted-foreground text-xs",children:r.jsx("a",{href:"' + SOURCE_URL + '",'
             'target:"_blank",rel:"noopener noreferrer",className:"hover:underline",children:"Powered by Documenso (AGPL-3.0)"})})')
if footer_js in signin_js:
    print("3b. signin footer already present")
else:
    if footer_old in signin_js:
        signin_js = signin_js.replace(footer_old, footer_js)
    elif signin_js.count(footer_target) == 1:
        signin_js = signin_js.replace(footer_target, 'className:"text-documenso-700 duration-200 hover:opacity-70"})}})}),' + footer_js + ']})})});')
    else:
        raise SystemExit("3b. signin footer target not found — refusing to patch (check SSR step 10 too)")
    with open(signin_path, "w") as f:
        f.write(signin_js)
    print("3b. signin footer written")

# 4. CSS contrast overrides
css_overrides = """
/* --- TOM OF FINLAND CONTRAST & BRANDING FIXES --- */
/* In light mode: primary button is pure black with pure white text */
.bg-documenso,
button.bg-documenso {
  background-color: #000000 !important;
  color: #ffffff !important;
}
.bg-documenso:hover,
button.bg-documenso:hover {
  background-color: rgba(0, 0, 0, 0.85) !important;
  color: #ffffff !important;
}
.bg-documenso *,
button.bg-documenso * {
  color: #ffffff !important;
}

/* In dark mode: primary button is crisp white with solid black text */
.dark .dark\\:bg-documenso,
.dark button.dark\\:bg-documenso {
  background-color: #ffffff !important;
  color: #000000 !important;
}
.dark .dark\\:bg-documenso:hover,
.dark button.dark\\:bg-documenso:hover {
  background-color: rgba(255, 255, 255, 0.88) !important;
  color: #000000 !important;
}
.dark .dark\\:bg-documenso *,
.dark button.dark\\:bg-documenso * {
  color: #000000 !important;
}
"""

for css_file in ["app-tof.css", "app-CEPnFH5l.css"]:
    path = os.path.join(ASSETS_DIR, css_file)
    with open(path, "r") as f:
        content = f.read()
    if "TOM OF FINLAND CONTRAST" not in content:
        content += css_overrides
        with open(path, "w") as f:
            f.write(content)
        print(f"4. {css_file} patched with contrast overrides")
    else:
        print(f"4. {css_file} already has contrast overrides")

# 4b. logo light/dark switching block (written on the server 2026-09-27 08:13 UTC by Nolan/Gemini, imported into git the same day).
#     Source of truth: logo-light-dark.css next to this script. Appended once per file; idempotent.
LOGO_CSS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-light-dark.css")
LOGO_MARK = "TOM OF FINLAND LOGO LIGHT / DARK MODE DYNAMIC SWITCHING"
with open(LOGO_CSS, "r") as f:
    logo_block = f.read()
for css_file in ["app-tof.css", "app-CEPnFH5l.css"]:
    path = os.path.join(ASSETS_DIR, css_file)
    with open(path, "r") as f:
        css = f.read()
    if LOGO_MARK in css:
        print(f"4b. {css_file}: logo light/dark block already present")
    else:
        with open(path, "w") as f:
            f.write(css.rstrip("\n") + "\n" + logo_block)
        print(f"4b. {css_file}: logo light/dark block appended")

# 4c. force the light theme (Q5, 2026-09-27): dark-mode devices got Documenso's dark variables on white pages.
#     Appended once per file, after 4b so it wins; idempotent.
LIGHT_CSS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "force-light.css")
LIGHT_MARK = "TOM OF FINLAND FORCE LIGHT THEME"
with open(LIGHT_CSS, "r") as f:
    light_block = f.read()
for css_file in ["app-tof.css", "app-CEPnFH5l.css"]:
    path = os.path.join(ASSETS_DIR, css_file)
    with open(path, "r") as f:
        css = f.read()
    head = css.split("/* ========================================================\n   " + LIGHT_MARK)[0] if LIGHT_MARK in css else css
    new = head.rstrip("\n") + "\n\n" + light_block
    if new == css:
        print(f"4c. {css_file}: force-light block already current")
    else:
        with open(path, "w") as f:   # in place (bind-mounted single file)
            f.write(new)
        print(f"4c. {css_file}: force-light block {'replaced' if LIGHT_MARK in css else 'appended'}")

# 5. server-build.js
server_path = os.path.join(ASSETS_DIR, "server-build.js")
with open(server_path, "r") as f:
    server_js = f.read()

old_svg = """const BrandingLogo = ({
  ...props
}) => {
  return /* @__PURE__ */ jsxs("svg", { xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 2248 320", ...props, children: ["""

new_svg = """const BrandingLogo = ({ className: s, style: y, ...props }) => {
  return /* @__PURE__ */ jsxs("span", { className: "inline-flex items-center", style: y, children: [
    /* @__PURE__ */ jsx("img", { src: "/branding-black.png", alt: "Tom of Finland Foundation", className: `block dark:hidden ${s || "h-6 w-auto"} object-contain`, ...props }),
    /* @__PURE__ */ jsx("img", { src: "/branding-white.png", alt: "Tom of Finland Foundation", className: `hidden dark:block ${s || "h-6 w-auto"} object-contain`, ...props })
  ]});
};
const IgnoredLogo = ({
  ...props
}) => {
  return /* @__PURE__ */ jsxs("svg", { xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 2248 320", ...props, children: ["""

if old_svg in server_js:
    server_js = server_js.replace(old_svg, new_svg)
    print("5. server-build.js BrandingLogo patched")
else:
    print("5. server-build.js BrandingLogo already patched or pattern differed")

server_js = server_js.replace("/assets/app-CEPnFH5l.css", "/assets/app-tof.css")

with open(server_path, "w") as f:
    f.write(server_js)
print("5. server-build.js written")
