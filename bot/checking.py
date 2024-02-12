
import re
from aiogram.fsm.state import StatesGroup ,State
class UserRegisterState(StatesGroup):
    email = State()
    username = State()
    password = State()
    password_confirm = State() 
    activation_code = State()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    if len(password) < 8:
        return False
    return True

print(UserRegisterState.email)