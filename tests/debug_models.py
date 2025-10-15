import json
import os
from src.models import Vacancy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "data", "vacancies.json")

data = json.load(open(file_path, encoding="utf-8"))
first = data["items"][0]
vac = Vacancy.from_api_to_dict(first)

print(vac._url)