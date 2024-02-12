from decouple import config
import aiohttp

API = config('URL')

class UserRegister:
    
    def __init__(self,data):
       self.data = data
       self.headers = {}

    async def register_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + 'account/register/',json = self.data) as response:
                result = await response.json()
                if "email" in result and result["email"] == ["user with this email already exists."]:
                    return f'Пользователь с таким email уже существует'
                elif type(result) == dict:
                    return f'Поздрваляю,вы создали аккаунт\nВам на почту пришла ссылка, перейдите по ней,\n и введите код чтобы активировать аккаунт'

    async def activate_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + 'account/activate/',json = self.data) as response:
                result = await response.json()
                return result
            
    async def login_api(self):
        data = self.data.copy()
        data.pop('username')
        data.pop('last_name')
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + '/account/login/',json = data) as response:
                result = await response.json()
                if result.get('detail') == 'No active account found with the given credentials':
                    return False
                else:
                    return True
            

