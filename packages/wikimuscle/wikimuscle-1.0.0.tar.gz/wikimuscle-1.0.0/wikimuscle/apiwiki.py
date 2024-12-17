from wikimuscle.services import Services
from wikimuscle.categories_url import CategoriesUrl
from wikimuscle.config import Config
from wikimuscle.interfaces import (MusclesCategory,
                                   DifficultiesCategory,
                                   EquipmentsCategory,
                                   IResponseExercise,
                                   _IMuscles, _IImage)
from typing import Literal, Union, List, Optional, Tuple, Dict
import json
import pathlib as plib


class ApiWiki:
    def __init__(self, path_database: str):
        self.path_database = path_database
        self.category_url = CategoriesUrl(self.path_database)
        self.config = Config()
        self.services = Services()

    def get_category(self, category: Literal["muscles", "equipments", "difficulties"]) -> Union[MusclesCategory, EquipmentsCategory, DifficultiesCategory]:
        if category == "equipments":
            cat = "category"
        else:
            cat = category
        result = []
        for el in self.category_url.data[cat]:
            result.append(el["name"])
        return result

    def get(self, muscles: Optional[List[MusclesCategory]] = None, equipments: Optional[List[EquipmentsCategory]] = None, difficulties: Optional[List[DifficultiesCategory]] = None):
        url = self.url(muscles, equipments, difficulties)
        return self.__fetch(url)

    def url(self, muscles: Optional[List[MusclesCategory]] = None, equipments: Optional[List[EquipmentsCategory]] = None, difficulties: Optional[List[DifficultiesCategory]] = None) -> str:
        base_url = self.config.url_directory
        query = {}
        if muscles:
            query["muscles"] = f"muscles={self.category_url.encode_url(
                self.category_url.get_ids("muscles", muscles))}"
        if equipments:
            query["equipment"] = f"equipment={self.category_url.encode_url(
                self.category_url.get_ids("category", equipments))}"
        if difficulties:
            query["difficulty"] = f"difficulty={self.category_url.encode_url(
                self.category_url.get_ids("difficulties", difficulties))}"

        url = self.category_url.parse_url(base_url, query)
        return url

    def __fetch(self, url: str) -> Tuple[Dict[str, IResponseExercise], List[IResponseExercise]]:
        resp = self.services.request_services(url)
        content: list = resp.json()
        results = []
        results_brut = []
        for target in content:
            endpoint = target["target_url"]["male"].split("/")[-1]
            format_url = self.config.url_exercise+"?slug="+endpoint
            request = self.services.request_services(format_url, True)[
                "results"][0]
            format_response: IResponseExercise = {
                "muscles": [{
                    "description": i["description"],
                    "id": i["id"],
                    "description_us": i["description_en_us"],
                    "name": i["name"],
                    "name_en_us": i["name_en_us"],
                    "scientific_name": i["scientific_name"],
                    "url_name": i["url_name"]
                } for i in request["muscles"]],
                "muscles_primary": self.__format_muscles(request["muscles_primary"]),
                "muscles_secondary": self.__format_muscles(request["muscles_secondary"]),
                "muscles_tertiary": self.__format_muscles(request["muscles_tertiary"]),
                "grips": [{
                    "id": i["id"],
                    "name": i["name"],
                    "name_en_us": i["name_en_us"],
                    "description": i["description"],
                    "description_en_us": i["description_en_us"],
                    "url_name": i["url_name"]
                } for i in request["grips"]],
                "category": {
                    "id": request["category"]["id"],
                    "name": request["category"]["name"],
                    "name_en_us": request["category"]["name_en_us"]
                },
                "additional_categories": [{
                    "id": i["id"],
                    "name": i["name"],
                    "name_en_us": i["name_en_us"]
                } for i in request["additional_categories"]],
                "difficulty": request["difficulty"],
                "force": request["force"],
                "mechanic": request["mechanic"],
                "images": [self.__format_images(image) for image in request["images"]],
                "correct_steps": [step for step in request["correct_steps"]],
                "target_url": request["target_url"],
                "female_images": [self.__format_images(image) for image in request["female_images"]],
                "male_images": [self.__format_images(image) for image in request["male_images"]],
                "name": request["name"],
                "slug": request["slug"]
            }
            results.append({endpoint: format_response})
            results_brut.append(format_response)
        return results, results_brut

    def __format_muscles(self, muscles):
        if muscles is None:
            return None

        if isinstance(muscles, list):
            for m in muscles:
                for key in ["lft", "rght", "tree_id", "level", "parent"]:
                    if key in m:
                        del m[key]
            return muscles
        else:
            for key in ["lft", "rght", "tree_id", "level", "parent"]:
                if key in muscles:
                    del muscles[key]
            return muscles

    def __format_images(self, image) -> _IImage:
        del image["dst_link"]
        return image

    def write_file_json(self, path, data) -> None:
        with open(path, "w") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
        return None

    def write_file(self, path, data) -> None:
        with open(path, "w") as file:
            file.writelines(data)
        return None

    def create_str(self, data) -> str:
        result = ""
        for i in data:
            result += f"{i} \n"
        return result.strip()

    def create_dir_exercise(self, base_path, element: IResponseExercise) -> None:
        images = element["images"]
        name_dir = element["name"]
        path_dir = plib.Path(base_path).joinpath(name_dir)
        path_dir.mkdir(exist_ok=True, parents=True)
        for image in images:
            if image["gender"] == 1:
                url_img = image["original_video"]
                path_img = path_dir.joinpath(
                    f"{name_dir}-{image["exercise"]}.mp4")
                self.services.request_donwload_video(
                    url_img, path_img.as_posix())
        steps = element["correct_steps"]
        sorted_steps = sorted(steps, key=lambda step: step["order"])
        steps_str = [i["text"] for i in sorted_steps]
        path_steps = path_dir.joinpath("steps.txt").as_posix()
        self.write_file(path_steps, self.create_str(steps_str))
        return None
