from abc import ABC, abstractmethod
from sum_gtfs_geojson.enums import DataType
from sum_gtfs_geojson.models import UrbanMobilitySystem, GTFSNetwork, HexGrid, Stop, StationInfoStatus
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from pathlib import Path
from typing import List, Optional, Literal
from sum_gtfs_geojson.utils import GeoToolkit


WORLD_COUNTRIES_FILE_PATH = "data/world/10m/ne_10m_admin_0_countries.shp"
CRS_GEOGRAPHIC = "EPSG:4326"
CRS_PROJECTED = "EPSG:3857"


class AbstractLoader(ABC):
    def __init__(self, country_a3: str, restrict_country_boundaries: bool = False,
                 distance_radius_km: float = None, grid_resolution: Optional[int] = None):
        """
        Initialize the AbstractLoader with a flag to include country border crossing data.
        Args:
            restrict_country_boundaries: Flag to restrict to country data. Defaults to False, then the complete data will be loaded, including neighbor countries (when applicable).
            distance_radius_km (float, optional): The distance radius in kilometers for filtering data. Defaults to None.
            grid_resolution (int, optional): Resolution of the grid. Defaults to None.
        """
        self.country_a3 = country_a3
        self.restrict_country_boundaries = restrict_country_boundaries
        self.distance_radius_km = distance_radius_km
        self.grid_resolution = grid_resolution

        if (restrict_country_boundaries):
            self.country_geo = self.get_country_boundaries()
        else:
            self.country_geo = None

    @property
    @abstractmethod
    def COUNTRY_A3_CODE(self) -> str:
        pass

    @property
    @abstractmethod
    def COUNTRY_NAME(self) -> str:
        pass

    @property
    @abstractmethod
    def COUNTRY_ISO_CODE(self) -> str:
        pass

    @property
    @abstractmethod
    def _CITY_CENTER(self) -> tuple:
        pass

    @property
    @abstractmethod
    def CITY_NAME(self) -> str:
        pass

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

    def is_location_within_country(self, latitude: float, longitude: float) -> bool:
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
            crs=CRS_GEOGRAPHIC
        )

        # Ensure Coordinate Reference Systems Match
        if point.crs != self.country_geo.crs:
            point = point.to_crs(self.country_geo.crs)

        is_within = point.within(self.country_geo.unary_union).iloc[0]
        return is_within

    def is_location_within_radius(self, latitude: float, longitude: float) -> bool:
        """
        Check if the given latitude and longitude are within the specified distance radius.

        Args:
            latitude (float): position latitude (float)
            longitude (float): position longitude (float)

        Returns:
            bool: True if the point is within the distance radius, False otherwise.
        """
        if self.distance_radius_km is None:
            return True

        # Create GeoSeries for city center and the test point
        center_lat, center_lon = self._CITY_CENTER
        city_center = gpd.GeoSeries(
            [Point(center_lon, center_lat)], crs=CRS_GEOGRAPHIC)
        point = gpd.GeoSeries([Point(longitude, latitude)], crs=CRS_GEOGRAPHIC)

        # Reproject to a metric CRS (meters)
        city_center = city_center.to_crs(CRS_PROJECTED)
        point = point.to_crs(CRS_PROJECTED)

        # Create a circular buffer (in meters)
        radius_meters = self.distance_radius_km * 1000
        city_buffer = city_center.buffer(radius_meters)

        return point.within(city_buffer.iloc[0]).iloc[0]

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
        if (self.restrict_country_boundaries and self.is_location_within_country(latitude, longitude) == False):
            return False
        if (self.distance_radius_km is not None and self.is_location_within_radius(latitude, longitude) == False):
            return False

        return True

    def load_all_data(self, datatypes: list[DataType] = None) -> UrbanMobilitySystem:
        """
            Load all data for the specified data types.
            :param datatypes: List of data types to load. If None, load all data types.
            :return: An UrbanMobilitySystem object containing the loaded data.
        """

        ums = UrbanMobilitySystem(
            public_transport=GTFSNetwork(),
            bike_stations=[],
            ridership=[],
            bike_trips=[],
            hex_grid=None
        )
        if datatypes is None:
            print("No data types specified, nothing to load.")
            return ums
            
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
        if DataType.HEX_GRID in datatypes:
            ums.hex_grid = self.load_hex_grid(ums.public_transport.stops, ums.bike_stations)
            print(
                f"Finished loading hex grid, loaded counter = {len(ums.hex_grid.cells)}")

        return ums
    
    def load_hex_grid(self, stops: List[Stop] = None, bike_stations: List[StationInfoStatus] = None) -> HexGrid:
        """
        Load the hex grid for the specified city.
        :return: A HexGrid object containing the hexagonal grid.
        """
        print("Loading hex grid... with resolution: ", self.grid_resolution)
        if self.grid_resolution is None:
            raise ValueError("Grid resolution must be set to load a hex grid.")
        
        stop_points = [
            Point(s.stop_lon, s.stop_lat) for s in stops if s.stop_lat is not None and s.stop_lat is not None]
        bike_station_points = [
            Point(s.lon, s.lat) for s in bike_stations if s.lon is not None and s.lat is not None]
        all_points = stop_points + bike_station_points
        if not all_points:
            raise ValueError("No valid points found for hex grid generation.")
        
        print(f"Generating hex grid with {len(all_points)} points.")
        grid = GeoToolkit.generate_hex_grid(all_points, self.grid_resolution)
        print(f"Hex grid generated with {len(grid.cells)} cells.")
        
        return grid
