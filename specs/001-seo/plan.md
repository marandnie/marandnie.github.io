# Plan técnico — Spec 001 SEO

## Restricciones de la plataforma

- **GitHub Pages "clásico"** construye con Jekyll **3.10** en modo `safe`: solo funcionan los plugins de la lista blanca. Los que usamos ya están en ella: `jekyll-seo-tag`, `jekyll-sitemap`, `jekyll-feed` y **`jekyll-redirect-from`** (nuevo).
- Tema **minima 2.5.1** (el que trae GitHub Pages). Se personaliza **sobrescribiendo includes y layouts** con archivos del mismo nombre en el repo; no hay hooks tipo `custom-head` en esta versión.
- En Jekyll 3.x, definir `exclude:` **reemplaza** la lista por defecto, así que hay que repetirla completa.
- GitHub Pages no permite redirecciones 301 del servidor. `jekyll-redirect-from` genera páginas con `meta refresh` a 0 s + `canonical`, que Google trata como redirección permanente.
- Cloudflare está delante de GitHub Pages (DNS + proxy). La verificación de Search Console por DNS (registro TXT) se hace ahí.

## Diseño

### Una sola fuente de datos de identidad → `_data/person.yml`

Nombre, rol, empresa, formación, credenciales, temas y perfiles (`sameAs`). El JSON-LD y el About leen de acá: para actualizar un dato se toca un solo archivo.

### `<head>` → `_includes/head.html` (override)

1. `{% seo %}` se captura y se recorta antes de su `<script type="application/ld+json">`. Así se conservan `title`, `description`, `canonical`, Open Graph y Twitter, pero se descarta su JSON-LD genérico (`WebSite` incluso en About y sin `Person`).
2. `{% include schema.html %}` → un único `@graph` (R7).
3. Favicons (R6) y `feed_meta`.

### Datos estructurados → `_includes/schema.html`

```
@graph
├── WebSite      @id /#website   publisher → /#person
├── Person       @id /#person    (de _data/person.yml)
└── según página:
    ├── /about/        → ProfilePage  mainEntity → /#person
    ├── layout: post   → BlogPosting  author → /#person
    └── resto          → WebPage      isPartOf → /#website
```

Todo string pasa por `jsonify` para escapar comillas y acentos.

### Layouts e includes sobrescritos

| Archivo | Cambio |
|---|---|
| `_includes/header.html` | El menú muestra `nav_title` si existe (About → "Sobre mí" en el menú, título SEO más largo). |
| `_layouts/post.html` | Se quita el microdata `itemscope BlogPosting` (duplicaba el JSON-LD sin autora). Se muestra la autora. Se conservan los microformatos `h-entry`. |
| `_layouts/home.html` | Textos en castellano ("Suscribite por RSS"). |

### URLs (R8–R10)

- `_config.yml`: `permalink: /blog/:title/` y `timezone: America/Argentina/Buenos_Aires`.
- Los posts se renombran con slug descriptivo y la fecha real (2020) en el nombre de archivo. Cada uno lleva `redirect_from` con su URL vieja exacta (la de `biología` con la tilde literal; Jekyll crea la carpeta y el servidor resuelve el `%C3%AD`).
- Se elimina `spd/index.html` (duplicado). `spd/primer-parcial/index.html` declara `redirect_from: /spd/`.
- Trabajos enlaza directo a `/spd/primer-parcial/`.

### Imágenes (R13–R14)

- `assets/img/marina-nieto.jpg`: copia de `pelo.jpg` (960×540, 86 KB) con nombre descriptivo, usada en About con `alt`, `width`, `height` y `height:auto`.
- `assets/img/marina-nieto-og.jpg`: `Marina.jpg` recortada y reducida a 1200×675, JPEG progresivo, < 200 KB. Es la imagen por defecto en `defaults` (con `width`/`height` para `og:image:width/height`).
- `Marina.jpg` y `pelo.jpg` se mantienen en la raíz para no romper enlaces externos existentes.

### Favicon (R6)

Monograma "M" blanco sobre círculo azul `#2a7ae2` (el azul de minima). Se genera con Pillow: `favicon.ico` (16/32/48), `favicon.svg` (mismo trazo en vector) y `apple-touch-icon.png` (180×180).

### Exclusiones (R11)

`exclude:` con la lista por defecto de Jekyll + `README.md` + `specs/`.

## Verificación

- Build local con las **mismas versiones que GitHub Pages** (Jekyll 3.10.0, minima 2.5.1, jekyll-seo-tag 2.8.0, jekyll-sitemap 1.4.0, jekyll-feed 0.17.0, jekyll-redirect-from 0.16.0) y `safe: true`.
- `specs/001-seo/seo_check.py` (solo biblioteca estándar de Python) valida CA1–CA10 contra `_site/` o contra el sitio publicado:

```bash
python3 specs/001-seo/seo_check.py _site                       # build local
python3 specs/001-seo/seo_check.py https://mandieto.com.ar     # producción
```

- Manual post-publicación: Rich Results Test (`/about/` y un post), inspección de URLs en Search Console.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Links externos a URLs viejas de posts | `redirect_from` con cada URL vieja exacta (CA4). |
| La redirección de la URL con tilde no resuelve en GitHub Pages | Se verifica en producción con `seo_check.py https://mandieto.com.ar`; si falla, se agrega la variante codificada. |
| Pérdida temporal de posiciones por el cambio de URLs | Bajo impacto: son 3 posts de 2020 con poco tráfico. |
| Override de minima desactualizado si GitHub Pages cambia de versión | Los overrides son pocos y chicos; minima 2.5.1 lleva años fija en GitHub Pages. |
