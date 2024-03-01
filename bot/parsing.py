from decouple import config
import aiohttp

URL = config('URL')

class UserRegister:
    
    def __init__(self,data):
       self.data = data
       self.headers = {}
       self.user_id = None
    
    async def register_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url = URL + 'account/register/',json = self.data) as response:
                result = await response.json()
                if "email" in result and result["email"] == ["user with this email already exists."]:
                    return f'Пользователь с таким email уже существует'
                elif type(result) == dict:
                    print(result)
                    self.user_id = result.get('id')
                    return f'Поздрваляю,вы создали аккаунт\nВам на почту пришла ссылка, перейдите по ней,\n и введите код чтобы активировать аккаунт'

    async def login_api(self):
        data = self.data
        # data.pop('username')
        # data.pop('password_confirm')
        async with aiohttp.ClientSession() as session:
            async with session.post(url = URL + 'account/login/',json = data) as response:
                result = await response.json()
                if result.get('detail') == 'No active account found with the given credentials':
                    return False
                else:
                    print(result)
                    self.headers = result
                    return result
    async def activate_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url = URL + 'account/activate/',json = {'activation_code':self.data['activation_code']}) as response:
                result = await response.json()
                if type(result) == dict:
                    res = await self.login_api()
                    self.headers = res
                return result
    
    async def get_user_profile(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            print(self.id)
            async with session.get(url = URL + f'account/user/{self.id}/') as response:
                result = await response.json()
                return result
            
            

