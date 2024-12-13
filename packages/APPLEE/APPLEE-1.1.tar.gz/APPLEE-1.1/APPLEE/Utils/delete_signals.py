import os

# Directorio raíz donde están las carpetas de los sujetos
root_dir = r'D:\portablesProyecto\BIDS_PORTABLES_CODIFICADO\derivatives\APPLEE'

# Palabras clave que identificarán los archivos a eliminar
keywords = ['reject', 'Muscle']

# Recorrer todas las subcarpetas y archivos
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        # Si el nombre del archivo contiene alguna de las palabras clave
        if any(keyword in file for keyword in keywords):
            file_path = os.path.join(subdir, file)
            print(f'Eliminando archivo: {file_path}')
            os.remove(file_path) 