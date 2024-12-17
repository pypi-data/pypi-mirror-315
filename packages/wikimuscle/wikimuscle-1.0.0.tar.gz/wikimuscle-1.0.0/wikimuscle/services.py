from requests.exceptions import HTTPError, Timeout, RequestException
import wikimuscle.config as config_wiki
import requests
from typing import Union


class Services:
    def __init__(self) -> None:
        self.config = config_wiki.Config()

    def request_services(self, url: str, to_json: bool = False, to_text: bool = False) -> Union[dict, str, requests.Response]:
        try:
            headers = {"Accept-Language": "fr-fr"} 
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            if to_json:
                return response.json()
            elif to_text:
                return response.text
            else:
                return response

        except HTTPError as http_err:
            raise Exception(f"HTTPError: {http_err}")
        except Timeout:
            raise Exception("Request timeout")
        except RequestException as req_err:
            raise Exception(f"RequestException: {req_err}")
        except Exception as e:
            raise Exception(f"General error: {e}")

    def request_donwload_video(self, url:str, path:str) -> str:
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(path, "wb") as file:
                    for chunck in response.iter_content(chunk_size=8192):
                        if chunck:
                            file.write(chunck)
                return path
        except HTTPError as http_err:
            raise Exception(f"HTTPError: {http_err}")           
        except Timeout:
            raise Exception("Request timeout")
        except RequestException as req_err:
            raise Exception(f"RequestException: {req_err}")
        except Exception as e:
            raise Exception(f"General error: {e}")
        
        
    def get_categories_url(self):
        categories = self.config.url_categories
        result = {}
        for cat, url in categories.items():
            req = self.request_services(url, True)
            result[cat] = req['results']
        return result
