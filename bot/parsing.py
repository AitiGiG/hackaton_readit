from decouple import config
import aiohttp

API = config('URL')

class UserRegister:
    id = 0
    def __init__(self,data):
       self.data = data
       self.headers = {}

    async def register_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + '/account/register/',json = self.data) as response:
                result = await response.json()
                if "email" in result and result["email"] == ["user with this email already exists."]:
                    return f'Пользователь с таким email уже существует'
                elif type(result) == dict:
                    self.id = result.get('id')
                    return f'Поздрваляю,вы создали аккаунт\nВам на почту пришла ссылка, перейдите по ней,\n и введите код чтобы активировать аккаунт'

    async def login_api(self):
        data = self.data
        # data.pop('username')
        # data.pop('password_confirm')
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + '/account/login/',json = data) as response:
                result = await response.json()
                if result.get('detail') == 'No active account found with the given credentials':
                    return False
                else:
                    return result
    async def activate_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + '/account/activate/',json = {'activation_code':self.data['activation_code']}) as response:
                result = await response.json()
                if type(result) == dict:
                    res = await self.login_api()
                    self.headers = res
                return result
    
    async def get_user_profile(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url = API + f'/account/user/{self.id}/') as response:
                result = await response.json()
                raise Exception(result)
                return result
            
            

