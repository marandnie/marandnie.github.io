---
layout: post
title: "Una IA encontró repeticiones tipo CRISPR en virus: qué sabemos (y qué no)"
date: 2026-10-XX 10:00:00 -0300
categories: biologia
description: "Claude encontró ART, un sistema de enzimas con repeticiones parecidas a CRISPR. Qué es, cómo se encontró y por qué todavía no sabemos qué hace."
# image: /assets/img/art-crispr.png   # descomentar cuando exista la imagen
---

<!-- BORRADOR: los archivos en _drafts/ no se publican. Para publicarlo, movelo a _posts/
     con el nombre AAAA-MM-DD-ia-repeticiones-crispr.md y completá la fecha de arriba. -->

<!-- 1. Gancho: el momento en que el agente "ve a ojo" el patrón repetido en el ADN crudo.
     Anthropic publicó la frase textual y una animación del ADN que estaba leyendo. -->

## Qué es CRISPR y cómo se descubrió

<!-- Repeticiones y espaciadores, explicado simple.
     Ishino (1987): repeticiones raras en E. coli. Francisco Mojica (Univ. de Alicante, 2000):
     reconoce que repeticiones reportadas por separado comparten rasgos comunes.
     Paralelo: todo empezó con alguien notando algo raro en una secuencia.
     Linkear "La humanidad del genoma". -->

## Qué encontró Claude: el sistema ART

<!-- ART = array-associated reverse transcriptases, sobre todo en bacteriófagos.
     Tres partes: transcriptasa reversa (RT) + gen compañero + arreglo de repeticiones espaciadas.
     Explicar qué es una RT, qué es un bacteriófago y qué es un "jumbo phage".
     Matiz: la RT ya era conocida; lo nuevo es el arreglo no codificante y la proteína accesoria.
     Diagrama simple de las tres partes. -->

## Cómo se trabajó

<!-- Humanos: prompt inicial + trabajo de laboratorio. Agentes: leen bibliografía, reproducen
     resultados, buscan candidatos, escriben informes, se autocritican.
     ~950 agentes, 21 h, 210 M tokens; >200.000 RTs → 3.500 candidatos → 20 finalistas. -->

## Cuánto cuesta descubrir algo (mirada FinOps)

<!-- Tu ángulo propio: estimar el costo de 210 M tokens a precios públicos de API
     y compararlo con semanas/meses de trabajo de un experto. Aclarar supuestos
     (modelo, proporción input/output, caching). -->

## Lo que todavía no sabemos

<!-- Función desconocida. Preprint sin revisión por pares. La RT ya era conocida.
     No hay enzima de corte asociada. Poca evidencia de función tipo CRISPR;
     el arreglo se expresa como ARNs cortos distintos. -->

## Otras voces

<!-- Feng Zhang (MIT / Broad): ejemplo entusiasmante, los arreglos merecen más investigación.
     Contrapeso: la nota de Nature, más cauta. -->

## Por qué importa

<!-- Más que ART en sí, la forma nueva de hacer ciencia.
     Preguntas abiertas: ¿quién figura como descubridor? ¿Cómo se revisan miles de hipótesis generadas por IA? -->

## Fuentes

- [Claude discovers a novel enzyme system - Anthropic](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system)
- Preprint: <!-- link -->
- [Nature](https://www.nature.com/articles/d41586-026-03039-6)
- The Next Web: <!-- link -->
- [Francisco Mojica - Wikipedia](https://en.wikipedia.org/wiki/Francisco_Mojica)
- [Historia de CRISPR - PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9174617/)
