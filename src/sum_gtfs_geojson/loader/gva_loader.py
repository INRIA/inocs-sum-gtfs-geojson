import pandas as pd
from pydantic import ValidationError
from sum_gtfs_geojson.models import Stop, Route, StationInfoStatus, BikeTrip, Ridership, StopTime, Trip
from sum_gtfs_geojson.enums import DataType
from .abstract_loader import AbstractLoader
import logging

logger = logging.getLogger(__name__)

STOPS_FILE_PATH = "data/living_labs/geneva/gtfs/stops.txt"
ROUTES_FILE_PATH = "data/living_labs/geneva/gtfs/routes.txt"
TRIPS_FILE_PATH = "data/living_labs/geneva/gtfs/trips.txt"
STOPTIMES_FILE_PATH = "data/living_labs/geneva/gtfs/stop_times.txt"
BIKES_STOPS_FILEPATH = "data/living_labs/geneva/gbfs/shared_bikes_stations_2024.xlsx"
RIDERSHIP_FILE_PATH = "data/living_labs/geneva/mobility/ridership_2024.csv"
BIKE_TRIPS_FILE_PATH = "data/living_labs/geneva/mobility/shared_bikes_trips.csv"


def clean_datetime(dt_str):
    # Remove ' UTC' and microseconds if present
    dt_str = dt_str.replace(' UTC', '')
    if '.' in dt_str:
        dt_str = dt_str.split('.')[0]
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")


def safe_get(row, key, default=None, dtype=None):
    val = row.get(key, default)
    if pd.isna(val):
        return default
    if dtype:
        try:
            return dtype(val)
        except Exception:
            return default
    return val


