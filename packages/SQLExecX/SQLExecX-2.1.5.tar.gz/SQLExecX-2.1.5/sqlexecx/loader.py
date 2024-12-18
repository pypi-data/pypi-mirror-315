# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import datetime, date


class Loader:

    def __init__(self, data, description):
        self.data = data
        self.description = description

    def to_df(self):
        """
        transform to DataFrame of pandas.
        :return DataFrame of pandas
        """
        use_polars = True
        try:
            import polars as pd
        except:
            try:
                import pandas as pd
                use_polars = False
            except:
                raise ModuleNotFoundError("No module named 'pandas', please install it use 'pip install pandas'")

        if self.description:
            description = [x[0] for x in self.description]
            if use_polars:
                return pd.DataFrame(data=self.data, schema=description, orient="row")
            else:
                return pd.DataFrame(data=self.data, columns=description)
            
        if use_polars:
            return pd.DataFrame(data=self.data, orient="row")
        else:
            return pd.DataFrame(data=self.data)

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        Save as csv
        :param file_name
        :param delimiter
        :param header bool, include header or not
        :param encoding default utf-8
        """
        import csv
        with open(file_name, 'w', newline='', encoding=encoding) as f:
            writer = csv.writer(f, delimiter=delimiter)
            if header and self.description:
                description = [x[0] for x in self.description]
                writer.writerow(description)
            writer.writerows(self.data)

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        Save as json
        :param file_name
        :param encoding default utf-8
        """
        import json
        from sqlexecutorx import Dict

        if self.data and self.description:
            names = [x[0] for x in self.description]
            data = list(map(lambda x: Dict(names, x), self.data))
            with open(file_name, 'w', encoding=encoding) as f:
                json.dump(data, f, default=_datetime_handler)


def _datetime_handler(obj):
    if isinstance(obj, datetime) or isinstance(obj, date):
        return obj.__str__()
