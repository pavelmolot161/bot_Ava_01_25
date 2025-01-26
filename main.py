### - 12.01.25
### - Бот будет работать на версии 3.9 !!!!!!!!!!!!!!!!!!!!!!!
### - Use this token to access the HTTP API:
### - ИМЯ БОТА - bot_Ava                                          временный T_raining_Bot
### - ИМЯ БОТА для внутренней работы и настройки - Ava_01_25_bot  временный T_raining_Bot


from aiogram import Bot, Dispatcher, executor, types  # Импорт необходимых классов из библиотеки aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импорт хранилища для состояний
import asyncio  # Импорт библиотеки asyncio для асинхронного программирования
from aiogram.dispatcher.filters.state import State, StatesGroup  # Импорт классов для работы с состояниями
from aiogram.dispatcher import FSMContext  # Импорт контекста состояний
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


API_TOKEN = '8072047087:AAGDSoPN8p0j_fZajx3hm8QMQJ1zGsIsuic'  # Токен Вашего бота

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)  # Создание экземпляра бота
storage = MemoryStorage()  # Создание хранилища для состояний
dp = Dispatcher(bot, storage=storage)  # Создание диспетчера для обработки сообщений

# Определение состояний
class Form(StatesGroup):  # Класс для определения состояний
    main_menu = State()  # Состояние для основного меню

@dp.message_handler(commands=['start'])  # Обработчик команды /start
async def cmd_start(message: types.Message):  # Асинхронная функция для обработки команды
    await message.answer("Добро пожаловать в bot Ava! Выберите опцию:",
                         reply_markup=main_menu_keyboard())  # Отправка приветственного сообщения с кнопками
# Основное меню
def main_menu_keyboard():  # Функция для создания клавиатуры основного меню
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создание клавиатуры с возможностью изменения размера
    keyboard.add("Рецепты", "Здоровье", "Фото канала", "Животные")  # Добавление кнопок в клавиатуру
    keyboard.add("Дополнительные функции", "Ссылки и ресурсы", "Беседка")  # Добавление дополнительных кнопок
    return keyboard  # Возврат созданной клавиатуры


@dp.message_handler(lambda message: message.text == "Назад в меню")        # Обработчик для кнопки "Назад в меню"
async def back_to_main_menu(message: types.Message):                      # Асинхронная функция для возврата в главное меню
    await message.answer("Вы вернулись в главное меню:",
                         reply_markup=main_menu_keyboard())               # Ответ с возвратом в главное меню


# Обработка выбора в основном меню
@dp.message_handler(lambda message: message.text == "Рецепты")            # Обработчик для кнопки "Рецепты"
async def recipes_menu(message: types.Message):                           # Асинхронная функция для обработки выбора
    await message.answer("Выберите категорию:",
                         reply_markup=recipes_keyboard())                 # Запрос выбора категории рецептов

def recipes_keyboard():  # Функция для создания клавиатуры категорий рецептов
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)             # Создание клавиатуры
    keyboard.add("Завтраки", "Ужины", "Десерты", "Вегетарианские")   # Добавление категорий
    keyboard.add("Назад в меню")                                           # Кнопка для возврата в основное меню
    return keyboard               # Возврат клавиатуры

# 3) Расчет калорий ____________________________________________________________________________________

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Определение состояний пользователя
class UserState(StatesGroup):
    age = State()      # Состояние для ввода возраста
    growth = State()   # Состояние для ввода роста
    weight = State()   # Состояние для ввода веса


with open('Formula_San_Zeora.txt', 'r', encoding='utf-8') as file:
    text_about_calories = file.read()

# Обработка выбора Расчета калорий
@dp.message_handler(lambda message: message.text == "Здоровье")  # Обработчик для кнопки "Здоровье"
async def recipes_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    await message.answer("Рассчитать норму калорий:", reply_markup=recipes_keyboard())

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.add(button, button2)

@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=kb)

@dp.callback_query_handler(text='formulas')  # Обработчик для кнопки "Формулы расчёта"
async def get_formulas(call):
    await call.message.answer(text_about_calories)
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст: ")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост: ")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес: ")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age

    await message.answer(f"Ваш приблизительный суточный расход калорий: {calories}")

    # Удаляем данные о пользователе после расчета
    await state.finish()  # Завершаем состояние
#____________________________________________________________________________________________________________________


# Обработка выбора категории рецептов
@dp.message_handler(lambda message: message.text in ["Завтраки", "Ужины", "Десерты", "Вегетарианские"])  # Обработчик для категорий рецептов
async def send_recipes(message: types.Message):                             # Асинхронная функция для отправки рецептов
    await message.answer(f"Вот несколько рецептов для {message.text}!",
                         )                 # Ответ с предложением рецептов и кнопкой "Назад в меню"


# 1)_________________________________________________________________________________________________________________

