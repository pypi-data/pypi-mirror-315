from wikimuscle.services import Services
from wikimuscle.interfaces import ISubCategoriesUrl, ICategoriesUrl
import json
import pathlib as plib
from typing import List, Literal


class CategoriesUrl:
    def __init__(self, path_database: str):
        self.path_database = path_database
        self.services = Services()

        if not plib.Path(self.path_database).joinpath("categories").exists():
            self.__resp = self._get_services()
        else:
            self.__resp = self.load_categories()

    @property
    def data(self) -> ICategoriesUrl:
        return self.__resp

    def _get_services(self):
        resp = self.services.get_categories_url()
        categories_url: ICategoriesUrl = {}
        for cat, req in resp.items():
            list_sub_cat = []
            for el in req:

                if cat == "difficulties" and el['id'] == 4:
                    sub_cat: ISubCategoriesUrl = {
                        "name": "Novice",
                        "id_name": el['id']
                    }
                    list_sub_cat.append(sub_cat)
                elif el["name"] and el["id"]:
                    sub_cat: ISubCategoriesUrl = {
                        "name": el['name'],
                        "id_name": el['id']
                    }
                    list_sub_cat.append(sub_cat)
            categories_url[cat] = list_sub_cat
        self.save_categories_url(categories_url)
        return categories_url

    def save_categories_url(self, data: ICategoriesUrl) -> None:
        path = plib.Path(self.path_database).joinpath("categories.json")
        with open(path, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
        return None

    def load_categories(self) -> ICategoriesUrl:
        path = plib.Path(self.path_database).joinpath("categories.json")
        with open(path, "r", encoding="utf-8") as file:
            buffer = file.read()
            data = json.loads(buffer)
        return data

    def get_ids(self, category: Literal["muscles", "category", "difficulties"], data: List[str]) -> list:
        result = []
        for i in data:
            el = self.data[category]
            for j in el:
                if j["name"] == i:
                    result.append(str(j["id_name"]))

        if len(result) < 0:
            raise Exception("No params found")
        return result

    def encode_url(self, encode_query: List[int]) -> str:
        return "%2C".join(encode_query)

    def parse_url(self, base: str, query: dict) -> str:
        query_string = "&".join(query.values())
        return f"{base}?{query_string}"
