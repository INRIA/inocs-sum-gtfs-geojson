from sum_gtfs_geojson.enums import LivingLabsCity, DataType
from sum_gtfs_geojson.loader import GenevaLoader, AbstractLoader
from sum_gtfs_geojson.models import UrbanMobilitySystem

DEFAULT_OUTPUT_JSON_FILES_PATH = "data/geojson/"


class SharedMobilityManager:
    def __init__(self,
                 city: LivingLabsCity = LivingLabsCity.GENEVA,
                 data_types: list[DataType] = None,
                 geojson_output_path: str = None,
                 restrict_country_boundaries: bool = False,
                 ):
        """
        Initialize the SharedMobilityManager with a specific city.        

        Args:
            city (LivingLabsCity, optional): The city for which to manage shared mobility data.. Defaults to LivingLabsCity.GENEVA.
            data_types (list[DataType], optional): List of data types to load. If None, all data types will be loaded. Defaults to None.
            geojson_output_path (str, optional): The path where the GeoJSON files will be saved. If None, a default path will be used data/geojson/{city_name}. Defaults to None.
            include_country_border_crossing (bool, optional): Flag to restrict to country data. Defaults to False, then the complete data will be loaded, including neighbor countries (when applicable).
        """
        self.city = city
        self.restrict_country_boundaries = restrict_country_boundaries
        self.loader = self.get_loader()
        self.geojson_output_path = geojson_output_path if geojson_output_path is not None else self._get_default_geojson_path()
        self.data = self.loader.load_all_data(data_types)

    def get_loader(self) -> AbstractLoader:
        """
        Get the appropriate loader for the specified city.
        :return: An instance of the loader for the specified city.
        """
        if self.city == LivingLabsCity.GENEVA:
            return GenevaLoader(self.restrict_country_boundaries)
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
        return DEFAULT_OUTPUT_JSON_FILES_PATH + str(self.city.name).lower() + f"_{'local' if self.restrict_country_boundaries else 'default'}"

    def save_to_geojson(self, output_path: str = None):
        """
        Save the loaded data to GeoJSON files.
        :param output_path: The path where the GeoJSON files will be saved.
        """
        if output_path is None:
            output_path = self.geojson_output_path
        self.data.save_to_geojson(output_path)
        print(f"Data saved to {output_path} as GeoJSON files.")
