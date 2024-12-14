import requests
from pydantic import BaseModel


from ...Utilites.system_logging import SysLogging, TypeLogging
from ...Application.Abstractions.base_rest_client import BaseRestClientFWDI
from ...Application.DTO.Auth.login_response import LoginResponse

class RestClientFWDI(BaseRestClientFWDI):
    def __init__(self):
        super().__init__()
        self.__is_init:bool = False
        self.__log__ = SysLogging(logging_level=TypeLogging.DEBUG, filename=f"RestClientFWDI")

    def init(self, config:any):
        from ...Infrastructure.Configs.rest_client_config import RestClientConfig
        self.__log__(f"{__name__}:{config}", 'debug')
        
        self.__config:RestClientConfig = config
        if hasattr(config, 'security_layer'):
            self.__schem:str = 'http' if not config.security_layer else 'https'
        else:
            self.__schem:str = 'http'

        self.__base_url = f'{self.__schem}://{self.__config.server}:{self.__config.port}'
        self.__is_auth: bool = False
        self.__token:str = ''
        self.__headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization':''
        }
        self.__is_init = True
    
    @property
    def IsAuth(self):
        return self.__is_auth if self.__is_init else False
        

    def login(self, url:str='/token')->bool:
        if not self.__is_init:
            raise Exception("RestClient not init !!!")
        
        self.__log__(f"{__name__}:{url}", 'debug')
        response = requests.post(f'{self.__base_url}{url}', 
                                 data = {'username': self.__config.username,'password': self.__config.password}) 
        self.__log__(f"{__name__}:{response}", 'debug')

        if response.status_code == 200:
            response_json = response.json()
            if 'access_token' in response_json:
                response_toke = LoginResponse(**response.json())
                self.__token = response_toke.access_token
                self.__headers["Authorization"] = f"Bearer {self.__token}"
                self.__is_auth = True
                
                return True
            else:
                print(f'Error auth:{response}')
                unknow_error = response.json()
                print(unknow_error)

                return False
        elif response.status_code == 401:
            error_auth = response.json()
            print(f"Error:{error_auth}, code: {response.status_code}")
            self.__log__(f"Error:{error_auth}, code: {response.status_code}", 'debug')

            return False
    
    def get(self, path:str, _data:BaseModel=None)->tuple|None:
        if not self.__is_init:
            raise Exception("RestClient not init !!!")

        self.__log__(f"{__name__}:{path}:{_data}", 'debug')
        if len(self.__token) > 0:
            if not _data is None:
                response_get = requests.get(f"{self.__base_url}{path}", data=_data.model_dump_json(), headers=self.__headers)
            else:
                response_get = requests.get(f"{self.__base_url}{path}", headers=self.__headers)
                
            self.__log__(f"{__name__}:{response_get}", 'debug')

            if response_get.status_code == 200:
                return response_get.json(), response_get.status_code
            else:
                error_json = response_get.json()
                if 'detail' in error_json:
                    if error_json['detail'] == 'Could not validate credentials':
                        if self.login():
                            return self.get(path, _data)

                return response_get, response_get.status_code
        else:
            return None

    def post(self, path:str, _data:BaseModel)->tuple|None:
        if not self.__is_init:
            raise Exception("RestClient not init !!!")

        self.__log__(f"{__name__}:{path}:{_data}", 'debug')
        if len(self.__token) > 0:
            response_post = requests.post(f"{self.__base_url}{path}", data=_data.model_dump_json(), headers=self.__headers)
            self.__log__(f"{__name__}:{response_post}", 'debug')

            if response_post.status_code == 200:
                return response_post.json(), response_post.status_code
            else:
                error_json = response_post.json()
                if 'detail' in error_json:
                    if error_json['detail'] == 'Could not validate credentials':
                        if self.login():
                            return self.get(path, _data)

                return response_post, response_post.status_code
        else:
            return None