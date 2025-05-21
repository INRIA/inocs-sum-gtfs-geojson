from abc import ABC, abstractmethod
from sum_gtfs_geojson.enums import DataType
from sum_gtfs_geojson.models import UrbanMobilitySystem, GTFSNetwork
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from pathlib import Path


DEFAULT_DATA_TYPES = [
    DataType.STOPS,
    DataType.ITINERARIES,
    DataType.BIKE_STATIONS,
    DataType.RIDERSHIP,
    DataType.BIKE_TRIPS,
]
WORLD_COUNTRIES_FILE_PATH = "data/world/10m/ne_10m_admin_0_countries.shp"


class AbstractLoader(ABC):
    def __init__(self, country_a3: str, restrict_country_boundaries: bool = False):
        """
        Initialize the AbstractLoader with a flag to include country border crossing data.
        :param restrict_country_boundaries: Flag to restrict to country data. Defaults to False, then the complete data will be loaded, including neighbor countries (when applicable).
        """
        self.country_a3 = country_a3
        self.restrict_country_boundaries = restrict_country_boundaries
        if (restrict_country_boundaries):
            self.country_geo = self.get_country_boundaries()
        else:
            self.country_geo = None

    @abstractmethod
    def load_stops(self):
        pass

    @abstractmethod
    def load_routes(self):
        pass

    @abstractmethod
    def load_trips(self):
        pass

    @abstractmethod
    def load_stop_times(self):
        pass

    @abstractmethod
    def load_bike_stations(self):
        pass

    @abstractmethod
    def load_ridership(self):
        pass

    @abstractmethod
    def load_bike_trips(self):
        pass

    def get_country_boundaries(self) -> gpd.GeoDataFrame:
        """
        Load the country boundaries for the specified country.

        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing the boundaries of the specified country.
        """
        # Load world country boundaries
        world = gpd.read_file(WORLD_COUNTRIES_FILE_PATH)
        country_row = world.loc[world['SOV_A3'] == self.country_a3]

        if (country_row is None):
            raise ValueError(
                f"Country with code {self.country_a3} not found in the shapefile.")
        return country_row

    def is_position_in_country(self, latitude: float, longitude: float) -> bool:
        """
        Check if the given latitude and longitude are within the country boundaries.

        Args:
            latitude (float): position latitude (float)
            longitude (float): position longitude (float)

        Returns:
            bool: True if the point is within the country boundaries, False otherwise.
        """
        # Filter the data
        point = gpd.GeoDataFrame(
            geometry=[Point(longitude, latitude)],
            crs="EPSG:4326"
        )
        
        # Ensure Coordinate Reference Systems Match
        if point.crs != self.country_geo.crs:
            point = point.to_crs(self.country_geo.crs)
            
        is_within = point.within(self.country_geo.unary_union).iloc[0]
        return is_within

    def position_is_valid(self, latitude: float = None, longitude: float = None) -> bool:
        """Check if the given latitude and longitude are valid.

        Args:
            latitude (float, optional): latitude position. Defaults to None.
            longitude (float, optional): longitude position. Defaults to None.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        if latitude is None or longitude is None:
            return False
        if (self.restrict_country_boundaries and self.is_position_in_country(latitude, longitude) == False):
            return False
        return True

    def load_all_data(self, datatypes: list[DataType] = None) -> UrbanMobilitySystem:
        """
            Load all data for the specified data types.
            :param datatypes: List of data types to load. If None, load all data types.
            :return: An UrbanMobilitySystem object containing the loaded data.
        """
        if datatypes is None:
            datatypes = DEFAULT_DATA_TYPES

        ums = UrbanMobilitySystem(
            public_transport=GTFSNetwork(),
            bike_stations=[],
            ridership=[],
            bike_trips=[]
        )
        if DataType.STOPS in datatypes:
            ums.public_transport.stops = self.load_stops()
            print(
                f"Finished loading stations, loaded counter = {len(ums.public_transport.stops)}")
        if DataType.ITINERARIES in datatypes:
            ums.public_transport.routes = self.load_routes()
            print(
                f"Finished loading routes, loaded counter = {len(ums.public_transport.routes)}")
            ums.public_transport.trips = self.load_trips()
            print(
                f"Finished loading trips, loaded counter = {len(ums.public_transport.trips)}")
            ums.public_transport.stop_times = self.load_stop_times()
            print(
                f"Finished loading stop_times, loaded counter = {len(ums.public_transport.stop_times)}")
        if DataType.BIKE_STATIONS in datatypes:
            ums.bike_stations = self.load_bike_stations()
            print(
                f"Finished loading bike_stations, loaded counter = {len(ums.bike_stations)}")
        if DataType.RIDERSHIP in datatypes:
            ums.ridership = self.load_ridership()
            print(
                f"Finished loading ridership, loaded counter = {len(ums.ridership)}")
        if DataType.BIKE_TRIPS in datatypes:
            ums.bike_trips = self.load_bike_trips()
            print(
                f"Finished loading bike_trips, loaded counter = {len(ums.bike_trips)}")
        return ums
