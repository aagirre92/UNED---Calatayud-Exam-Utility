# Utilidad de Exámenes de Calatayud

Este proyecto consiste en una serie de scripts diseñados para manejar el repositorio de exámenes de la página de Calatayud, que es el principal repositorio de exámenes de la UNED. Los scripts permiten a los usuarios descargar, renombrar y fusionar archivos PDF de exámenes con información adicional.

## Pasos para Usar los Scripts

### Paso 1: Extraer URLs de los Exámenes
Primero, navega a la página de Calatayud y ejecuta el script `get_href_downloads.js` en la consola del navegador. Este script extraerá todas las URLs de los exámenes disponibles y las guardará en un archivo JSON.

### Paso 2: Crear `list_downloads.json`
Crea un archivo llamado `list_downloads.json` y pega las URLs extraídas en formato JSON. El archivo debe verse así:
```json
{
  "urls": [
    "http://www.calatayud.uned.es/examenes/docs/7190/1/71901089/E719010890A11J1.pdf",
    "http://www.calatayud.uned.es/examenes/docs/7190/1/71901089/E719010890C11J1.pdf",
    ...
  ]
}
```

### Paso 3: Descargar los PDFs de los Exámenes
Ejecuta el script `download_files.py`. Este script lee el archivo `list_downloads.json` y descarga los PDFs de los exámenes en una carpeta llamada `downloaded_pdfs`.

### Paso 4: Renombrar los PDFs de los Exámenes
Ejecuta el script `rename_downloaded_pdfs.py`. Este script renombra los PDFs descargados según una convención de nombres más legible basada en la información del examen.

### Paso 5: Añadir Encabezados y Fusionar PDFs
Ejecuta el script `main_merge_pdfs.py`. Este script añade encabezados a cada PDF con información como el mes, año y convocatoria, y luego fusiona todos los exámenes en un único archivo PDF llamado `merged_output.pdf`.

## Detalles de los Scripts

### `get_href_downloads.js`
Extrae URLs de PDFs de la página de Calatayud y las guarda en un archivo JSON.

### `list_downloads.json`
Contiene la lista de URLs de los exámenes en formato JSON.

### `download_files.py`
Descarga los PDFs de los exámenes desde las URLs listadas en `list_downloads.json`.

### `rename_downloaded_pdfs.py`
Renombra los PDFs descargados a un formato más legible.

### `main_merge_pdfs.py`
Añade encabezados a los PDFs con información del examen y los fusiona en un único archivo PDF.

## Ejemplo de Uso

1. Ejecuta `get_href_downloads.js` en la consola del navegador en la página de Calatayud (una vez estés dentro de la página donde están las URL con los examemes, es decir, los 'iconitos').
2. Crea `list_downloads.json` con las URLs extraídas.
3. Ejecuta `download_files.py` para descargar los PDFs.
4. Ejecuta `rename_downloaded_pdfs.py` para renombrar los PDFs.
5. Ejecuta `main_merge_pdfs.py` para añadir encabezados y fusionar los PDFs.

Este proyecto simplifica el proceso de manejo de PDFs de exámenes de la página de Calatayud, facilitando la descarga, renombrado y fusión de los mismos con información adicional.