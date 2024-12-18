from setuptools import setup, find_packages

setup(
    name='u3m',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'numpy',
        'opencv-python',
        'scikit-image',
        'scipy',
        'laspy',
        'pyproj',
        'lazrs[laszip]',
        'leafmap',
        'xarray',
        'rasterio',
        'localtileserver'
    ],
    python_requires='>=3.10',  # Specify your Python version requirement here
)