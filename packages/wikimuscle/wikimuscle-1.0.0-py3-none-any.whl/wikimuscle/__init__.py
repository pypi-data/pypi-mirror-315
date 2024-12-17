from wikimuscle.apiwiki import ApiWiki
from typing import Optional, Union
from pathlib import Path
from os import PathLike
from wikimuscle.interfaces import *
from wikimuscle.categories_url import *
from wikimuscle.config import Config
from wikimuscle.services import Services


class Wiki(ApiWiki):
    def __init__(self, path_database: Optional[Union[str, PathLike, Path]] = None):
        if isinstance(path_database, str):
            path = Path(path_database).joinpath('database')
        elif isinstance(path_database, Path):
            path = path_database.joinpath('database')
        elif path_database is None:
            path = Path().cwd().joinpath('database')
        elif isinstance(path_database, PathLike):
            path = Path(path_database).joinpath("database")
        path.mkdir(parents=True, exist_ok=True)
        self.path_database = path.as_posix()
        super().__init__(self.path_database)

    def get(
        self,
        muscles: Optional[List[MusclesCategory]] = None, equipments: Optional[List[EquipmentsCategory]] = None, difficulties: Optional[List[DifficultiesCategory]] = None,
        path_json: Optional[Union[str, PathLike, Path]] = None,
        create_dir:bool=False,
        dir_exercises: Optional[Union[str, PathLike, Path]] = None
        ):
        resp, resp_original = super().get(muscles, equipments, difficulties)
        if path_json:
            self.write_file_json(path_json, resp)
        if create_dir:
            self.create_dir(dir_exercises, resp_original)
        return resp, resp_original

    def create_dir_exercise(self, base_path: Optional[Union[str, PathLike, Path]] = None, element: Optional[IResponseExercise] = None):
        if base_path is None:
            base_path = Path().cwd()
        if element is None:
            return None
        return super().create_dir_exercise(base_path, element)

    def create_dir(self, base_path: Optional[Union[str, PathLike, Path]] = None, data: Optional[List[IResponseExercise]] = None):
        if base_path is None:
            base_path = Path().cwd()
        if data is None:
            return None

        base_path = Path(base_path).joinpath("exercises")
        base_path.mkdir(exist_ok=True, parents=True)

        for element in data:
            self.create_dir_exercise(base_path, element)

        return None
