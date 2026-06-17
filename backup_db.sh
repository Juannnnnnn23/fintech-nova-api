#!/bin/bash
DB_FILE="database.db"
BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_NAME="backup_${TIMESTAMP}.tar.gz"

echo "[$(date '+%H:%M:%S')] Iniciando backup de FinTech Nova..."

if [ ! -f "$DB_FILE" ]; then
  echo "[ERROR] No se encontró el archivo: $DB_FILE"
  exit 1
fi

if [ ! -d "$BACKUP_DIR" ]; then
  echo "[INFO] Creando carpeta de backups: $BACKUP_DIR"
  mkdir -p "$BACKUP_DIR"
fi

echo "[INFO] Creando backup: $BACKUP_DIR/$BACKUP_NAME"
tar -czf "$BACKUP_DIR/$BACKUP_NAME" "$DB_FILE"

if [ $? -eq 0 ]; then
  BACKUP_SIZE=$(du -sh "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)
  echo "[OK] Backup completado exitosamente."
  echo "[OK] Archivo: $BACKUP_DIR/$BACKUP_NAME ($BACKUP_SIZE)"
else
  echo "[ERROR] El backup falló."
  exit 1
fi

BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 7 ]; then
  echo "[INFO] Limpiando backups antiguos..."
  ls -1t "$BACKUP_DIR"/*.tar.gz | tail -n +8 | xargs rm -f
fi

echo "[$(date '+%H:%M:%S')] Proceso de backup finalizado."