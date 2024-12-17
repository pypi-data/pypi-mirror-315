from typing import TypedDict


class ICategoriesConfigWikiMuscleUrl (TypedDict):
    muscles: str
    category: str
    difficulties: str


class Config:
    def __init__(self):
        self.__directory = self.url_api() + "exercise/exercises/directory/"
        self.__categories = {
            "muscles": self.url_api()+"muscle/muscles/",
            "category": self.url_api()+"exercise/categories/?enable=true",
            "difficulties": self.url_api()+"exercise/difficulties/"
        }
        self.__exercices = self.url_api() + "exercise/exercises/"

    @property
    def url_directory(self) -> str:
        return self.__directory

    @property
    def url_categories(self) -> ICategoriesConfigWikiMuscleUrl:
        return self.__categories
    
    @property
    def url_exercise(self) -> str:
        return self.__exercices

    def url_api(self) -> str:
        return "https://musclewiki.com/newapi/"
