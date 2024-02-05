# import telebot
# from telebot import types
# from decouple import config
# from myapp.models import Post, User, Favorite, Like

# BOT_KEY = 'YOUR_TELEGRAM_BOT_TOKEN' 
# bot = telebot.TeleBot(BOT_KEY)

# users = {}

# def pretty_post(post):
#     title = post.title
#     content = post.content
#     created_at = post.created_at
#     return f'Заголовок: {title}\nСодержание: {content}\nСоздано: {created_at}'

# def send_next_post(message, posts, post_counter):
#     current_post = posts[post_counter]
#     response = pretty_post(current_post)
#     markup = types.InlineKeyboardMarkup()
#     id = current_post.id
#     like_data = json.dumps({'option': 'like', 'post_id': id})
#     skip_data = json.dumps({'option': 'skip', 'post_id': id})
#     like = types.InlineKeyboardButton(text='Лайк', callback_data=like_data)
#     skip = types.InlineKeyboardButton(text='Следующий', callback_data=skip_data)
#     markup.add(like, skip)
#     bot.send_message(message.chat.id, response, reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: True)
# def like_or_skip(callback):
#     callback_data = json.loads(callback.data)
#     if callback_data['option'] == 'like':
#         user_id = users['user'].id
#         post_id = callback_data['post_id']
        

#         like, created = Like.objects.get_or_create(user_id=user_id, post_id=post_id)
        
#         if created:
#             bot.answer_callback_query(callback.id, text='Пост лайкнут!')
#         else:
#             bot.answer_callback_query(callback.id, text='Вы уже лайкнули этот пост!')
#     else:
#         bot.answer_callback_query(callback.id, text='Вы пропустили этот пост')

# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Привет! Для начала войдите в свой аккаунт. Введите логин и пароль в формате:\nЛОГИН\nПАРОЛЬ')
#     bot.register_next_step_handler(message, auth_user)

# def auth_user(message):
#     login, password = message.text.split('\n')
    
#     user = User.objects.filter(username=login, password=password).first()
    
#     if user:
#         users['user'] = user
#         bot.send_message(message.chat.id, 'Вы успешно вошли в систему. Введите что-то, чтобы получить первый пост.')
#         bot.register_next_step_handler(message, send_posts)
#     else:
#         bot.register_next_step_handler(message, error)

# def send_posts(message):
#     user_id = users['user'].id
#     favorite_posts = Favorite.objects.filter(user_id=user_id)
    
#     if favorite_posts.exists():
#         for post in favorite_posts:
#             send_next_post(message, favorite_posts, post_counter)
#         bot.send_message(message.chat.id, 'Посты закончились')
#     else:
#         bot.send_message(message.chat.id, 'У вас нет избранных постов')

# def error(message):
#     bot.send_message(message.chat.id, 'Извините, но вы не вошли в систему')
