import pandas as pd
import os

def ris_to_xlsx(ris_file, output_file="referencias.xlsx"):
    referencias = []
    ref_actual = {}

    with open(ris_file, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue  # saltar líneas vacías

            if linea.startswith("ER"):  # Fin de una referencia
                if ref_actual:
                    referencias.append(ref_actual)
                    ref_actual = {}
            else:
                try:
                    clave, valor = linea.split("  - ", 1)
                    clave = clave.strip()
                    valor = valor.strip()

                    # Si la clave ya existe, convertir en lista
                    if clave in ref_actual:
                        if isinstance(ref_actual[clave], list):
                            ref_actual[clave].append(valor)
                        else:
                            ref_actual[clave] = [ref_actual[clave], valor]
                    else:
                        ref_actual[clave] = valor
                except ValueError:
                    pass  # ignorar líneas mal formadas

    # Convertir a DataFrame
    df = pd.DataFrame(referencias)

    # Guardar en Excel
    df.to_excel(output_file, index=False, engine="openpyxl")

    print(f"✅ Archivo convertido: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    archivo_ris = "C:/Users/User/Desktop/archivo.ris"
    ris_to_xlsx(archivo_ris, "C:/Users/User/Desktop/referencias.xlsx")