# DataScienceTree

Una herramienta de línea de comandos para inicializar proyectos de Análisis Exploratorio de Datos (EDA) con una estructura de carpetas estandarizada.

## 🚀 Características

- Creación automática de estructura de carpetas para proyectos de Data Science
- Generación de README.md personalizado
- Inicialización automática de entorno virtual con Poetry
- Opción para incluir directorio de modelos
- Creación automática de archivos .gitkeep para mantener la estructura en Git

## 📋 Requisitos Previos

- Python 3.11 o superior
- Poetry para gestión de dependencias
- Git (opcional, pero recomendado)

## 🔧 Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>

# Instalar usando Poetry
poetry install
```

## 🎯 Uso

La herramienta se puede usar a través de línea de comandos con el siguiente comando:

```bash
DSTree init [OPTIONS]
```

### Opciones disponibles:

- `--models`: Flag opcional para incluir la carpeta 'models'
- `--name`: Nombre del proyecto (se solicitará si no se proporciona)
- `--author`: Autor del proyecto (se solicitará si no se proporciona)

### Ejemplo de uso:

```bash
DSTree init --models --name "Mi Proyecto EDA" --author "Juan Maniglia"
```

## 📁 Estructura de Carpetas Generada

```
├── README.md          <- Documentación principal del proyecto
├── data/
│   ├── raw/          <- Datos originales, inmutables
│   └── processed/    <- Datos procesados para modelado
├── notebooks/        <- Jupyter notebooks
├── scripts/         <- Scripts de procesamiento y análisis
├── reports/         <- Reportes generados y visualizaciones
└── models/          <- Modelos entrenados (opcional)
```

## 🛠️ Tecnologías Utilizadas

- [Click](https://click.palletsprojects.com/) - Framework para crear aplicaciones de línea de comandos
- [Poetry](https://python-poetry.org/) - Gestión de dependencias y empaquetado
- Python 3.11

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor, siéntete libre de:

1. Hacer fork del proyecto
2. Crear tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## 📬 Contacto

Juan Maniglia - [@JuanManiglia](https://github.com/JuanManiglia)

Link del proyecto: [https://github.com/JuanManiglia/dataScienceTree](https://github.com/JuanManiglia/dataScienceTree)