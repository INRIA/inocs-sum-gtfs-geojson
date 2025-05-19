from setuptools import setup, find_packages
from Cython.Build import cythonize
import glob

DIST_DIR = "dist"

ext_modules = cythonize(
    glob.glob("src/sum_gtfs_geojson/*.py", recursive=True),
    compiler_directives={"language_level": "3"},
)

setup(
    name="sum_gtfs_geojson",
    version="0.1.0",
    author="Rebeca MURILLO",
    description="Public transport GTFS and Shared Urban Mobility data manager. GTFS parser and a GeoJSON exporter.", 
    packages=find_packages(),
    ext_modules=ext_modules,
    install_requires=[
        "pydantic",
        "geopandas",
        "pandas",
        "build",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['data/*']}
)

print(f"✅ Full build completed! Distribution ready at ./{DIST_DIR}/ 🚀")
