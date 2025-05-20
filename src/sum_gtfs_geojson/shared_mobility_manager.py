from sum_gtfs_geojson.enums import LivingLabsCity, DataType
from sum_gtfs_geojson.loader import GenevaLoader, AbstractLoader
from sum_gtfs_geojson.models import UrbanMobilitySystem

DEFAULT_OUTPUT_JSON_FILES_PATH = "data/living_labs/"


class SharedMobilityManager:
    def __init__(self, city: LivingLabsCity = LivingLabsCity.GENEVA, data_types: list[DataType] = None):
        """
        Initialize the SharedMobilityManager with a specific city.        

        Args:
            city (LivingLabsCity, optional): The city for which to manage shared mobility data.. Defaults to LivingLabsCity.GENEVA.
            data_types (list[DataType], optional): List of data types to load. If None, all data types will be loaded. Defaults to None.
        """
        self.city = city
        self.loader = self.get_loader(city)
        self.data = self.loader.load_all_data(data_types)

    def get_loader(self, city: LivingLabsCity) -> AbstractLoader:
        """
        Get the appropriate loader for the specified city.
        :param city: The city for which to get the loader.
        :return: An instance of the loader for the specified city.
        """
        if city == LivingLabsCity.GENEVA:
            return GenevaLoader()
        else:
            raise ValueError(f"Unsupported city: {city}")
        # Add more loaders for other cities as needed

    def load_data(self, datatypes: list[DataType] = None) -> UrbanMobilitySystem:
        """
        Load data for the specified city and data types.
        :param datatypes: List of data types to load. If None, load all data types.
        :return: An UrbanMobilitySystem object containing the loaded data.
        """
        self.data = self.loader.load_all_data(datatypes)
        return self.data

    def get_default_geojson_path(self) -> str:
        """
        Get the default path for saving GeoJSON files.
        :return: The default path for saving GeoJSON files.
        """
        return DEFAULT_OUTPUT_JSON_FILES_PATH + str(self.city.name).lower() + "/geojson"

    def save_to_geojson(self, output_path: str = None):
        """
        Save the loaded data to GeoJSON files.
        :param output_path: The path where the GeoJSON files will be saved.
        """
        if output_path is None:
            output_path = self.get_default_geojson_path()
        self.data.save_to_geojson(output_path)
        print(f"Data saved to {output_path} as GeoJSON files.")
