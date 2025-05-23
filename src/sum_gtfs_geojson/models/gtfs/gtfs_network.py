from typing import List, Dict, Tuple
from pydantic import Field
from .. import SumGtfsBaseModel
from shapely.geometry import Point, LineString, mapping
import geopandas as gpd
from . import Stop, Route, Trip, StopTime, Itinerary
from collections import defaultdict
import json


class GTFSNetwork(SumGtfsBaseModel):
    """
    Represents the full public transport network described by GTFS files.

    Attributes:
        stops: All GTFS stops (stations or platforms).
        routes: All GTFS routes (lines).
        trips: All trips (vehicle runs) along routes.
        stop_times: Stop-by-stop itineraries for each trip.
    """
    stops: List[Stop] = Field(default_factory=list)
    routes: List[Route] = Field(default_factory=list)
    trips: List[Trip] = Field(default_factory=list)
    stop_times: List[StopTime] = Field(default_factory=list)
    itineraries: List[Itinerary] = Field(default_factory=list)

    def stops_to_geojson(self, filepath: str = None) -> gpd.GeoDataFrame:
        """
        Export stops as a GeoJSON file, with stop information as properties.
        Args:
            filepath (str): The path to the output GeoJSON file. Optional, if defined it will be saved to this path.
        """
        if not self.stops:
            return
        gdf = gpd.GeoDataFrame(
            [s.model_dump() for s in self.stops],
            geometry=[Point(s.stop_lon, s.stop_lat)
                      for s in self.stops if s.stop_lon is not None and s.stop_lat is not None],
            crs="EPSG:4326"
        )
        if (filepath is not None):
            gdf.to_file(filepath, driver="GeoJSON")

        return gdf

    def itineraries_to_geojson(self, filepath: str = None) -> gpd.GeoDataFrame:
        """
        Export each route's itinerary as a GeoJSON LineString, using stop sequences for each trip.

        Args:
            filepath (str): The path to the output GeoJSON file. Optional, if defined it will be saved to this path.
        """
        print("Exporting itineraries to GeoJSON... for itineraries count = ", len(
            self.itineraries))
        if not self.itineraries:
            return
        features = []
        for itinerary in self.itineraries:
            coords = [(stop.stop_lon, stop.stop_lat)
                      for stop in itinerary.stops if stop.stop_lon is not None and stop.stop_lat is not None]
            if len(coords) < 2:
                continue
            feature = {
                "type": "Feature",
                "geometry": mapping(LineString(coords)),
                "properties": {
                    "route_id": itinerary.route_id,
                    "direction_id": itinerary.direction_id,
                    "trip_id": itinerary.trip_id,
                    "headsign": itinerary.headsign,
                    "route_short_name": itinerary.route_short_name,
                    "route_long_name": itinerary.route_long_name,
                    "route_type": itinerary.route_type,
                    "color": itinerary.color,
                    "text_color": itinerary.text_color
                }
            }
            features.append(feature)
        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }
        if filepath is not None:
            with open(filepath, 'w') as f:
                json.dump(feature_collection, f, indent=4)
        print(f"Exported {len(features)} itineraries to {filepath}")

        return gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")

    def build_itineraries(
        self,
        stops: List[Stop],
        stop_times: List[StopTime],
        trips: List[Trip],
        routes: List[Route]
    ) -> List[Itinerary]:
        """
        Constructs a list of Itinerary objects from GTFS data.

        Args:
            stops (List[Stop]): List of Stop instances.
            stop_times (List[StopTime]): List of StopTime instances.
            trips (List[Trip]): List of Trip instances.
            routes (List[Route]): List of Route instances.

        Returns:
            List[Itinerary]: A list of Itinerary objects representing unique route and direction combinations.
        """
        # Map stop_id to Stop object for quick lookup
        stop_lookup: Dict[str, Stop] = {stop.stop_id: stop for stop in stops}

        # Group stop_times by trip_id
        trip_stop_times: Dict[str, List[StopTime]] = defaultdict(list)
        for st in stop_times:
            trip_stop_times[st.trip_id].append(st)

        # Group trips by (route_id, direction_id) and select the first trip as representative
        trip_by_route_dir: Dict[Tuple[str, int], Trip] = {}
        for trip in trips:
            key = (trip.route_id, trip.direction_id or 0)
            if key not in trip_by_route_dir:
                trip_by_route_dir[key] = trip

        # Map route_id to Route object for metadata
        route_lookup: Dict[str, Route] = {
            route.route_id: route for route in routes}

        self.itineraries: List[Itinerary] = []

        for (route_id, direction_id), trip in trip_by_route_dir.items():
            stop_times_list = sorted(
                trip_stop_times.get(trip.trip_id, []),
                key=lambda st: st.stop_sequence
            )

            # Build the list of Stop instances for the itinerary
            itinerary_stops: List[Stop] = []
            for st in stop_times_list:
                stop = stop_lookup.get(st.stop_id)
                if stop:
                    itinerary_stops.append(stop)

            if len(itinerary_stops) < 2:
                continue  # Skip itineraries with insufficient stops

            route = route_lookup.get(route_id)

            itinerary = Itinerary(
                route_id=route.route_id if route else route_id,
                direction_id=direction_id,
                trip_id=trip.trip_id,
                headsign=trip.trip_headsign,
                route_short_name=route.route_short_name if route else None,
                route_long_name=route.route_long_name if route else None,
                route_type=route.route_type if route else None,
                color=route.route_color if route else None,
                text_color=route.route_text_color if route else None,
                stops=itinerary_stops
            )

            self.itineraries.append(itinerary)

        return self.itineraries
