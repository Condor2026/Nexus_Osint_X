# Contribuir a Nexus_Osint_X

Gracias por interesarte por el proyecto. Antes de nada, una aclaración importante para que no perdamos el tiempo ninguno de los dos:

> **No se aceptan Pull Requests de código.**
>
> El código de Nexus_Osint_X es **100 % del autor**. Las ideas, los reportes de bugs y las sugerencias son bienvenidos y se agradecen; el código, no.

Esto es una decisión deliberada, no un olvido. El motivo está explicado abajo.

---

## Qué SÍ se acepta

- **Reportes de bugs**: algo no funciona como debería. Abre un issue con los pasos para reproducirlo.
- **Ideas y sugerencias**: una fuente nueva, una mejora de UX, un cambio en cómo se puntúa la severidad, una idea para el mapa…
- **Correcciones de documentación**: si el README tiene una errata, una instrucción confusa o un enlace roto, dilo. Eso no es código.
- **Avisos de seguridad**: **en privado**, siguiendo `SECURITY.md`. No abras un issue público con detalles explotables.
- **Crédito por una idea**: si tu sugerencia acaba implementada, se te acredita en el README (sección "Créditos") o en el commit, como tú prefieras.

## Qué NO se acepta

- **Pull Requests de código**. Ni grandes ni pequeños. Ni "solo un typo en un comentario". Si abres uno, se cerrará sin mergear.
- **Parches enviados por email o en un issue**. Mismo motivo: no se aceptan contribuciones de código por ninguna vía.
- **Snippets copiados de otros proyectos**. Aunque sean de licencia compatible, no se aceptan. El código es del autor.
- **Issues con "aquí tienes el fix"**. Si abres un issue y pegas el código que lo arregla, se agradece la intención, pero el issue se cerrará como "no se acepta código". Describe el problema y, si quieres, la idea de la solución; el código lo escribe el autor.

---

## Por qué no se aceptan PRs de código

Tres motivos, en orden de importancia:

1. **Claridad legal y de propiedad.** El código es 100 % del autor. Si se aceptara código de terceros, ese tercero pasaría a ser co-titular de su contribución, y relicenciar el proyecto (por ejemplo, para una versión futura con otra licencia) requeriría su permiso. El autor quiere mantener la puerta abierta a decidir el futuro del proyecto sin ataduras de terceros. No se usa un CLA porque no se acepta código; es más simple así.

2. **Seguridad.** Cada línea de código que entra en el proyecto es una línea que alguien tiene que revisar, entender y mantener. En un proyecto personal, sin equipo de revisión, aceptar código externo es un riesgo: una contribución maliciosa o simplemente descuidada puede abrir un agujero. El autor prefiere escribir él mismo lo que entra.

3. **Coherencia de estilo y arquitectura.** El proyecto está escrito con una estructura muy concreta (las secciones `§ 0` a `§ 15`, el modelo de datos, el flujo de barrido, el frontend). Mantener eso coherente es más fácil si una sola persona escribe el código. Las ideas se incorporan; el código lo escribe el autor a su manera.

Nada de esto es hostilidad hacia quien quiere contribuir. Es una decisión de diseño del proyecto. Si tienes una idea, se agradece de verdad; si tienes código, se agradece la intención, pero no se acepta.

---

## Cómo reportar un bug

Abre un issue en GitHub con:

- **Qué esperabas que pasara** y **qué pasó en realidad**.
- **Pasos para reproducirlo** (cuanto más concretos, mejor).
- **Versión de NEXUS** (commit o fecha) y **sistema** (SO, versión de Python).
- **Logs relevantes**: la consola donde corre `python nexus.py`. Si hay un error, pega el traceback completo. Si el log tiene claves de API, **bórralas antes de pegarlo**.
- **Captura de pantalla** si es un problema visual del dashboard.

No hace falta que sepas arreglarlo. Con que sepas describirlo, es suficiente.

## Cómo sugerir una idea

Abre un issue con la etiqueta `idea` (o pon "Idea:" en el título). Explica:

- **Qué problema resuelve** o **qué mejora aporta**.
- **Cómo lo imaginas** (aunque sea en dos frases).
- **Si es una fuente nueva**: enlace a la fuente, si es pública o requiere clave, y qué tipo de eventos aportaría.

No prometas plazos. El autor tiene tiempo limitado y prioriza lo que puede. Si la idea entra, se te acredita.

## Cómo avisar de un problema de seguridad

**No abras un issue público.** Sigue `SECURITY.md`: usa GitHub Security Advisories o el email de contacto del perfil. Ahí se explica el alcance y qué esperar.

---

## Créditos

Las ideas que acaban implementadas se acreditan en el README, en la sección "Créditos", con el nombre o alias que indiques. Si no quieres aparecer, dilo y no apareces. El mérito es tuyo; el código, del autor.

---

## Resumen en una línea

**Ideas: sí. Bugs: sí. Código: no.** Gracias por respetarlo.

- Condor2026.
