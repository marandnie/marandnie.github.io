# Spec 001 — SEO de mandieto.com.ar

- **Estado:** implementada (pendiente de publicar y medir)
- **Fecha:** 2026-10-06
- **Referencia:** [Guía de optimización en buscadores (SEO) para principiantes — Google Search Central](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- **Dueña:** Marina Nieto

## 1. Objetivo

Que quien busque **"Marina Nieto"** junto con **FinOps** (o su trabajo en costos de nube) encuentre este sitio, y que Google entienda sin ambigüedad quién es la autora: su rol, dónde trabaja, su trayectoria y sus perfiles en otros sitios.

Objetivo secundario: dejar la base técnica sana (URLs, metadatos, imágenes, duplicados) para que cada post nuevo salga bien indexado sin trabajo extra.

## 2. Decisiones de Marina (clarificación, 2026-10-06)

| # | Pregunta | Decisión |
|---|----------|----------|
| D1 | Nombre y título del sitio | Se mantiene el título **"El sitio web de Marina"**. El nombre a usar es **"Marina Nieto"** (sin "Andrea"). El rol va en la **descripción** y en **About**. |
| D2 | Datos profesionales públicos | Empleador actual (Gire S.A.), trayectoria (Accenture, Mercado Libre, TIVIT LATAM), certificación de la FinOps Foundation y estudios en UNSAM. |
| D3 | LinkedIn | Enlazar https://www.linkedin.com/in/marandnie/ |
| D4 | Posts de 2020 | Se dejan como están (contenido intacto). Solo se arreglan URLs, idioma y metadatos. |

## 3. Auditoría del estado actual (2026-10-06)

| Área de la guía | Hallazgo | Severidad |
|---|---|---|
| Que Google entienda quién sos | Ninguna página dice "FinOps". El About habla de una estudiante; no hay trayectoria ni LinkedIn. En una búsqueda de prueba de nombre + FinOps el sitio no aparece. | Alta |
| Datos estructurados | Solo hay un `WebSite` genérico. No hay `Person` ni `ProfilePage`; los posts no declaran autora. | Alta |
| Descripción (meta description) | Una sola descripción genérica para todo el sitio; no menciona nombre ni rol. Las páginas internas no tienen descripción propia. | Media |
| URLs | `/biolog%C3%ADa/2020/02/05/Lasrazasnoexisten.html` tiene caracteres codificados; los slugs (`newpost`, `Agile`) no describen el contenido; los nombres de archivo dicen 2021 y los posts son de 2020. | Media |
| Contenido duplicado | `/spd/` y `/spd/primer-parcial/` son el mismo quiz (solo difiere un emoji). | Media |
| Archivos expuestos | `README.md` del repo se publica como página (`/README.md` responde 200). | Baja |
| Imágenes | La foto del About se sirve desde `raw.githubusercontent.com`, con alt genérico y sin dimensiones. La imagen para compartir (`Marina.jpg`) pesa 667 KB a 2560×1440. | Media |
| Favicon | No hay favicon (Google lo muestra junto al resultado). | Media |
| Idioma | El sitio es `es-AR`, pero el post del Manifiesto Ágil está en inglés y se declara como español. "About", la página 404 y "subscribe via RSS" están en inglés. | Baja |
| Rastreo | `robots.txt` y `sitemap.xml` existen y funcionan. HTTPS y redirecciones `www` → raíz y `http` → `https` correctas. | OK |
| Mobile | El tema minima es responsive. | OK |

## 4. Historias de usuaria

- **H1.** Como reclutadora que busca "Marina Nieto FinOps", quiero encontrar su sitio y ver de inmediato su rol, su empresa y su trayectoria.
- **H2.** Como Google, quiero datos estructurados coherentes (Person + ProfilePage + BlogPosting) para asociar el sitio, LinkedIn, GitHub y X a la misma persona.
- **H3.** Como lectora que llega desde un link viejo, quiero que la URL antigua me lleve a la nueva sin un 404.
- **H4.** Como Marina, quiero que un post nuevo herede automáticamente URL limpia, autora, descripción e imagen, sin tocar código.

## 5. Requisitos

Cada requisito indica la sección de la guía de Google de la que sale.

### Identidad y contenido (guía: *Make your site interesting and useful*)

- **R1.** El About presenta a Marina Nieto como FinOps Analyst en Gire S.A. (Buenos Aires), con un resumen de lo que hace, la trayectoria (D2), la formación y el contacto (email y LinkedIn).
- **R2.** La descripción del sitio (meta description de la home y texto del pie) menciona "Marina Nieto" y su rol FinOps.
- **R3.** El título del sitio sigue siendo "El sitio web de Marina" (D1). El About usa como título "Marina Nieto — FinOps Analyst" y en el menú se lee "Sobre mí".
- **R4.** El contenido de los posts de 2020 no se modifica (D4).

### Cómo se ve en Google (guía: *Influence how your site looks in Google Search*)

- **R5.** Cada página indexable tiene `<title>` y `meta description` **únicos**.
- **R6.** El sitio tiene favicon (ICO 48×48 multiresolución + SVG + apple-touch-icon), declarado en el `<head>`.
- **R7.** Datos estructurados JSON-LD en un único `@graph` por página:
  - `WebSite` y `Person` en todas las páginas, con `@id` estables (`/#website`, `/#person`).
  - `Person`: `name` "Marina Nieto", `jobTitle`, `worksFor`, `alumniOf`, `hasCredential`, `knowsAbout`, `image` y `sameAs` (LinkedIn, GitHub, X).
  - About → `ProfilePage` con `mainEntity` = la persona.
  - Posts → `BlogPosting` con `author` = la persona, `datePublished`, `image` e `inLanguage`.
  - Resto → `WebPage`.
  - Sin bloques duplicados ni contradictorios (se elimina el JSON-LD automático de jekyll-seo-tag y el microdata del layout `post`).

### Organización (guía: *Organize your site*)

- **R8.** Los posts usan URLs descriptivas, sin caracteres codificados: `/blog/<slug>/`.
- **R9.** Cada URL vieja de post redirige a la nueva (H3).
- **R10.** Un solo URL por contenido: `/spd/` redirige a `/spd/primer-parcial/` (la versión corregida), que queda como canónica.
- **R11.** `README.md`, `specs/` y archivos de desarrollo no se publican.
- **R12.** El sitemap lista solo URLs canónicas (sin páginas de redirección ni 404).

### Imágenes (guía: *Optimize your images*)

- **R13.** La foto del About se sirve desde el propio dominio, con nombre de archivo descriptivo, `alt` descriptivo y `width`/`height`.
- **R14.** La imagen para compartir en redes es de 1200×675 y pesa menos de 200 KB.

### Idioma

- **R15.** El post en inglés declara `lang="en"`. Los textos de interfaz del sitio (404, RSS, fechas) están en castellano.

### Fuera del sitio (guía: *Next steps* y *Promote your website*)

- **R16.** Search Console verificado (propiedad de dominio), sitemap enviado y URLs clave inspeccionadas.
- **R17.** Los perfiles de LinkedIn, GitHub y X enlazan a mandieto.com.ar (cierra el círculo de `sameAs`).

## 6. Criterios de aceptación

Verificables con `specs/001-seo/seo_check.py` (contra el build local o contra el sitio publicado):

- **CA1.** Cada página del sitemap responde 200, tiene un solo `<title>`, `meta description` no vacía de 50 a 170 caracteres y `canonical` absoluto que apunta a sí misma. Títulos y descripciones no se repiten entre páginas.
- **CA2.** Cada página tiene exactamente un bloque JSON-LD válido con `Person` "Marina Nieto" y `sameAs` con LinkedIn, GitHub y X. `/about/` incluye `ProfilePage`; cada post incluye `BlogPosting` con `author`.
- **CA3.** Ninguna URL del sitemap contiene `%` ni mayúsculas; los posts están bajo `/blog/`.
- **CA4.** Las 3 URLs viejas de posts y `/spd/` devuelven una página de redirección hacia la URL nueva (meta refresh + canonical).
- **CA5.** `/README.md` no existe en el build.
- **CA6.** `/favicon.ico` existe, declarado en el `<head>`, de 48×48 o múltiplo.
- **CA7.** Todas las `<img>` tienen `alt` no vacío; la del About tiene `width` y `height`.
- **CA8.** La imagen `og:image` existe, mide 1200×675 y pesa < 200 KB.
- **CA9.** El post del Manifiesto Ágil tiene `<html lang="en">`.
- **CA10.** El cuerpo de los 3 posts de 2020 es idéntico al original (D4).
- **CA11.** (Manual, post-publicación) Rich Results Test sin errores para `/about/` y un post; Search Console sin errores de cobertura en 4 semanas.

## 7. Métricas de éxito (Search Console, a 8–12 semanas)

- El sitio aparece para la consulta "marina nieto finops" (impresiones > 0, posición media en primera página).
- `/about/` indexada y mostrada con el favicon.
- 0 páginas con "Duplicada sin canónica seleccionada por el usuario".

## 8. Fuera de alcance

- Reescribir o despublicar los posts de 2020 (D4).
- Los sitios en subdominios (`cine.`, `tramoya.`) y los proyectos servidos desde otros repos (`/hex-calculator/`, `/vitamin-d-iu-calculator/`): tienen su propio HTML y su propio SEO.
- Cambiar de tema o de generador.

## 9. Preguntas abiertas

- **P1.** El link "B12" de Trabajos apunta a la home y no hay ninguna página B12 publicada. ¿Qué proyecto es? Hasta definirlo, queda como está.
- **P2.** Nombre exacto de la certificación de la FinOps Foundation (p. ej. *FinOps Certified Practitioner*). Hoy figura de forma genérica en `_data/person.yml`.
