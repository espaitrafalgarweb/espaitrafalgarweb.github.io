# espaitrafalgar.coop

Web estàtica d'una sola pàgina de l'Espai Trafalgar, el futur espai cooperatiu del carrer de
Trafalgar, 12, de Barcelona que impulsen Arç Cooperativa, Som Connexió, Sostre Cívic i Crític.

El text de la pàgina és el que va lliurar Crític i no s'hi ha afegit copy nou. Les imatges són una
tria de quatre fotografies i renders del material que va passar el client.

## Requisits

Node ^20.19.0 o >=22.12.0, i Python 3 amb Pillow si cal tornar a generar les imatges.

## Ordres

```
npm install          # instal·la Vite, Tailwind i les fonts
npm run dev          # servidor de desenvolupament
npm run build        # compila a dist/
npm run preview      # serveix dist/ per comprovar-lo
npm run images       # regenera public/img a partir de source-assets/
```

## Com està fet

Vite 8 compila la pàgina i Tailwind CSS 4 genera el full d'estil, sense CDN. El tema (colors,
tipografies i escala de text) es declara amb `@theme` a `src/styles.css`, i els dos únics
components propis són les dues classes d'enllaç.

Les tipografies són Archivo per als titulars i Newsreader per al text, totes dues amb llicència
Open Font License. Se serveixen des del mateix domini, en format woff2 variable i només amb el
subconjunt latin, que ja cobreix els diacrítics catalans i el punt volat de l'ela geminada. Els
fitxers són a `public/fonts/` i provenen dels paquets `@fontsource-variable/archivo` i
`@fontsource-variable/newsreader`.

Les imatges es generen amb `tools/build-images.py`, que retalla, redimensiona i escriu cada mida en
AVIF, WebP i JPEG a `public/img/`. Els originals són a `source-assets/`, que no es versiona perquè
pesa 181 MB.

Els fitxers que han d'estar a l'arrel publicada són a `public/`: `robots.txt`, `llms.txt`,
`sitemap.xml`, `404.html`, `favicon.svg` i `.well-known/security.txt`. Vite els copia a `dist/`
sense tocar-los.

Les dades estructurades són un sol graf JSON-LD dins de `index.html`, amb Organization, Place,
WebSite i WebPage. Només declara el que la pàgina ensenya.

## Desplegament a GitHub Pages

El flux de treball `.github/workflows/deploy.yml` compila i desplega a cada push a `main`. Puja
l'artefacte amb `include-hidden-files: true`, que és el que fa que `.well-known/security.txt`
arribi al lloc publicat.

El domini propi es configura a Settings, Pages del repositori, no amb cap fitxer CNAME, perquè amb
un flux de treball propi GitHub ignora aquest fitxer. Al proveïdor de DNS, que en aquest cas és
Gandi, cal declarar per al domini sense subdomini quatre registres A cap a 185.199.108.153,
185.199.109.153, 185.199.110.153 i 185.199.111.153, i quatre registres AAAA cap a
2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153 i 2606:50c0:8003::153. Quan GitHub
validi el domini, cal marcar Enforce HTTPS.

## Comprovacions d'accessibilitat

La pàgina s'ha comprovat amb axe-core 4.14 contra les regles WCAG 2.2 de nivell A i AA, a 1280 i a
320 píxels d'amplada, i amb els quatre valors d'espaiat de text del criteri 1.4.12 aplicats. Per
repetir-ho:

```
npm run build
cp node_modules/axe-core/axe.min.js dist/axe.min.js
cd dist && python3 -m http.server 8788
```

i executar `axe.run()` des de la consola del navegador amb el fitxer carregat. Cal esborrar
`dist/axe.min.js` abans de desplegar, o tornar a compilar.
