#!/usr/bin/env python3
import re
import sys
from datetime import datetime

SQL_INJECTION_PATTERNS = [
    (r"'\s*OR\s*'?1'?\s*=\s*'?1", "Bypass de autenticación clásico (OR 1=1)"),
    (r"'\s*--",                    "Comentario SQL para ignorar contraseña"),
    (r"UNION\s+SELECT",            "Inyección UNION para extraer datos"),
    (r"DROP\s+TABLE",              "Intento de eliminar tabla (Destructivo)"),
    (r"EXEC\s*\(",                 "Ejecución de comandos del sistema"),
    (r"INSERT\s+INTO.*SELECT",     "Inyección de datos desde otra tabla"),
]

def analyze_log_file(log_path):
    incidents = []
    total_lines = 0
    suspicious_lines = 0

    try:
        with open(log_path, 'r', encoding='utf-8') as log_file:
            for line_number, line in enumerate(log_file, start=1):
                total_lines += 1
                line = line.strip()
                if not line:
                    continue
                for pattern, description in SQL_INJECTION_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        suspicious_lines += 1
                        incidents.append({
                            'line_number': line_number,
                            'content': line,
                            'attack_type': description
                        })
                        break
    except FileNotFoundError:
        print(f"[ERROR] Archivo no encontrado: {log_path}")
        sys.exit(1)
    except PermissionError:
        print(f"[ERROR] Sin permiso para leer: {log_path}")
        sys.exit(1)

    return {
        'total_lines': total_lines,
        'suspicious_lines': suspicious_lines,
        'clean_lines': total_lines - suspicious_lines,
        'incidents': incidents
    }

def print_report(results, log_path):
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"  REPORTE DE SEGURIDAD — FinTech Nova")
    print(f"  Archivo analizado : {log_path}")
    print(f"  Fecha de análisis : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{separator}")
    print(f"  Total líneas      : {results['total_lines']}")
    print(f"  Líneas limpias    : {results['clean_lines']}")
    print(f"  Incidentes        : {results['suspicious_lines']}")
    print(f"{separator}\n")

    if results['incidents']:
        print("  ⚠️  INCIDENTES DETECTADOS:")
        for i, incident in enumerate(results['incidents'], 1):
            print(f"  [{i}] Línea {incident['line_number']}: {incident['attack_type']}")
            print(f"       → {incident['content'][:80]}...")
    else:
        print("  ✅ No se detectaron incidentes. Logs limpios.")

    print(f"\n{separator}\n")

if __name__ == "__main__":
    log_file = "server.log"
    print(f"[INFO] Iniciando análisis de seguridad del archivo: {log_file}")
    results = analyze_log_file(log_file)
    print_report(results, log_file)