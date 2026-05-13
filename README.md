# GBC Kiosko (Game Boy Color en navegador, un solo juego)

Página web minimalista que ejecuta **un ROM específico de Game Boy Color** y
no le da al usuario ninguna otra opción: no hay selector de archivos, no hay
menú, no hay forma de cargar otro juego. Solo la pantalla del emulador y los
controles por teclado.

Emulador usado: [GameBoy-Online](https://github.com/taisel/GameBoy-Online) de
Grant Galitz (JavaScript puro, sin dependencias). Cargado desde jsDelivr CDN.

## Estructura

    gbc-kiosk/
    ├── index.html       ← la página kiosko
    ├── rom/
    │   └── game.gbc     ← TU ROM va acá (renombralo a game.gbc)
    ├── serve.py         ← servidor estático local para probar
    └── README.md

## Cómo usarlo

1. Poné tu ROM en `rom/game.gbc` (renombrá tu archivo si hace falta).
   También funciona con `.gb` — el contenido importa, no la extensión.
2. Servilo por HTTP. **No funciona abriéndolo con doble clic** (CORS bloquea
   `fetch()` desde `file://`). Opciones:
   - Local rápido: `python serve.py` y abrir <http://localhost:8000>
   - Node: `npx serve` dentro de la carpeta
   - PHP: `php -S localhost:8000`
   - Hosting estático: subí toda la carpeta a Netlify, Vercel, GitHub Pages,
     Cloudflare Pages, S3, etc.

## Controles por defecto

| Acción          | Tecla       |
|-----------------|-------------|
| D-pad           | Flechas     |
| A               | X           |
| B               | Z           |
| Start           | Enter       |
| Select          | Shift       |
| Pantalla compl. | F           |

Para cambiarlos, editá el array `settings[14]` en `index.html`. Es el orden:
`[Right, Left, Up, Down, A, B, Select, Start]` con `keyCode` de cada tecla.

## Modo kiosko más estricto

El HTML ya bloquea:

- Click derecho / menú contextual
- Drag & drop (no se puede soltar otro ROM encima)
- Selección de texto
- Atajos con Ctrl/Cmd

Para un kiosko de verdad (tablet o PC dedicada):

- **Chrome en modo kiosko**: `chrome --kiosk http://localhost:8000`
  (pantalla completa real, sin barra, sin atajos del sistema).
- En tablets, usá el modo "App fija" / "Guided Access" del sistema operativo
  para que no puedan salir de Chrome.

## Personalizar el ROM

Si querés que el ROM tenga otro nombre o ruta, cambiá esta línea en
`index.html`:

```js
var ROM_PATH = 'rom/game.gbc';
```

## Embebido en un único archivo (opcional)

Si querés todo en un solo `.html` sin carpeta `rom/`, podés embeber el ROM en
base64 dentro del HTML. Es práctico para distribución pero el archivo se
vuelve grande y se ve raro en el navegador (puede ralentizar la carga).
Avisame si querés que te lo arme así.

## Aclaración legal

Solo usalo con ROMs que poseas legalmente (cartuchos propios dumpeados) o
con homebrew libre. Distribuir ROMs comerciales sin permiso del titular es
ilegal en la mayoría de jurisdicciones.
