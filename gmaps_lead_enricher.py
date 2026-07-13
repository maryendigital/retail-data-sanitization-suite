import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import shutil

# --- COLORES ANSI ---
ROJO = '\033[91m'
VERDE = '\033[92m'
AMARILLO = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

print(f"{CYAN}=============================================")
print("      CONVERTIDOR GOOGLE MAPS (ENLACES)      ")
print(f"============================================={RESET}\n")

def abrir_en_vscode(filepath):
    """Abre el archivo temporal utilizando Visual Studio Code."""
    try:
        subprocess.Popen(['code', filepath], shell=True)
    except Exception as e:
        print(f"{ROJO}Error al intentar abrir VS Code: {e}{RESET}")

def main():
    # 1. SELECCIÓN DE ARCHIVO (GUI HÍBRIDA)
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar el archivo CSV crudo",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )

    if not ruta_archivo:
        print(f"{AMARILLO}Operación cancelada. No se seleccionó ningún archivo.{RESET}")
        return

    archivo_temporal = "temp_gmaps_viewer.xlsx"

    # 2. FLUJO DE TRABAJO (CARGA Y PROCESAMIENTO)
    try:
        print(f"\n{CYAN}🧠 Procesando archivo y generando enlaces...{RESET}")
        
        # Leer el archivo CSV sin aplicar modificaciones de limpieza
        df = pd.read_csv(ruta_archivo)
        
        # Nombres de columnas definidos requeridos para el Excel
        nombres_esperados = ['NOMBRE', 'DIRECCION', 'TELEFONO', 'COMENTARIO', 'LINKWP', 'URL']
        
        # Ajustar la cantidad de columnas del DataFrame a las 6 especificadas
        columnas_actuales = list(df.columns)
        
        for i, nombre in enumerate(nombres_esperados):
            if i < len(columnas_actuales):
                columnas_actuales[i] = nombre
            else:
                # Crear la columna vacía si no existe en el CSV original
                df[nombre] = ""
                columnas_actuales.append(nombre)
                
        # Asignar los nuevos nombres a las columnas existentes
        df.columns = columnas_actuales[:len(df.columns)]
        
        # Asegurar que existan las columnas para realizar la concatenación
        if 'TELEFONO' in df.columns and 'LINKWP' in df.columns:
            # Construir el enlace inyectando el valor exacto de la columna TELEFONO
            url_parte1 = "https://api.whatsapp.com/send/?phone=%2B"
            url_parte2 = "&text&type=phone_number&app_absent=0"
            
            # La conversión a string (astype) garantiza que se pueda concatenar, 
            # manteniendo el dato exactamente como viene (sin limpiar caracteres).
            df['LINKWP'] = url_parte1 + df['TELEFONO'].astype(str) + url_parte2
        
        # Generar borrador temporal en Excel
        df.to_excel(archivo_temporal, index=False)

        print(f"\n{CYAN}📊 VISTA PREVIA LISTA{RESET}")
        print(f"El archivo temporal {VERDE}{archivo_temporal}{RESET} ha sido creado.")
        print("👉 Abriendo en VS Code para validación...")

        # 3. VISUALIZACIÓN EN VS CODE
        abrir_en_vscode(archivo_temporal)

        # 4. DECISIONES Y GUARDADO POR TERMINAL
        guardar = input(f"\n{AMARILLO}¿Conservar estos datos con un nombre definitivo? (si/no): {RESET}").strip().lower()

        if guardar in ['si', 's', 'yes', 'y']:
            nombre_archivo = input(f"{CYAN}Indicar el nombre final del archivo: {RESET}").strip()
            
            if not nombre_archivo.endswith('.xlsx'):
                nombre_archivo += '.xlsx'
                
            shutil.copy2(archivo_temporal, nombre_archivo)
            print(f"\n{VERDE}✅ Archivo guardado exitosamente como: {nombre_archivo}{RESET}")
        else:
            print(f"\n{AMARILLO}Operación cancelada. El borrador será descartado.{RESET}")

    except Exception as e:
        print(f"\n{ROJO}❌ Error crítico al procesar el archivo: {e}{RESET}")

    finally:
        # 5. LIMPIEZA
        if os.path.exists(archivo_temporal):
            try:
                os.remove(archivo_temporal)
                print(f"{VERDE}🧹 Archivo temporal eliminado correctamente del sistema.{RESET}")
            except PermissionError:
                print(f"{AMARILLO}⚠️ Nota: No se pudo borrar el temporal automáticamente. Cerrar la pestaña en VS Code antes de ejecutar nuevamente.{RESET}")

        print(f"\n{CYAN}Proceso finalizado.{RESET}")

if __name__ == "__main__":
    main()