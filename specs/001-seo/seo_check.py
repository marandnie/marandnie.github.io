#!/usr/bin/env python3
"""Chequeos de aceptación de la spec 001 (SEO) para mandieto.com.ar.

Uso:
    python3 specs/001-seo/seo_check.py _site                    # build local
    python3 specs/001-seo/seo_check.py https://mandieto.com.ar  # sitio publicado
    python3 specs/001-seo/seo_check.py _site --git-base 7614e79  # + CA10 (desde la raíz del repo)

Solo usa la biblioteca estándar. Sale con código 1 si algún chequeo falla.
"""
import argparse
import json
import os
import re
import struct
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

SITE_URL = "https://mandieto.com.ar"
PERSON_NAME = "Marina Nieto"
SAME_AS_HOSTS = ("linkedin.com", "github.com", "x.com")

# CA4: URL vieja -> URL nueva
REDIRECTS = {
    "/2020/01/09/newpost.html": "/blog/nueva-web/",
    "/biolog%C3%ADa/2020/02/05/Lasrazasnoexisten.html": "/blog/la-humanidad-del-genoma/",
    "/softwaredev/2020/02/06/Agile.html": "/blog/agile-manifesto/",
    "/spd/": "/spd/primer-parcial/",
}
ENGLISH_PAGES = ["/blog/agile-manifesto/"]  # CA9
# CA10: archivo viejo -> archivo nuevo (el cuerpo debe ser idéntico)
RENAMED_POSTS = {
    "_posts/2021-01-09-newpost.md": "_posts/2020-01-09-nueva-web.md",
    "_posts/2021-02-04-Lasrazasnoexisten.md": "_posts/2020-02-04-la-humanidad-del-genoma.md",
    "_posts/2021-02-06-Agile.md": "_posts/2020-02-06-agile-manifesto.md",
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.titles = []
        self.meta = {}
        self.links = []
        self.imgs = []
        self.jsonld = []
        self._in_title = False
        self._in_jsonld = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title, self._buf = True, []
        elif tag == "meta":
            key = a.get("name") or a.get("property") or a.get("http-equiv")
            if key:
                self.meta[key.lower()] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_jsonld, self._buf = True, []

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self.titles.append("".join(self._buf).strip())
            self._in_title = False
        elif tag == "script" and self._in_jsonld:
            self.jsonld.append("".join(self._buf))
            self._in_jsonld = False

    def handle_data(self, data):
        if self._in_title or self._in_jsonld:
            self._buf.append(data)

    def link(self, rel):
        return [l for l in self.links if rel in (l.get("rel") or "").split()]


class Source:
    """Lee archivos del build local o URLs del sitio publicado."""

    def __init__(self, target):
        self.remote = target.startswith("http")
        self.target = target.rstrip("/")

    def get(self, path):
        """Devuelve (status, bytes) para una ruta del sitio, p. ej. '/about/'."""
        if self.remote:
            req = urllib.request.Request(self.target + path, headers={"User-Agent": "seo-check/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as e:
                return e.code, b""
        rel = urllib.parse.unquote(path).lstrip("/")
        if rel == "" or rel.endswith("/"):
            rel += "index.html"
        f = os.path.join(self.target, rel)
        if not os.path.isfile(f):
            return 404, b""
        with open(f, "rb") as fh:
            return 200, fh.read()


def jpeg_size(data):
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg_len
    return None


def ico_sizes(data):
    _, _, count = struct.unpack("<HHH", data[:6])
    sizes = []
    for n in range(count):
        w, h = data[6 + 16 * n], data[7 + 16 * n]
        sizes.append((w or 256, h or 256))
    return sizes


def front_matter_body(text):
    m = re.match(r"---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


class Report:
    def __init__(self):
        self.failures = 0

    def check(self, code, ok, msg):
        print(f"  [{'OK' if ok else 'FALLA'}] {code} {msg}")
        if not ok:
            self.failures += 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="carpeta _site o URL base del sitio")
    ap.add_argument("--git-base", help="commit original para verificar CA10 (correr desde la raíz del repo)")
    args = ap.parse_args()

    src = Source(args.target)
    rep = Report()

    status, sitemap = src.get("/sitemap.xml")
    if status != 200:
        sys.exit(f"No se pudo leer sitemap.xml ({status})")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in ET.fromstring(sitemap).findall("s:url/s:loc", ns)]
    paths = [u[len(SITE_URL):] or "/" for u in urls]
    print(f"Sitemap: {len(paths)} URLs\n")

    titles, descriptions, pages = {}, {}, {}
    for path in paths:
        print(path)
        status, body = src.get(path)
        rep.check("CA1", status == 200, f"responde {status}")
        if status != 200:
            continue
        p = Page()
        p.feed(body.decode("utf-8"))
        pages[path] = p
        desc = p.meta.get("description", "")
        canon = [l.get("href") for l in p.link("canonical")]
        rep.check("CA1", len(p.titles) == 1, f"un <title>: {p.titles}")
        rep.check("CA1", 50 <= len(desc) <= 170, f"description de {len(desc)} caracteres")
        rep.check("CA1", canon == [SITE_URL + path], f"canonical {canon}")
        rep.check("CA3", "%" not in path and path == path.lower(), "URL sin % ni mayúsculas")
        if re.search(r"/\d{4}/\d{2}/\d{2}/", path):
            rep.check("CA3", False, "post fuera de /blog/")
        titles.setdefault(p.titles[0] if p.titles else "", []).append(path)
        descriptions.setdefault(desc, []).append(path)

        # CA2: un único bloque JSON-LD con la persona
        rep.check("CA2", len(p.jsonld) == 1, f"{len(p.jsonld)} bloque(s) JSON-LD")
        graph = []
        try:
            graph = json.loads(p.jsonld[0])["@graph"]
        except (IndexError, KeyError, ValueError) as e:
            rep.check("CA2", False, f"JSON-LD inválido: {e}")
        by_type = {}
        for node in graph:
            by_type.setdefault(node.get("@type"), []).append(node)
        person = (by_type.get("Person") or [{}])[0]
        same_as = " ".join(person.get("sameAs", []))
        rep.check("CA2", person.get("name") == PERSON_NAME, f"Person.name = {person.get('name')!r}")
        rep.check("CA2", all(h in same_as for h in SAME_AS_HOSTS), "sameAs con LinkedIn, GitHub y X")
        if path == "/about/":
            prof = (by_type.get("ProfilePage") or [{}])[0]
            rep.check("CA2", prof.get("mainEntity", {}).get("@id") == person.get("@id"), "ProfilePage → Person")
        if path.startswith("/blog/"):
            post = (by_type.get("BlogPosting") or [{}])[0]
            rep.check("CA2", post.get("author", {}).get("name") == PERSON_NAME, "BlogPosting con autora")
            rep.check("CA2", bool(post.get("datePublished")), "BlogPosting con datePublished")

        # CA6 / CA7
        rep.check("CA6", any("favicon.ico" in (l.get("href") or "") for l in p.link("icon")), "declara favicon")
        for img in p.imgs:
            rep.check("CA7", bool((img.get("alt") or "").strip()), f"alt en {img.get('src')}")
        if path == "/about/":
            rep.check("CA7", all(i.get("width") and i.get("height") for i in p.imgs), "foto con width/height")
        if path in ENGLISH_PAGES:
            rep.check("CA9", p.lang == "en", f'<html lang="{p.lang}">')
        print()

    print("Sitio")
    dup_t = {t: ps for t, ps in titles.items() if len(ps) > 1}
    dup_d = {d: ps for d, ps in descriptions.items() if len(ps) > 1}
    rep.check("CA1", not dup_t, f"títulos únicos {dup_t or ''}")
    rep.check("CA1", not dup_d, f"descripciones únicas {list(dup_d.values()) or ''}")

    for old, new in REDIRECTS.items():
        status, body = src.get(old)
        html = body.decode("utf-8", "replace")
        ok = status == 200 and 'http-equiv="refresh"' in html and SITE_URL + new in html
        rep.check("CA4", ok, f"{urllib.parse.unquote(old)} → {new}")
        rep.check("CA4", SITE_URL + old not in [SITE_URL + p for p in paths], f"{urllib.parse.unquote(old)} fuera del sitemap")

    rep.check("CA5", src.get("/README.md")[0] == 404, "README.md no publicado")

    status, ico = src.get("/favicon.ico")
    sizes = ico_sizes(ico) if status == 200 else []
    rep.check("CA6", any(w % 48 == 0 and w == h for w, h in sizes), f"favicon.ico {sizes}")

    home = pages.get("/")
    og = home.meta.get("og:image", "") if home else ""
    status, img = src.get(og[len(SITE_URL):]) if og.startswith(SITE_URL) else (404, b"")
    dims = jpeg_size(img) if status == 200 else None
    rep.check("CA8", dims == (1200, 675) and len(img) < 200 * 1024, f"og:image {og} {dims} {len(img) // 1024} KB")

    if args.git_base:
        for old, new in RENAMED_POSTS.items():
            before = subprocess.run(["git", "show", f"{args.git_base}:{old}"], capture_output=True, text=True).stdout
            with open(new, encoding="utf-8") as fh:
                after = fh.read()
            rep.check("CA10", front_matter_body(before) == front_matter_body(after), f"cuerpo intacto: {new}")

    print(f"\n{'Todo OK' if not rep.failures else str(rep.failures) + ' falla(s)'}")
    sys.exit(1 if rep.failures else 0)


if __name__ == "__main__":
    main()
