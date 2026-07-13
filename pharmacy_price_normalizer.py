import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import re

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    archivo = filedialog.askopenfilename(
        title="Sube tu archivo de Farmatodo",
        filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx")]
    )
    return archivo

def limpiar_monto(valor):
    """Convierte formatos como Bs.756.50 o 7.608,39 en números limpios"""
    if pd.isna(valor) or str(valor).strip() == "" or valor == 0:
        return 0.0
    
    s = str(valor).upper().replace("BS.", "").strip()
    s = re.sub(r'[^\d,.]', '', s) # Quita letras y símbolos
    
    if not s: return 0.0

    # Lógica de detección de miles y decimales
    if ',' in s and '.' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        if s.count(',') > 1: s = s.replace(',', '')
        else: s = s.replace(',', '.')
    elif '.' in s:
        if s.count('.') > 1:
            partes = s.split('.')
            s = f"{''.join(partes[:-1])}.{partes[-1]}"
            
    try:
        return round(float(s), 2)
    except:
        return 0.0

def extraer_precio_unidad(texto):
    """Limpia 'Tabletas a Bs 75.65' y deja solo 75.65"""
    if pd.isna(texto) or texto == "":
        return 0.0
    # Buscamos cualquier número (con puntos o comas) que esté al final o tras la palabra 'Bs'
    numeros_encontrados = re.findall(r"[\d,.]+", str(texto))
    if numeros_encontrados:
        # Tomamos el último número de la cadena, que suele ser el precio
        return limpiar_monto(numeros_encontrados[-1])
    return 0.0

def procesar_farmatodo():
    print("=== OPTIMIZADOR DE DATOS FARMATODO PRO ===\n")
    
    ruta = seleccionar_archivo()
    if not ruta: return

    try:
        # Carga inteligente del archivo
        if ruta.endswith('.csv'):
            df = pd.read_csv(ruta, encoding='utf-8', sep=None, engine='python')
        else:
            df = pd.read_excel(ruta)

        # 1. Definimos el mapeo de nombres técnicos a nombres solicitados
        mapeo = {
            'product-card__title': 'Producto',
            'product-card__brand': 'Marca',
            'product-card__price-value': 'Precio_Actual',
            'product-card__price-offer': 'Precio_Anterior',
            'product-card__pum': 'Precio_por_Unidad',
            'bv_text': 'Calificacion',
            'bv_text 2': 'Opiniones',
            'product-image__link href': 'Link'
        }

        # Renombrar
        df = df.rename(columns=mapeo)

        # 2. Seleccionamos y REORDENAMOS las columnas según tu pedido
        columnas_ordenadas = [
            'Producto', 'Marca', 'Precio_Actual', 'Precio_Anterior', 
            'Precio_por_Unidad', 'Calificacion', 'Opiniones', 'Link'
        ]
        
        # Solo tomamos las que existan para evitar errores
        columnas_finales = [c for c in columnas_ordenadas if c in df.columns]
        df_visor = df[columnas_finales].copy()

        # 3. LIMPIEZA DE DATOS
        if 'Precio_Actual' in df_visor.columns:
            df_visor['Precio_Actual'] = df_visor['Precio_Actual'].apply(limpiar_monto)
        
        if 'Precio_Anterior' in df_visor.columns:
            df_visor['Precio_Anterior'] = df_visor['Precio_Anterior'].apply(limpiar_monto)

        if 'Precio_por_Unidad' in df_visor.columns:
            # Aquí eliminamos "Tabletas", "gramos", etc.
            df_visor['Precio_por_Unidad'] = df_visor['Precio_por_Unidad'].apply(extraer_precio_unidad)

        # 4. GUARDADO
        nombre_salida = "REPORTE_FARMATODO_PRO.xlsx"
        df_visor.to_excel(nombre_salida, index=False)

        print(f"✅ ¡PROCESO COMPLETADO!")
        print(f"📊 Columna 'Precio por Unidad' ahora es solo numérica.")
        print(f"🗑️ Columna 'Tiempo de Entrega' ha sido eliminada.")
        print(f"📂 Archivo generado: '{nombre_salida}'")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    procesar_farmatodo()