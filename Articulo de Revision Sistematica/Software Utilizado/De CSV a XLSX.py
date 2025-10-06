import pandas as pd
import os

def csv_to_xlsx(csv_file, output_file="convertido.xlsx"):
    # Intentamos leer con latin1 en lugar de utf-8
    df = pd.read_csv(csv_file, encoding="latin1", sep=None, engine="python")
    
    # Guardar como Excel
    df.to_excel(output_file, index=False, engine="openpyxl")
    
    print(f"✅ Archivo convertido: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    # Ruta del archivo CSV en el escritorio
    csv_file = "C:/Users/User/Desktop/archivo.csv"   # 👈 pon aquí el nombre real
    salida = "C:/Users/User/Desktop/convertido.xlsx"
    csv_to_xlsx(csv_file, salida)