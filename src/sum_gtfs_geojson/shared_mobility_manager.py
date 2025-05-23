from sum_gtfs_geojson.enums import LivingLabsCity, DataType
from sum_gtfs_geojson.loader import GenevaLoader, AbstractLoader
from sum_gtfs_geojson.models import UrbanMobilitySystem
from typing import Optional

DEFAULT_OUTPUT_JSON_FILES_PATH = "data/geojson/"
DEFAULT_DATA_TYPES = [
    DataType.STOPS,
    DataType.ITINERARIES,
    DataType.BIKE_STATIONS,
    DataType.RIDERSHIP,
    DataType.BIKE_TRIPS,
    DataType.HEX_GRID
]

class SharedMobilityManager:
    def __init__(self,
                 city: LivingLabsCity = LivingLabsCity.GENEVA,
                 data_types: Optional[list[DataType]] = DEFAULT_DATA_TYPES,
                 geojson_output_path: Optional[str] = None,
                 restrict_country_boundaries: Optional[bool] = False,
                 distance_radius_km: Optional[float] = None,
                 grid_resolution: Optional[int] = 8
                 ):
        """
        Initialize the SharedMobilityManager with a specific city.        

        Args:
            city (LivingLabsCity, optional): The city for which to manage shared mobility data.. Defaults to LivingLabsCity.GENEVA.
            data_types (list[DataType], optional): List of data types to load. If None, all data types will be loaded. Defaults to None.
            geojson_output_path (str, optional): The path where the GeoJSON files will be saved. If None, a default path will be used data/geojson/{city_name}. Defaults to None.
            include_country_border_crossing (bool, optional): Flag to restrict to country data. Defaults to False, then the complete data will be loaded, including neighbor countries (when applicable).
            distance_radius_km (float, optional): The distance radius in kilometers for filtering data. Defaults to None.
            grid_resolution (int, optional): Resolution of the grid, from 0 to 15. Defaults to 8 (~1 km width, edge length ~1.22 km).
        """
        self.city = city
        self.data_types = data_types
        self.restrict_country_boundaries = restrict_country_boundaries
        self.distance_radius_km = distance_radius_km
        self.grid_resolution = grid_resolution
        self.loader = self.get_loader()
        self.geojson_output_path = geojson_output_path if geojson_output_path is not None else self._get_default_geojson_path()
        self.data = self.loader.load_all_data(data_types)

    def get_loader(self) -> AbstractLoader:
        """
        Get the appropriate loader for the specified city.
        :return: An instance of the loader for the specified city.
        """
        if self.city == LivingLabsCity.GENEVA:
            return GenevaLoader(restrict_country_boundaries=self.restrict_country_boundaries,
                                distance_radius_km=self.distance_radius_km,
                                grid_resolution=self.grid_resolution
                                )
        else:
            raise ValueError(
                f"Unsupported Living Lab: {self.city}, no values found for this city.")
        # Add more loaders for other cities as needed

    def load_data(self, datatypes: list[DataType] = None) -> UrbanMobilitySystem:
        """
        Load data for the specified city and data types.
        :param datatypes: List of data types to load. If None, load all data types.
        :return: An UrbanMobilitySystem object containing the loaded data.
        """
        self.data = self.loader.load_all_data(datatypes)
        return self.data

    def _get_default_geojson_path(self) -> str:
        """
        Get the default path for saving GeoJSON files.
        :return: The default path for saving GeoJSON files. Value is "data/geojson/{city_name}".
        """
        city_name = str(self.city.name).lower()
        file_path = [DEFAULT_OUTPUT_JSON_FILES_PATH, city_name]

        if self.restrict_country_boundaries:
            file_path.append("_within-country")

        if self.distance_radius_km:
            file_path.append(f"_{self.distance_radius_km}km-radius")
        
        if self.grid_resolution is not None and DataType.HEX_GRID in self.data_types:
            file_path.append(f"_{self.grid_resolution}res-hexgrid")

        return "".join(file_path)

    def save_to_geojson(self, output_path: str = None):
        """
        Save the loaded data to GeoJSON files.
        :param output_path: The path where the GeoJSON files will be saved.
        """
        if output_path is None:
            output_path = self.geojson_output_path
        self.data.save_to_geojson(output_path)
        print(f"Data saved to {output_path} as GeoJSON files.")
