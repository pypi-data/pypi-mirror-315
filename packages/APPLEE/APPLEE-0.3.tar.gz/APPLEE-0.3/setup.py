from setuptools import setup, find_packages

setup(
    name='APPLEE',  # Nombre de tu paquete
    version='0.3',  # Versión inicial
    packages=['APPLEE'],  # Esto busca automáticamente los paquetes
    install_requires=[],  # Lista de dependencias (por ejemplo, 'numpy', 'pandas')
    description='Descripción breve de tu paquete',
    long_description=open('README.md').read(),
    author=' ',
    author_email=' ',
    url='https://github.com/GRUNECO/portables.git',  # URL del repositorio
)
