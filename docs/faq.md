# FAQ

**¿Puedo operar en REAL?**  
Sí, alterna en el panel o usa `switch_to_real()`. Requiere credenciales válidas y responsabilidad del usuario.

**¿Cómo entreno la recuperación?**  
Marca manualmente **WIN/LOSS** tras cada operación; `core/recovery.apply_result()` ajusta el pool.

**¿Dónde se guardan mis ajustes?**  
En `data/config.json` y `data/session.json`.

**¿Cómo agrego un plugin?**  
Pon un `.py` en `tools/` o en una carpeta registrada y llama `discover_plugins()`.
