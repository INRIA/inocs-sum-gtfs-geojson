# Introduction sum_gtfs_geojson 
The library `sum_gtfs_geojson` aims to facilitate the experimentation with Living Labs data within the context of SUM project. The data used within the repository is publicly available by public transport providers. 

## Features
The library proposes the following features : 
- load public transport network data for a Living Lab 
- create hexagonal grid for the network 
- restrict the perimerer to a given radius in KM
- restrict the perimeter within the country (ignore stops in neighbouring countries)
- convert data to GeoJson
- Demo to display data in map, with HTML/JS and Leaflet library for map display 
- Living Lab available : GENEVA


## Documentation

- Read the [API documentation sum_gtfs_geojson](https://inria.github.io/inocs-sum-gtfs-geojson/docs) for complete parameter configuration. 
- Check our dynamic map [demo with preprocessed data](https://inria.github.io/inocs-sum-gtfs-geojson)



## Install the package 
In Python environment, it is a good practice to isolate your project in an environment. The following documentation uses `pipenv` to handle packages installation the local environment. 

Download the built package available at the [dist folder](https://github.com/INRIA/inocs-sum-gtfs-geojson/tree/main/dist). 

Then install from local file. 

Install from local file : 
```sh
pipenv install $PATH_TO_FILE/sum_gtfs_geojson-0.1.0-cp39-cp39-macosx_10_9_universal2.whl
```


Or install from Github link. 

Install from local file : 
```sh
pipenv install https://inria.github.io/inocs-sum-gtfs-geojson/dist/sum_gtfs_geojson-0.1.0-cp39-cp39-macosx_10_9_universal2.whl
```

## Build and publish the package

### 1. Install dependencies and build package 
Create environment and install pipenv, then install dependencies. 
Finally, build the package. 

```bash
python3 -m venv env && source env/bin/activate && pip install pipenv && pipenv install --dev
# Build the wheel
python -m build

# Generate the docs
python build_docs.py

# OPTIONAL : clean and reset the build files 
rm -rf build dist *.egg-info

```
**The compiled wheel package .whl file will be at `./dist` folder.**

**The documentation will be at `./dist` folder.**


## Local installation for development

Ensure you have Python installed (recommended: Python 3.8+).

1. Clone the repository
2. Create an environment
3. Install the necessary packages
4. Create experiments and run the models
5. Analyze the results

### 1. Clone the repository

Clone the repository using the following command:

```bash
git clone https://github.com/INRIA/inocs-sum-gtfs-geojson.git
```

### 2. Create an environment

Check the [Python packaging user guide](https://packaging.python.org/en/latest/tutorials/managing-dependencies/) for more information on how to manage dependencies in Python.

On Debian protected environment, create a virtual enviornment first :

```bash
python3 -m venv env && source env/bin/activate && pip install pipenv
```

Install library pipenv to handle the environment and the dependencies.

```bash
pip install pipenv
```


## View the dynamic map with generated data

### Start server with python

```py
python -m http.server 8080 
```

Then go to page in browser : http://localhost:8080

