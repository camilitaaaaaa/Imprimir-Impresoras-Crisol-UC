"""
Divide un archivo PDF en múltiples archivos de N páginas cada uno
(por defecto 30). El último archivo puede tener menos páginas si el
total no es divisible exactamente.

Uso:
    python dividir_pdf.py archivo.pdf
    python dividir_pdf.py archivo.pdf --paginas 30 --salida ./salida
"""

import argparse
import math
import os

from pypdf import PdfReader, PdfWriter


def dividir_pdf(ruta_pdf: str, paginas_por_archivo: int = 30, carpeta_salida: str = None):
    if not os.path.isfile(ruta_pdf):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_pdf}")

    # Nombre base del archivo (sin extensión) y carpeta de salida
    nombre_base = os.path.splitext(os.path.basename(ruta_pdf))[0]

    if carpeta_salida is None:
        carpeta_salida = os.path.dirname(os.path.abspath(ruta_pdf))
    os.makedirs(carpeta_salida, exist_ok=True)

    reader = PdfReader(ruta_pdf)
    total_paginas = len(reader.pages)

    if total_paginas == 0:
        print("El PDF no tiene páginas.")
        return []

    total_partes = math.ceil(total_paginas / paginas_por_archivo)
    # Para que los números queden bien ordenados alfabéticamente (01, 02, ..., 10)
    ancho_numero = len(str(total_partes))

    archivos_generados = []

    for parte in range(total_partes):
        inicio = parte * paginas_por_archivo
        fin = min(inicio + paginas_por_archivo, total_paginas)

        writer = PdfWriter()
        for i in range(inicio, fin):
            writer.add_page(reader.pages[i])

        numero_parte = str(parte + 1).zfill(ancho_numero)
        nombre_salida = f"{nombre_base}_{numero_parte}.pdf"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)

        with open(ruta_salida, "wb") as f:
            writer.write(f)

        archivos_generados.append(ruta_salida)
        print(f"Creado: {ruta_salida}  (páginas {inicio + 1}-{fin})")

    print(f"\nListo. {total_paginas} páginas divididas en {total_partes} archivo(s).")
    return archivos_generados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Divide un PDF en archivos de N páginas.")
    parser.add_argument("pdf", help="Ruta al archivo PDF a dividir")
    parser.add_argument(
        "--paginas", type=int, default=30, help="Cantidad de páginas por archivo (default: 30)"
    )
    parser.add_argument(
        "--salida", type=str, default=None, help="Carpeta donde guardar los archivos generados"
    )

    args = parser.parse_args()
    dividir_pdf(args.pdf, paginas_por_archivo=args.paginas, carpeta_salida=args.salida)