class GenevaLoader(AbstractLoader):
    def load_stops(self):
        """ Load GTFS stops from the GTFS data file
        Geneva headers in file :
        stop_id,stop_name,stop_lat,stop_lon,stop_desc,zone_id,stop_url,location_type,parent_station
        Returns:
            list[Stop]: A list of Stop objects representing the stops in the GTFS data.
        """
        print("Loading GTFS stops...")
        public_transport_stations = pd.read_csv(STOPS_FILE_PATH)
        public_transport_stations = public_transport_stations.where(
            pd.notnull(public_transport_stations), None)
        stops = []
        for _, row in public_transport_stations.iterrows():
            try:
                stops.append(
                    Stop(
                        stop_id=safe_get(row, "stop_id", ""),
                        stop_name=safe_get(row, "stop_name", ""),
                        stop_lat=safe_get(row, "stop_lat", None, float),
                        stop_lon=safe_get(row, "stop_lon", None, float),
                        stop_desc=safe_get(row, "stop_desc", None),
                        zone_id=safe_get(row, "zone_id", None),
                        stop_url=safe_get(row, "stop_url", None),
                        location_type=safe_get(row, "location_type", 0, int),
                        parent_station=safe_get(row, "parent_station", None),
                    )
                )
            except ValidationError as e:
                # logger.exception(f"ValidationError in load_stops: {e}")
                continue
        print("Success lines to process / total lines : ",
              len(stops), "/", len(public_transport_stations))
        return stops

    def load_routes(self):
        """ Load GTFS routes from the GTFS data file
        Geneva headers in file :
        route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color
        Returns:
            list[Route]: A list of Route objects representing the routes in the GTFS data.
        """
        print("Loading GTFS routes...")
        public_transport_routes = pd.read_csv(ROUTES_FILE_PATH)
        public_transport_routes = public_transport_routes.where(
            pd.notnull(public_transport_routes), None)
        routes = []
        for _, row in public_transport_routes.iterrows():
            try:
                routes.append(
                    Route(
                        route_id=safe_get(row, "route_id", ""),
                        agency_id=safe_get(row, "agency_id", "", str),
                        route_short_name=safe_get(row, "route_short_name", ""),
                        route_long_name=safe_get(row, "route_long_name", ""),
                        route_desc=safe_get(row, "route_desc", None),
                        route_type=safe_get(row, "route_type", ""),
                        route_url=safe_get(row, "route_url", None),
                        route_color=safe_get(row, "route_color", None),
                        route_text_color=safe_get(
                            row, "route_text_color", None),
                    )
                )
            except ValidationError as e:
                # logger.exception(f"ValidationError in load_routes: {e}")
                continue
        print("Success lines to process / total lines : ",
              len(routes), "/", len(public_transport_routes))
        return routes

    def load_trips(self):
        """ Load GTFS trips from the GTFS data file 
        Geneva headers in file : 
        route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id,trip_type
        Returns:
            list[Trip]: A list of Trip objects representing the trips in the GTFS data.
        """
        print("Loading GTFS trips...")
        public_transport_trips = pd.read_csv(TRIPS_FILE_PATH)
        public_transport_trips = public_transport_trips.where(
            pd.notnull(public_transport_trips), None)
        print("Trips lines to process: ", len(public_transport_trips))

        trips = []
        for _, row in public_transport_trips.iterrows():
            try:
                trips.append(
                    Trip(
                        route_id=safe_get(row, "route_id", "", str),
                        service_id=safe_get(row, "service_id", "", str),
                        trip_id=safe_get(row, "trip_id", "", str),
                        trip_headsign=safe_get(
                            row, "trip_headsign", None, str),
                        trip_short_name=safe_get(
                            row, "trip_short_name", None, str),
                        direction_id=safe_get(row, "direction_id", None, int),
                        block_id=safe_get(row, "block_id", None, str),
                        shape_id=safe_get(row, "shape_id", None, str),
                    )
                )
            except ValidationError as e:
                logger.exception(f"ValidationError in load_trips: {e}")
                continue
        print("Success lines to process / total lines : ",
              len(trips), "/", len(public_transport_trips))
        return trips

    def load_stop_times(self):
        """ Load GTFS stop_times from the GTFS data file
        Geneva headers in file :
        trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled

        Returns:
            list[StopTime]: A list of StopTime objects representing the stop times in the GTFS data.
        """
        print("Loading GTFS stop_times...")
        public_transport_stop_times = pd.read_csv(STOPTIMES_FILE_PATH)
        public_transport_stop_times = public_transport_stop_times.where(
            pd.notnull(public_transport_stop_times), None)
        print("Stop times lines to process: ",
              len(public_transport_stop_times))

        stop_times = []
        for _, row in public_transport_stop_times.iterrows():
            try:
                stop_times.append(
                    StopTime(
                        trip_id=safe_get(row, "trip_id", "", str),
                        arrival_time=safe_get(row, "arrival_time", "", str),
                        departure_time=safe_get(
                            row, "departure_time", "", str),
                        stop_id=safe_get(row, "stop_id", "", str),
                        stop_sequence=safe_get(row, "stop_sequence", 0, int),
                        stop_headsign=safe_get(
                            row, "stop_headsign", None, str),
                        pickup_type=safe_get(row, "pickup_type", None, int),
                        drop_off_type=safe_get(
                            row, "drop_off_type", None, int),
                        shape_dist_traveled=safe_get(
                            row, "shape_dist_traveled", None, float),
                        timepoint=safe_get(row, "timepoint", None, int),
                    )
                )
            except ValidationError as e:
                logger.exception(f"ValidationError in load_stop_times: {e}")
                continue
        print("Success lines to process / total lines : ",
              len(stop_times), "/", len(public_transport_stop_times))
        return stop_times

    def load_bike_stations(self):
        """ Load bike sharing stations from the GBFS data file
        Geneva headers in file :
        name	latitude	longitude
        Returns:
            list[StationInfoStatus]: A list of StationInfoStatus objects representing the bike sharing stations.
        """
        print("Loading bike sharing stations...")
        shared_bikes_stations = pd.read_excel(BIKES_STOPS_FILEPATH)
        shared_bikes_stations = shared_bikes_stations.where(
            pd.notnull(shared_bikes_stations), None)
        bike_stations = []
        for _, row in shared_bikes_stations.iterrows():
            try:
                bike_stations.append(
                    StationInfoStatus(
                        station_id=safe_get(row, "name", ""),
                        name=safe_get(row, "name", ""),
                        lat=safe_get(row, "latitude", None, float),
                        lon=safe_get(row, "longitude", None, float),
                        short_name="",
                        address="",
                        capacity=None,
                        region_id="",
                        rental_methods=None,
                        has_kiosk=None,
                        history=[],
                    )
                )
            except ValidationError as e:
                logger.exception(f"ValidationError in load_bike_stations: {e}")
                continue
        print("Success lines to process / total lines : ",
              len(bike_stations), "/", len(shared_bikes_stations))
        return bike_stations

    def load_ridership(self):
        """ Load ridership data from the Excel file
        Geneva headers in file :
        Date	Timeslot	Index Day Week	Line Type	Schedule Type	Line	Stop	Long Code Stop	Number of Boarding Passengers	Number of Disembarking Passengers	jour_semaine	Week Index	Month Year	Stop Latitudes	Stop Longtitudes	Final Data	filter_graph

        Returns:
            list[Ridership]: A list of Ridership objects representing the ridership data.
        """
        print("Loading ridership data...")
        public_transport_ridership = pd.read_csv(RIDERSHIP_FILE_PATH)
        public_transport_ridership = public_transport_ridership.where(
            pd.notnull(public_transport_ridership), None)
        ridership_data = []
        for _, row in public_transport_ridership.iterrows():
            try:
                ridership_data.append(
                    Ridership(
                        date=safe_get(row, "Date", "", str),
                        timeslot=safe_get(row, "Timeslot", "", str),
                        day_index=safe_get(row, "Index Day Week", 0, int),
                        line_type=safe_get(row, "Line Type", "", str),
                        schedule_type=safe_get(row, "Schedule Type", "", str),
                        line=safe_get(row, "Line", "", str),
                        stop_name=safe_get(row, "Stop", "", str),
                        stop_code=safe_get(row, "Long Code Stop", "", str),
                        boardings=safe_get(
                            row, "Number of Boarding Passengers", 0, int),
                        alightings=safe_get(
                            row, "Number of Disembarking Passengers", 0, int),
                        day_label=safe_get(row, "jour_semaine", ""),
                        week_index=safe_get(row, "Week Index", 0, int),
                        month_year=safe_get(row, "Month Year", "", str),
                        stop_lat=safe_get(row, "Stop Latitudes", None, float),
                        stop_lon=safe_get(
                            row, "Stop Longtitudes", None, float),
                        is_final=bool(safe_get(row, "Final Data", False)),
                        is_filtered=bool(safe_get(row, "filter_graph", False)),
                    )
                )
            except ValidationError as e:
                logger.exception(f"ValidationError in load_ridership: {e}")
                continue
        print("Success lines to process / total lines : ",
              len(ridership_data), "/", len(public_transport_ridership))
        return ridership_data

    def load_bike_trips(self):
        """ Load bike trips data from the CSV file
        Geneva headers in file :
        trip_id,rental_id,vehicle_type,trip_started_at_utc,trip_ended_at_utc,latitude_start,longitude_start,latitude_end,longitude_end,distance_in_km

        Returns:
            list[BikeTrip]: A list of BikeTrip objects representing the bike trips data.
        """
        print("Loading bike trips data...")
        bike_trips = pd.read_csv(BIKE_TRIPS_FILE_PATH)
        bike_trips = bike_trips.where(pd.notnull(bike_trips), None)
        bike_trips_data = []
        for _, row in bike_trips.iterrows():
            try:
                bike_trips_data.append(
                    BikeTrip(
                        trip_id=safe_get(row, "trip_id", "", str),
                        rental_id=safe_get(row, "rental_id", "", str),
                        vehicle_type=safe_get(row, "vehicle_type", "", str),
                        trip_started_at_utc=safe_get(
                            row, "trip_started_at_utc", "", str),
                        trip_ended_at_utc=safe_get(
                            row, "trip_ended_at_utc", "", str),
                        latitude_start=safe_get(
                            row, "latitude_start", None, float),
                        longitude_start=safe_get(
                            row, "longitude_start", None, float),
                        latitude_end=safe_get(
                            row, "latitude_end", None, float),
                        longitude_end=safe_get(
                            row, "longitude_end", None, float),
                        distance_in_km=safe_get(
                            row, "distance_in_km", None, float),
                    )
                )
            except ValidationError as e:
                logger.exception(
                    f"ValidationError in load_bike_trips for line {row.index}: {e}")
                continue
        print("Success lines to process / total lines : ",
              len(bike_trips_data), "/", len(bike_trips))
        return bike_trips_data
