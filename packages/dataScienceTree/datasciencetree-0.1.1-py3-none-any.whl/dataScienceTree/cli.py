import os
import click
import subprocess

@click.group()
def main():
    """Herramienta para inicializar EDA"""
    pass

@main.command()
@click.option('--models', is_flag=True, help="Incluir la carpeta 'models'.")
@click.option('--name', prompt='Nombre del proyecto', help="El nombre del proyecto.")
@click.option('--author', prompt='Autor del proyecto', help="El autor o desarrollador principal.")
def init(models, name, author):
    """Inicializa la estructura de carpetas para EDA y entorno virtual con Poetry"""
    
    # Diccionario de carpetas con descripciones
    folders = {
        'data/raw': 'The original, immutable data dump.',
        'data/processed': 'The final, canonical data sets for modeling.',
        'notebooks': 'Jupyter notebooks for exploration and analysis.',
        'scripts': 'Scripts for data processing and analysis.',
        'reports': 'Generated analysis reports, visualizations, and results.'
    }

    # Anhadir la carpeta 'models' solo si el flag --models esta presente
    if models:
        folders['models'] = 'Trained models and related files.'

    # Crear las carpetas y el archivo .gitkeep en cada una
    for folder, description in folders.items():
        os.makedirs(folder, exist_ok=True)
        gitkeep_path = os.path.join(folder, '.gitkeep')
        with open(gitkeep_path, 'w') as f:
            pass
        print(f'Carpeta {folder} creada con .gitkeep')

    # Crear README.md con la estructura mejorada
    readme_content = f"""# {name}

Autor: {author}

## Descripcion

Este proyecto esta organizado en una estructura de carpetas para facilitar el análisis exploratorio de datos (EDA) y el desarrollo de modelos.

## Estructura de Carpetas

├── README.md <- El README de nivel superior para los desarrolladores que utilicen este proyecto. 
├── data 
│ ├── processed <- Los conjuntos de datos definitivos para la modelización. 
│ └── raw <- Los datos originales e inmutados. 
├── notebooks <- Jupyter notebooks para exploración y análisis. 
├── scripts <- Python scripts para el tratamiento y análisis de datos. 
├── reports <- Generación de informes de análisis, visualizaciones y resultados.
"""
    
    # Incluir la carpeta 'models' en el README solo si se ha creado
    if models:
        readme_content += "├── models <- Modelos entrenados y archivos relacionados.\n"

    readme_content += "```\n"

    # Guardar el README.md
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(readme_content)

    print("Archivo README.md creado con descripciones de cada carpeta.")

    # Crear un entorno virtual usando Poetry
    subprocess.run(['poetry', 'install'])
    print("Entorno virtual de Poetry creado")

    print("Estructura de carpetas, archivos .gitkeep, README.md y entorno virtual inicializados")