# # Обработка других кнопок
# @dp.message_handler(lambda message: message.text == "Фото канала")              # Обработчик для кнопки "Пейзажи"
# async def landscapes_menu(message: types.Message):                          # Асинхронная функция для обработки выбора
#     await message.answer("Вот красивые фотографии пейзажей!",
#                          )                                       # Ответ с фотографиями пейзажей и кнопкой "Назад в меню"


@dp.message_handler(lambda message: message.text == "Фото канала")  # Обработчик для кнопки "Фото канала"
async def landscapes_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    await message.answer("Перейдите по ссылке на папку с фотографиями:",
                         reply_markup=types.InlineKeyboardMarkup().add(
                             types.InlineKeyboardButton("Перейти к фото",
                             url="https://photos.google.com/share/AF1QipOzji_5ZJd4GLg28voPaFGOmj_kQNnC0ShYsTVXgZX0_4leVTeX15hpLFfdOn40xg?key=cjFFUmpRcWdVQnVKdDlaYWkwaU5rYnhIVzMzTDRB")  # Ссылка на папку
                         ))                                                                       # Добавление кнопки с ссылкой

#______________________________________________________________________________________________________________________









@dp.message_handler(lambda message: message.text == "Животные")             # Обработчик для кнопки "Животные"
async def animals_menu(message: types.Message):                             # Асинхронная функция для обработки выбора
    await message.answer("Вот милые фотографии животных!",
                         )                 # Ответ с фотографиями животных и кнопкой "Назад в меню"

@dp.message_handler(lambda message: message.text == "Дополнительные функции")  # Обработчик для кнопки "Дополнительные функции"
async def additional_features_menu(message: types.Message):                 # Асинхронная функция для обработки выбора
    await message.answer("Выберите опцию:",
                         reply_markup=additional_features_keyboard())       # Запрос выбора дополнительных функций

@dp.message_handler(lambda message: message.text == "Обратная связь")       # Обработчик для кнопки "Обратная связь"
async def feedback_menu(message: types.Message):                            # Асинхронная функция для обработки выбора
    await message.answer("Отправьте свой отзыв:",
                         )                 # Ответ с запросом отзыва и кнопкой "Назад в меню"

def additional_features_keyboard():                                              # Функция для создания клавиатуры дополнительных функций
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)                   # Создание клавиатуры
    keyboard.add("Обратная связь", "Подписка на новости", "Назад в меню")  # Добавление кнопок
    return keyboard  # Возврат клавиатуры

@dp.message_handler(lambda message: message.text == "Подписка на новости")        # Обработчик для кнопки "Подписка на новости"
async def subscription_menu(message: types.Message):                              # Асинхронная функция для обработки выбора
    await message.answer("Вы подписаны на новости!",
                         )                       # Ответ с подтверждением подписки и кнопкой "Назад в меню"

# 2) ___________________________________________________________________________________________________________________

@dp.message_handler(lambda message: message.text == "Ссылки и ресурсы")           # Обработчик для кнопки "Ссылки и ресурсы"
async def links_resources_menu(message: types.Message):                           # Асинхронная функция для обработки выбора
    keyboard = InlineKeyboardMarkup()  # Создание инлайн-клавиатуры
    keyboard.add(InlineKeyboardButton("Перейти на YouTube канал 'Все обо Всем'",
                                       url="https://youtube.com/@elena_ivanovaaa?si=jye0JlS9ozmRTrqF"))  # Кнопка с ссылкой
    keyboard.add(InlineKeyboardButton("Перейти на Дзен канал 'Pantera Volna'",
                                       url="https://dzen.ru/id/64de5ea842a0d1556b524b48"))  # Кнопка с ссылкой
    await message.answer("Вот ссылки на мои каналы!", reply_markup=keyboard)  # Ответ с клавиатурой

# @dp.message_handler(lambda message: message.text == "Ссылки и ресурсы")           # Обработчик для кнопки "Ссылки и ресурсы"
# async def links_resources_menu(message: types.Message):                           # Асинхронная функция для обработки выбора
#     await message.answer("Вот ссылки на наши социальные сети и блог!",
#                          )                       # Ответ с ссылками и кнопкой "Назад в меню"

#______________________________________________________________________________________________________________________


@dp.message_handler(lambda message: message.text == "Беседка")                    # Обработчик для кнопки "Беседка"
async def gazebo_menu(message: types.Message):                                    # Асинхронная функция для обработки выбора
    await message.answer("Добро пожаловать в беседку! Здесь Вы можете задавать вопросы и участвовать в опросах.",
                         )  # Ответ с информацией о беседке и кнопкой "Назад в меню"

# Запуск бота
if __name__ == '__main__':  # Проверка, что скрипт запускается напрямую
    executor.start_polling(dp, skip_updates=True)  # Запуск бота и обработка обновлений