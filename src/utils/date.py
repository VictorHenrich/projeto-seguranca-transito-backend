from datetime import datetime


class DateUtils:
    @classmethod
    def parse_string_to_datetime(cls, date_string: str) -> datetime:
        try:
            return datetime.strptime(date_string, "%Y-%m-%d")
        except:
            try:
                return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

            except:
                return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
