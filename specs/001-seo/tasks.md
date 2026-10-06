# Tareas — Spec 001 SEO

`[x]` hecho · `[ ]` pendiente · `(Rn)` requisito · `(CAn)` criterio de aceptación

## Fase 1 — Base técnica

- [x] T01 `_config.yml`: `author`, descripción con nombre y rol, `linkedin_username`, `timezone`, `permalink: /blog/:title/`, `jekyll-redirect-from`, `exclude`, formato de fecha, imagen por defecto con dimensiones. (R2, R8, R11)
- [x] T02 `Gemfile`: sumar `jekyll-redirect-from` para builds locales.
- [x] T03 `_data/person.yml` con los datos de identidad (D1–D3). (R1, R7)

## Fase 2 — Head y datos estructurados

- [x] T04 `_includes/head.html`: `{% seo %}` sin su JSON-LD + `schema.html` + favicons. (R5, R6, R7)
- [x] T05 `_includes/schema.html`: `@graph` con WebSite, Person y ProfilePage / BlogPosting / WebPage. (R7, CA2)
- [x] T06 `_layouts/post.html`: quitar microdata duplicado, mostrar autora. (R7)
- [x] T07 `_includes/header.html`: soporte de `nav_title`. (R3)
- [x] T08 `_layouts/home.html`: textos en castellano. (R15)

## Fase 3 — Contenido e identidad

- [x] T09 `about.md`: bio FinOps, trayectoria, formación, contacto, foto local con alt; `title` + `nav_title` + `description`. (R1, R3, R13, CA7)
- [x] T10 `trabajos.md`: descripción propia, link directo al quiz de SPD, link al About. (R5, R10)
- [x] T11 `404.html` en castellano con link a la home. (R15)

## Fase 4 — URLs y duplicados

- [x] T12 Renombrar los 3 posts (slug descriptivo, fecha 2020) + `redirect_from` + `description`; `lang: en` en el Manifiesto Ágil. Cuerpo sin cambios. (R4, R8, R9, R15, CA3, CA4, CA9, CA10)
- [x] T13 Borrar `spd/index.html`; `redirect_from: /spd/` + título y descripción en `spd/primer-parcial/`. (R10, CA4)

## Fase 5 — Imágenes y favicon

- [x] T14 `assets/img/marina-nieto.jpg` y `assets/img/marina-nieto-og.jpg` (1200×675, < 200 KB). (R13, R14, CA8)
- [x] T15 `favicon.ico`, `favicon.svg`, `apple-touch-icon.png`. (R6, CA6)

## Fase 6 — Verificación

- [x] T16 `specs/001-seo/seo_check.py` (CA1–CA10).
- [x] T17 Build local con versiones de GitHub Pages en modo `safe` + `seo_check.py _site` en verde.

### Resultado de la verificación (2026-10-06)

| Contra | Fallas |
|---|---|
| Sitio publicado hoy (antes de los cambios) | 56 |
| Build local de esta rama (Jekyll 3.10.0, modo `safe`, plugins de GitHub Pages) | **0** (CA1–CA10 OK) |

## Fase 7 — Publicación y Search Console (Marina)

- [ ] T18 Publicar la rama `seo/001-plan-seo` en GitHub y mergearla a `main`.
- [ ] T19 Correr `python3 specs/001-seo/seo_check.py https://mandieto.com.ar` después del deploy. (CA1–CA9 en producción)
- [x] T20 Search Console: propiedad `mandieto.com.ar` creada y verificada (ya existía). (R16)
- [ ] T21 Search Console → Sitemaps → enviar `https://mandieto.com.ar/sitemap.xml`. (R16)
- [ ] T22 Inspección de URLs → solicitar indexación de `/` y `/about/`. (R16)
- [ ] T23 Rich Results Test de `https://mandieto.com.ar/about/` y de un post. (CA11)
- [ ] T24 Poner `https://mandieto.com.ar` en LinkedIn (Información de contacto → Sitio web), GitHub (Website del perfil) y X (bio). (R17)
- [ ] T25 Resolver la pregunta abierta P1 (link "B12"). P2 resuelta: FinOps Certified Practitioner.

## Fase 8 — Contenido (recomendado, continuo)

La guía de Google pone el contenido original y útil por encima de todo lo técnico. Hoy el sitio no tiene ningún post sobre FinOps, que es justamente lo que tiene que posicionar. Ideas basadas en tu experiencia:

- [ ] T26 Publicar el borrador de ART/CRISPR (ya tiene la sección "mirada FinOps").
- [ ] T27 Post: consultas útiles sobre AWS CUR 2.0 con Athena (con SQL de ejemplo).
- [ ] T28 Post: Savings Plans vs. Reserved Instances: cómo decidir, con números de ejemplo.
- [ ] T29 Post: cómo armar un reporte de costos por unidad de negocio (tags, asignación de costos compartidos).
- [ ] T30 Post: FinOps multi-cloud: lo que aprendí comparando AWS, GCP, Azure, Huawei e IBM Cloud.

Con 1 post por mes alcanza; lo importante es que sea propio y concreto.

## Fase 8b — Privacidad de la foto (Marina)

Llegan visitas desde IDCrawl (buscador de personas que junta fotos y perfiles públicos).

- [ ] T33 Reemplazar la foto por una ilustración propia **con los mismos nombres de archivo**: `assets/img/marina-nieto.jpg` (960×540, About + schema) y `assets/img/marina-nieto-og.jpg` (1200×675, redes). Actualizar el `alt` en `about.md`.
- [ ] T34 Borrar las fotos viejas que siguen publicadas: `Marina.jpg` y `pelo.jpg` en la raíz del repo.
- [ ] T35 Después del deploy, en Search Console → Eliminaciones → Nueva solicitud → Eliminación temporal, cargar las URLs viejas de las fotos (`/Marina.jpg`, `/pelo.jpg`). Como van a dar 404, Google las saca del todo al volver a rastrearlas.
- [ ] T36 Pedir la baja del perfil en `idcrawl.com/remove-my-information`.

## Fase 9 — Medición

- [ ] T31 A las 4 semanas: Search Console → Páginas (cobertura) sin errores.
- [ ] T32 A las 8–12 semanas: Rendimiento → consultas con "marina nieto" y "finops". Comparar con las métricas de éxito de la spec.
