from setuptools import setup, find_packages

setup(
    name='openrs-python',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'Pillow',
        'opencv-python',
        'pyproj',
        'scipy',
        'shapely',
        'fiona',
        'geopandas',
        'scikit-image'
    ],
    python_requires='>=3.10',  # Specify your Python version requirement here
)

