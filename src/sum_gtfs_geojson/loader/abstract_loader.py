from abc import ABC, abstractmethod
from sum_gtfs_geojson.enums import DataType
from sum_gtfs_geojson.models import UrbanMobilitySystem, GTFSNetwork

DEFAULT_DATA_TYPES = [
    DataType.STOPS,
    DataType.ITINERARIES,
    DataType.BIKE_STATIONS,
    DataType.RIDERSHIP,
    DataType.BIKE_TRIPS,
]

class AbstractLoader(ABC):
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
            print(f"Finished loading stations, loaded counter = {len(ums.public_transport.stops)}")
        if DataType.ITINERARIES in datatypes:
            ums.public_transport.routes = self.load_routes()            
            print(f"Finished loading routes, loaded counter = {len(ums.public_transport.routes)}")
            ums.public_transport.trips = self.load_trips()
            print(f"Finished loading trips, loaded counter = {len(ums.public_transport.trips)}")
            ums.public_transport.stop_times = self.load_stop_times()
            print(f"Finished loading stop_times, loaded counter = {len(ums.public_transport.stop_times)}")
        if DataType.BIKE_STATIONS in datatypes:
            ums.bike_stations = self.load_bike_stations()
            print(f"Finished loading bike_stations, loaded counter = {len(ums.bike_stations)}")
        if DataType.RIDERSHIP in datatypes:
            ums.ridership = self.load_ridership()
            print(f"Finished loading ridership, loaded counter = {len(ums.ridership)}")
        if DataType.BIKE_TRIPS in datatypes:
            ums.bike_trips = self.load_bike_trips()
            print(f"Finished loading bike_trips, loaded counter = {len(ums.bike_trips)}")
        return ums
