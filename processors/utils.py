import os, unidecode, requests, yaml
from pathlib import Path
from pydash import strings
from dateutil.relativedelta import relativedelta

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
    def to_int(cls, s):
        if not s or not cls.is_number(s): return s
        return int(s)

    @classmethod
    def subtract_months(cls, from_day, months):
        return cls.add_to_date(from_day = from_day, months = -1 * months)

    @classmethod
    def add_to_date(cls, from_day, years = 0, weeks =0, months = 0, days =0, hours=0, minutes = 0, seconds = 0):
        return from_day + relativedelta(years = years, months = months, weeks = weeks, days = days, hours = hours, minutes = minutes, seconds= seconds)
    
    @classmethod
    def parse_date(cls, text):
        if not text: return None
        if isinstance(text, datetime):
            return text

        if cls.is_number(text):
            return datetime.fromtimestamp(Utils.to_int(text)/1000.0)

        if not text.__contains__("T"):
            return parser.parse(text)

        # apply UTC correction - as isofomat is not not adjusting time when tzinfo is UTC properly
        t = strings.split(text, "T")
        date_part = t[0]
        time_offset_part = t[1] if cls.size(t) > 1 else "00:00:00"
        time_part = time_offset_part
        offset_part = "00:00"
        operator = 1
        if time_offset_part.__contains__("+"):
            operator = 1
            parts = strings.split(time_offset_part, "+")
            time_part = parts[0]
            offset_part = parts[1] if cls.size(parts) > 1 else "00:00"
        elif time_offset_part.__contains__("-"):
            operator = -1
            parts = strings.split(time_offset_part, "-")
            time_part = parts[0]
            offset_part = parts[1] if cls.size(parts) > 1 else "00:00"

        new_date_text = f'{date_part}T{time_part}Z'
        hours = 0
        minutes = 0
        if offset_part != "00:00":
            hours_minutes = offset_part.split(":")
            hours = operator * int(hours_minutes[0])
            minutes = operator * int(hours_minutes[1]) if cls.size(hours_minutes) > 1 else 0

        d = parser.parse(new_date_text)
        d = cls.add_to_date(d, hours = hours, minutes = minutes)

        return d

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

class Commit:

    def __init__(self, sha, pr_url, created, pr_urls = []):
        self.sha = sha
        self.pr_url = pr_url
        self.created = created
        self.pr_urls = pr_urls or []

    @classmethod
    def to_dict(cls, c):
        if not c:
            return {}

        return {
            "sha": c.sha,
            "pr_url": c.pr_url,
            "created": Utils.format_date(c.created)
        }

    @classmethod
    def earliest(cls, c1, c2):
        if not c1:
            return c2
        if not c2:
            return c1

        return c1 if c1.created < c2.created else c2

