# Configuración

## `data/config.json`
Parámetros de ejecución (ejemplo):
```json
{
  "email": "tu_correo@dominio.com",
  "asset": "EURUSD-OTC",
  "stake_base": 1.0,
  "recovery_margin": 0.05,
  "coords": {"call": [x,y], "put": [x,y]},
  "mode": "demo"
}
```

- **email**: usuario de IQ Option.
- **asset**: activo por defecto.
- **stake_base**: monto base por operación.
- **recovery_margin**: extra para cubrir pérdidas con ganancia objetivo.
- **coords**: coordenadas absolutas para clics de CALL/PUT.
- **mode**: `demo` o `real`.

## `data/session.json`
Estado volátil (último balance, pérdidas acumuladas, flags).

## Variables en `core/state.py`
- Flags globales (pausa, modo, límites).
- Factores máximos de stake y protección de balance.
