# Arcadia — Datos y estadísticas

## Dónde están los datos

### 1. Firebase Console
**URL:** https://console.firebase.google.com → proyecto `arcade-saves`

#### Usuarios registrados → `Firestore → users`
Cada usuario que inicia sesión con Google genera un documento:
```
users/{uid}/
  name:       "Nicolas Alarcon"
  email:      "nico@gmail.com"
  photo:      "https://..." (foto de Google)
  verified:   true
  createdAt:  timestamp
  verifiedAt: timestamp (si quitó publicidad)
```

#### Tickets de soporte → `Firestore → tickets`
Cada mensaje enviado desde el botón "Sugerencias y soporte":
```
tickets/{auto-id}/
  tipo:      "sugerencia" | "bug" | "juego" | "otro"
  mensaje:   "texto del usuario"
  nombre:    "Nicolas Alarcon"
  email:     "nico@gmail.com"
  uid:       "firebase-uid"
  fecha:     "2026-05-21T..."
  createdAt: timestamp
```

#### Partidas guardadas → `Firestore → saves`
```
saves/{uid}/roms/{consola_juego}/
  state:     "base64..." (estado del emulador)
  sram:      "base64..." (save del juego)
  savedAt:   timestamp
```

#### Usuarios autenticados → `Authentication → Usuarios`
Lista de todos los que iniciaron sesión con Google:
- Email, nombre, foto
- Último inicio de sesión
- Fecha de creación
- UID

---

### 2. Google Sheets
**Cómo acceder:** Abrí el Google Apps Script → en el menú arriba click en el nombre del proyecto → "Spreadsheet" vinculado

Contiene:
- Fecha, nombre y email de cada registro
- Tickets enviados (columnas: acción, tipo, mensaje, nombre, email)

---

### 3. Firebase Auth — Estadísticas de uso
**Firebase Console → Authentication → Uso**
- Usuarios activos diarios / semanales / mensuales
- Nuevos usuarios por día
- Métodos de autenticación usados

---

## Qué más podés capturar para analítica

### Opción A — Google Analytics 4 (recomendado, gratis)
Agregá este snippet en el `<head>` del index.html:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```
Reemplazá `G-XXXXXXXXXX` con tu ID de GA4 (gratis en analytics.google.com).

Te da automáticamente:
- Usuarios únicos por día/semana/mes
- Dispositivos (celular vs escritorio)
- País y ciudad
- Duración promedio de sesión
- Páginas más visitadas
- Fuentes de tráfico (¿de dónde llegan?)

### Eventos personalizados que podés trackear en GA4
Agregá `gtag('event', ...)` en el código para rastrear acciones específicas:

```javascript
// Consola seleccionada
gtag('event', 'consola_seleccionada', { consola: 'NES' });

// Juego iniciado
gtag('event', 'juego_iniciado', { consola: 'GB', juego: 'Pokemon Crystal' });

// Login con Google
gtag('event', 'login', { method: 'Google' });

// Publicidad quitada
gtag('event', 'no_ads_activado');

// Partida guardada
gtag('event', 'partida_guardada', { consola: 'NES', juego: 'Contra' });

// Ticket de soporte enviado
gtag('event', 'ticket_enviado', { tipo: 'sugerencia' });
```

### Opción B — Firestore como base de analítica propia
Sin herramientas externas, guardando eventos en Firestore:

```
events/{auto-id}/
  tipo:     "game_played" | "console_selected" | "login" | "no_ads"
  consola:  "NES"
  juego:    "Contra (U)"
  uid:      "..."
  sesion:   "session-random-id"
  ts:       timestamp
  device:   "mobile" | "desktop"
  screen:   "768x1024"
```

Colección sugerida: `events` — podés consultarla con filtros en Firestore.

### Qué comportamientos analizar

| Dato | Para qué sirve |
|------|---------------|
| Juego más iniciado | Saber qué contenido es más popular |
| Consola más usada | Decidir si agregar más ROMs de esa consola |
| Tasa de conversión Google login | ¿Cuántos visitantes se registran? |
| Tasa de no-ads | ¿Cuántos quitan publicidad? |
| Duración de sesión | ¿Cuánto tiempo juegan? |
| Horario de uso | ¿Cuándo hay más tráfico? (para mantenimiento) |
| Dispositivo | ¿Optimizar para mobile o desktop? |
| País | ¿Dónde está el público? |
| Juegos que fallan | ROMs que disparan el hint de "Reiniciar consola" |
| Tickets por tipo | ¿Qué piden los usuarios? |

---

## Cómo implementar GA4 paso a paso

1. Ir a https://analytics.google.com
2. Crear cuenta → crear propiedad "Arcadia"
3. Configurar flujo de datos → Web → ingresar `nicolasdmo.github.io`
4. Copiar el ID de medición (`G-XXXXXXXXXX`)
5. Agregar el snippet al `<head>` de `index.html`
6. Verificar en GA4 → Informes → Tiempo real (debería aparecer tu visita)

Con esto tenés un panel completo gratis de tráfico, usuarios y comportamiento.

---

## Resumen de dónde ver cada cosa

| Dato | Dónde |
|------|-------|
| Usuarios registrados | Firebase → Firestore → `users` |
| Quiénes se loguearon | Firebase → Authentication → Usuarios |
| Tickets de soporte | Firebase → Firestore → `tickets` |
| Partidas guardadas | Firebase → Firestore → `saves` |
| Registros históricos | Google Sheets (via Apps Script) |
| Tráfico y sesiones | Google Analytics 4 (si lo configurás) |
| Eventos de juego | Firebase → Firestore → `events` (si lo implementás) |
