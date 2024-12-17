from datetime import datetime
import pandas as pd
import json
from opengate_data.utils.utils import send_request, handle_exception, set_method_call, validate_type
from flatten_dict import unflatten

class PandasIotCollectionBuilder:
    """Optimized Pandas IoT Collection Builder"""

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.headers = self.client.headers
        self.method_calls = []
        self.dataframe = None
        self.columns = []
        self.payload = {"devices": {}}

    @set_method_call
    def from_dataframe(self, df: pd.DataFrame):
        validate_type(df, pd.DataFrame, "Dataframe")
        if not {'device_id', 'at'}.issubset(df.columns):
            raise ValueError("The dataframe must contain 'device_id' and 'at' columns.")
        now_milliseconds = int(datetime.now().timestamp() * 1000)
        df['at'] = df['at'].apply(lambda x: now_milliseconds if pd.isna(x) or x == '' else self._convert_to_milliseconds(x))
        self.dataframe = df
        self._process_dataframe()
        return self

    @set_method_call
    def with_columns(self, columns):
        validate_type(columns, list, "Columns")
        for column in columns:
            validate_type(column, str, "Column name")
        self.columns = columns

        if self.dataframe is not None:
            missing_columns = [col for col in columns if col not in self.dataframe.columns]
            if missing_columns:
                raise ValueError(f"Missing columns in dataframe: {', '.join(missing_columns)}")
        else:
            raise ValueError("Dataframe must be set before calling with_columns().")

        return self

    @set_method_call
    def build(self):
        self._validate_build()
        return self

    @set_method_call
    def build_execute(self, include_payload=False):
        self._validate_build()
        results = self._execute_pandas_collection(include_payload)
        self.dataframe['status'] = self.dataframe['device_id'].apply(
            lambda device_id: "Success" if device_id in results and all(r['status_code'] == 201 for r in results[device_id]) else "Failed"
        )
        return self.dataframe

    @set_method_call
    def execute(self, include_payload=False):
        if 'build' not in self.method_calls and 'build_execute' not in self.method_calls:
            raise ValueError("You need to call build() or build_execute() before execute().")
        results = self._execute_pandas_collection(include_payload)
        self.dataframe['status'] = self.dataframe['device_id'].apply(
            lambda device_id: "Success" if device_id in results and all(r['status_code'] == 201 for r in results[device_id]) else "Failed"
        )
        return self.dataframe

    def _validate_build(self):
        if self.dataframe is None:
            raise ValueError("Dataframe is not set. Call from_dataframe() before build().")
        if self.columns:
            missing_columns = [col for col in self.columns if col not in self.dataframe.columns]
            if missing_columns:
                raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    def _process_dataframe(self):
        required_columns = ['device_id', 'at']
        optional_columns = ['origin_device_identifier', 'version', 'path', 'trustedboot', 'from']

        datastream_columns = self.columns or [col for col in self.dataframe.columns if col not in required_columns + optional_columns]
        if not datastream_columns:
            raise ValueError("No datastream columns found in the dataframe.")

        unflats = []
        for df_dict in self.dataframe.to_dict(orient='records'):
            if any('_' in key for key in df_dict.keys()):
                unflat = unflatten(df_dict, splitter='underscore')
                unflats.append(self._add_underscore_to_current_keys(unflat))
            elif any('.' in key for key in df_dict.keys()):
                unflat = unflatten(df_dict, splitter='dot')
                unflats.append(self._add_underscore_to_current_keys(unflat))
            else:
                raise ValueError('Column names must be linked with "_" or "."')

        now_milliseconds = int(datetime.now().timestamp() * 1000)

        def process_row(row):
            device_id = row['device_id']
            at = row['at']  # The 'at' column is already converted during `from_dataframe`.
            from_ = self._convert_to_milliseconds(row.get('from'))

            if device_id not in self.payload['devices']:
                self.payload['devices'][device_id] = {
                    "datastreams": [],
                    "version": "1.0.0",
                    **{field: row[field] for field in optional_columns if field in row and pd.notna(row[field])}
                }

            for col in datastream_columns:
                value = row.get(col)
                if isinstance(value, (list, dict)):
                    valid_value = bool(value)  # Non-empty list or dict
                else:
                    valid_value = pd.notna(value)  # Scalars

                if valid_value:
                    validate_type(value, (int, str, float, bool, dict, list), f"Datastream value for {col}")
                    if col.startswith("entity.location"):
                        value = {
                            "position": {
                                "type": "Point",
                                "coordinates": value
                            }
                        }
                    datapoint = {"value": value, "at": at, "from": from_} if from_ else {"value": value, "at": at}

                    existing_ds = next((ds for ds in self.payload['devices'][device_id]['datastreams'] if ds['id'] == col), None)
                    if existing_ds:
                        existing_ds['datapoints'].append(datapoint)
                    else:
                        self.payload['devices'][device_id]['datastreams'].append({"id": col, "datapoints": [datapoint]})

        self.dataframe.apply(process_row, axis=1)

    def _add_underscore_to_current_keys(self, dct: dict):
        for key in list(dct.keys()):
            if isinstance(dct[key], dict):
                self._add_underscore_to_current_keys(dct[key])
            if key == 'current':
                dct[f'_{key}'] = dct.pop(key)

        return dct

    @staticmethod
    def _convert_to_milliseconds(value):
        if pd.isna(value) or value == '':
            return int(datetime.now().timestamp() * 1000)
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            return int(pd.to_datetime(value).timestamp() * 1000)
        if isinstance(value, datetime):
            return int(value.timestamp() * 1000)
        raise ValueError(f"Invalid timestamp value: {value}")

    def _execute_pandas_collection(self, include_payload):
        results = {}

        for device_id, device_data in self.payload['devices'].items():
            url = f"{self.client.url or 'https://connector-tcp:9443'}/south/v80/devices/{device_id}/collect/iot"
            batches = self._split_into_batches(device_data)

            for batch in batches:
                try:
                    response = send_request(method='post', headers=self.headers, url=url, json_payload=batch)
                    result = {'status_code': response.status_code}
                    if include_payload and response.status_code == 201:
                        result['payload'] = batch
                    results.setdefault(device_id, []).append(result)
                except Exception as e:
                    return handle_exception(e)

        return results

    def _split_into_batches(self, device_data):
        batches, current_batch = [], {"datastreams": [], "version": device_data["version"]}

        for datastream in device_data["datastreams"]:
            current_batch["datastreams"].append(datastream)

        if current_batch["datastreams"]:
            batches.append(current_batch)

        return batches
