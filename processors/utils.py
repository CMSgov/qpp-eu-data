import os, unidecode, requests, yaml
from pathlib import Path
from pydash import strings
from dateutil.relativedelta import relativedelta
from datetime import datetime, timezone

class Config:

    def __init__(self):
        super().__init__()
        with open(os.path.join(FileUtils.get_root(), "config.yml"), 'r') as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)

    def get(self, key):
        return Utils.get_value(self._config, key)

class FileUtils:

    @classmethod
    def get_root(cls):
        path = Path(__file__)
        return path.parent.parent

    @classmethod
    def absolute_path(cls, folder, file_name=None):
        if file_name is not None:
            return cls.get_root().joinpath(folder).joinpath(file_name)
        return cls.get_root().joinpath(folder)

    @classmethod
    def mkdirs(cls, path):
        Path(path).mkdir(parents=True, exist_ok=True)

class Utils:
    @classmethod
    def remove_accents(cls, s):
        unaccented_string = unidecode.unidecode(s)
        return unaccented_string

    @classmethod
    def remove_all(cls, str, to_delete = []):
        s1 = str
        for s in to_delete:
            s1 = strings.replace(s1, s, "", ignore_case=True)
        return s1

    @classmethod
    def subtract_months(cls, from_day, months):
        return cls.add_to_date(from_day = from_day, months = -1 * months)

    @classmethod
    def add_to_date(cls, from_day, years = 0, weeks =0, months = 0, days =0, hours=0, minutes = 0, seconds = 0):
        return from_day + relativedelta(years = years, months = months, weeks = weeks, days = days, hours = hours, minutes = minutes, seconds= seconds)

    @classmethod
    def format_date(cls, the_date):
        if the_date: return the_date.isoformat()
        return None
    
    @classmethod
    def get_value(cls, dict, key):
        v = dict
        for p in strings.split(key, "."):
            if v is None: continue
            v = v.get(p)
        return v

    @classmethod
    def now(cls):
        d = datetime.utcnow()
        return d.replace(tzinfo= timezone.utc)

class APIUtils:
    @classmethod
    def http_get(cls, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            raise requests.exceptions.HTTPError(errh)
        except requests.exceptions.ConnectionError as errc:
            raise requests.exceptions.ConnectionError(errc)
        except requests.exceptions.Timeout as errt:
            raise requests.exceptions.Timeout(errt)
        except requests.exceptions.RequestException as err:
            raise requests.exceptions.RequestException(err)