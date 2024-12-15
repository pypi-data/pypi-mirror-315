from typing import Any, List, Optional
from typing_extensions import override
from influxdb_client_3 import InfluxDBClient3, Point
from masterpiece.timeseries import TimeSeries


class Influx(TimeSeries):
    """Influx time series database (version 3) for MasterPiece."""

    def __init__(self, name: str = "influx"):
        """Construct InfluxDB v3 client for writing and reading time series.

        Args:
            name (str, optional): Name of the object to be created. Defaults to "influx".
        """
        super().__init__(name)
        self.influx_client = InfluxDBClient3(
            host=self.host,
            token=self.token,
            org=self.org,
            database=self.database,
        )

    @override
    def write(self, point: Point) -> None:
        self.influx_client.write(record=point)

    @override
    def write_dict(
        self, name: str, tags: dict[str, Any], fields: dict[str, Any], ts: str
    ) -> None:
        point: dict[str, Any] = {
            "measurement": name,
            "tags": tags,
            "fields": fields,
            "time": ts,
        }
        self.influx_client.write(record=point)

    @override
    def read_dict(
        self,
        measurement: str,
        start_time: str,
        end_time: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        try:
            # Select specific fields or all fields
            fields_query = ", ".join(fields) if fields else "*"

            # Construct the base SQL query
            query = (
                f"SELECT {fields_query} FROM {measurement} WHERE time >= '{start_time}'"
            )
            if end_time:
                query += f" AND time <= '{end_time}'"

            # Add tag filters
            if tags:
                tag_conditions = " AND ".join(
                    f"{key} = '{value}'" for key, value in tags.items()
                )
                query += f" AND {tag_conditions}"

            # Order by time
            query += " ORDER BY time"

            # Execute the query
            result = self.influx_client.query(query)

            # Convert the result to a list of dictionaries
            records = []
            for row in result:
                records.append(dict(row))

            return records

        except Exception as e:
            raise Exception(f"Failed to read data: {e}")

    @override
    def read_point(
        self,
        measurement: str,
        start_time: str,
        end_time: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> list[Point]:

        try:
            # Select specific fields or all fields
            fields_query = ", ".join(fields) if fields else "*"

            # Construct the base SQL query
            query = (
                f"SELECT {fields_query} FROM {measurement} WHERE time >= '{start_time}'"
            )
            if end_time:
                query += f" AND time <= '{end_time}'"

            # Add tag filters
            if tags:
                tag_conditions = " AND ".join(
                    f"{key} = '{value}'" for key, value in tags.items()
                )
                query += f" AND {tag_conditions}"

            # Order by time
            query += " ORDER BY time"

            # Execute the query
            result = self.influx_client.query(query)

            # Convert the result to a list of Point objects
            points = []
            for row in result:
                point = Point(measurement)
                for key, value in row.items():
                    if key == "time":
                        point.time(value)
                    elif isinstance(value, (int, float)):
                        point.field(key, value)
                    else:
                        point.tag(key, value)
                points.append(point)

            return points

        except Exception as e:
            raise Exception(f"Failed to read data as Points: {e}")
