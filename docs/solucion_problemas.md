# Solución de problemas

## No conecta a IQ Option
- Verifica credenciales (correo/contraseña).
- Revisa si hay 2FA o captchas.
- Prueba `switch_to_demo()` primero.

## Clics no hacen efecto
- Verifica coordenadas y que la ventana esté en primer plano.
- Desactiva superposiciones (Game Bar, overlays).
- Comprueba permisos de accesibilidad.

## Indicadores no coinciden
- Checa el `interval` y `count` de velas.
- Asegura timezone/locale.
- Valida fórmulas con valores de referencia.

## Recuperación sube mucho el stake
- Ajusta `recovery_margin` y `balance_cap`.
- Revisa `STAKE_MAX_FACTOR` en `core/state.py`.

## Build falla en Windows
- Usa Python 3.10–3.11.
- Instala C++ Build Tools si alguna lib lo requiere.
