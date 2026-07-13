import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo de Ferretería EPA",
        filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx")]
    )
    return archivo

def procesar_visor_epa():
    print("=== VISOR DE DATOS EPA (LIMPIEZA ACTIVA) ===\n")
    
    ruta = seleccionar_archivo()
    if not ruta:
        print("❌ No se seleccionó ningún archivo.")
        return

    try:
        # Carga según extensión
        if ruta.endswith('.csv'):
            df = pd.read_csv(ruta)
        else:
            df = pd.read_excel(ruta)

        # 1. Diccionario de Renombramiento específico para EPA
        mapeo_epa = {
            'product-item-link': 'Producto',
            'price': 'Precio_Base',
            'price 3': 'Decimales',
            'product href': 'Enlace_Web',
            'product-image-photo src': 'Imagen_Link'
        }

        # 2. Renombrar
        df = df.rename(columns=mapeo_epa)

        # 3. Filtrar columnas útiles
        # Excluimos 'product' y 'product 2' porque contienen código CSS/JS basura
        columnas_utiles = [col for col in mapeo_epa.values() if col in df.columns]
        
        if not columnas_utiles:
            print("❌ El archivo no tiene el formato esperado de EPA.")
            print(f"Columnas detectadas: {list(df.columns)}")
            return

        df_visor = df[columnas_utiles].copy()

        # 4. Limpieza rápida de precios (opcional, para asegurar que sean números)
        if 'Precio_Base' in df_visor.columns:
            df_visor['Precio_Base'] = df_visor['Precio_Base'].astype(str).str.replace(',', '.')

        # 5. Guardar para Excel Viewer
        nombre_salida = "VISOR_EPA_LIMPIO.xlsx"
        df_visor.to_excel(nombre_salida, index=False)

        print(f"✅ Análisis completado.")
        print(f"📂 Archivo generado: '{nombre_salida}'")
        print("-" * 50)
        print("💡 INSTRUCCIÓN: Abre 'VISOR_EPA_LIMPIO.xlsx' en el panel de")
        print("   archivos a tu izquierda para verlo con Excel Viewer.")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    procesar_visor_epa()