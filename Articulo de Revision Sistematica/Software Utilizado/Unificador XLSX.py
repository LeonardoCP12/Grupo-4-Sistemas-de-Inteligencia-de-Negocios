import pandas as pd
import glob
import os

def main():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    archivos = glob.glob(os.path.join(carpeta, "*.xlsx"))

    if not archivos:
        print("No se encontraron archivos XLSX en la carpeta.")
        return

    print(f"Se encontraron {len(archivos)} archivos XLSX:")
    for f in archivos:
        print(" -", os.path.basename(f))

    # Unir todos los Excel (por defecto toma la primera hoja)
    df = pd.concat([pd.read_excel(f) for f in archivos], ignore_index=True)

    salida = os.path.join(carpeta, "unidos.xlsx")

    # 👇 Debug: mostrar dónde se guarda
    print("Carpeta actual:", os.getcwd())
    print("Archivo de salida:", os.path.abspath(salida))

    df.to_excel(salida, index=False, engine="openpyxl")

    print("✅ Listo: creado 'unidos.xlsx'")

if __name__ == "__main__":
    main()
