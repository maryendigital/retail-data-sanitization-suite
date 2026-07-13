import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    # Asegura que la ventana salga al frente
    root.attributes("-topmost", True)
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo de MercadoLibre",
        filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx")]
    )
    return archivo

def procesar_vista_previa():
    print("=== VISOR DE DATOS MERCADOLIBRE ===\n")
    
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

        # Diccionario de Renombramiento (Mapeo técnico a humano)
        mapeo_columnas = {
            'title': 'Producto',
            'price': 'Precio_Crudo',
            'item_page_link': 'Link_Producto',
            'delivery_free_shipping_message': 'Envio_Gratis',
            'seller_name_2': 'Vendedor',
            'seller_rating_sales': 'Ventas_Vendedor',
            'available_quantity': 'Stock_Num',
            'stock_available_message': 'Info_Stock',
            'ratingvalue': 'Calificacion',
            'brand': 'Marca',
            'product_model': 'Modelo'
        }

        # Renombramos solo las columnas que existan en el archivo
        df = df.rename(columns=mapeo_columnas)

        # Seleccionamos las columnas más relevantes para la vista previa
        columnas_finales = [col for col in mapeo_columnas.values() if col in df.columns]
        df_vista = df[columnas_finales]

        # Guardamos un archivo local para el Excel Viewer de VS Code
        nombre_salida = "VISTA_LEGIBLE.xlsx"
        df_vista.to_excel(nombre_salida, index=False)

        print(f"✅ Archivo procesado con éxito.")
        print(f"📂 Se ha creado '{nombre_salida}' en tu carpeta actual.")
        print("-" * 50)
        print("💡 INSTRUCCIÓN: Haz clic en 'VISTA_LEGIBLE.xlsx' en tu panel izquierdo")
        print("   de VS Code para verlo con tu Excel Viewer.")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")

if __name__ == "__main__":
    procesar_vista_previa()