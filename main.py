# ### - 12.01.25 работа 10 часов
# ### - 26.01.25 работа 6 часов
# ### - 27.01.25 работа 4 часа
# ### - 28.02.25 работа 3 часа перезапуск и обновление

#
# ### - Бот будет работать на версии 3.9 !!!!!!!!!!!!!!!!!!!!!!!
# ### - Use this token to access the HTTP API:
# ### - ИМЯ БОТА - Ava                                          временный T_raining_Bot
# ### - ИМЯ БОТА для внутренней работы и настройки - Ava_01_25_bot  временный T_raining_Bot

import os
from aiogram import Bot, Dispatcher, executor, types  # Импорт необходимых классов из библиотеки aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импорт хранилища для состояний
import asyncio  # Импорт библиотеки asyncio для асинхронного программирования
from aiogram.dispatcher.filters.state import State, StatesGroup  # Импорт классов для работы с состояниями
from aiogram.dispatcher import FSMContext  # Импорт контекста состояний
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from datetime import datetime  # Импорт модуля datetime для работы с датой и временем

API_TOKEN = '8072047087:AAGDSoPN8p0j_fZajx3hm8QMQJ1zGsIsuic'  # Токен Вашего бота

# ____ПРОВЕРКА НА НАЛИЧИЕ ДРУГОГО ЭКЗАМПЛЯРА БОТА - ???_________________________________________________________________

# # Путь к файлу блокировки
# LOCK_FILE = 'bot.lock'
#
# # Проверка наличия другого экземпляра бота
# if os.path.exists(LOCK_FILE):
#     print("Бот уже запущен. Завершите предыдущий экземпляр перед запуском нового.")
#     exit(1)
#
# # Создание файла блокировки
# with open(LOCK_FILE, 'w') as f:
#     f.write("locked")

# ______________________________________________________________________________________________________________________

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)  # Создание экземпляра бота
storage = MemoryStorage()  # Создание хранилища для состояний
dp = Dispatcher(bot, storage=storage)  # Создание диспетчера для обработки сообщений

# Словарь с ссылками на папки Google Drive для категорий рецептов
FOLDER_LINKS = {
    "Завтраки": "https://drive.google.com/drive/folders/19eIGch4MuF91kpPiq_aMt0EKC5ijEkwR",
    "Ужины": "https://drive.google.com/drive/folders/139F1dcIHtRASsLD082g7IQUGzn6zTRcI",
    "Десерты": "https://drive.google.com/drive/folders/1BTSk4V4WJ5CdL9tW7n9fz71PeBVKq-C2",
    "Вегетарианские": "https://drive.google.com/drive/folders/176ugjLUVq53ScteUFmMNcQDsZjcQBKQp"
}


# Определение состояний
class Form(StatesGroup):  # Класс для определения состояний
    main_menu = State()  # Состояние для основного меню
    height = State()
    weight = State()
    gender = State()
    age = State()
    body_type = State()


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


@dp.message_handler(lambda message: message.text == "Назад в меню")  # Обработчик для кнопки "Назад в меню"
async def back_to_main_menu(message: types.Message):  # Асинхронная функция для возврата в главное меню
    await message.answer("Вы вернулись в главное меню:",
                         reply_markup=main_menu_keyboard())  # Ответ с возвратом в главное меню


# Обработка выбора в основном меню
@dp.message_handler(lambda message: message.text == "Рецепты")  # Обработчик для кнопки "Рецепты"
async def recipes_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    await message.answer("Выберите категорию:",
                         reply_markup=recipes_keyboard())  # Запрос выбора категории рецептов


def recipes_keyboard():  # Функция для создания клавиатуры категорий рецептов
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создание клавиатуры
    keyboard.add("Завтраки", "Ужины", "Десерты", "Вегетарианские")  # Добавление категорий
    keyboard.add("Назад в меню")  # Кнопка для возврата в основное меню
    return keyboard  # Возврат клавиатуры


# Обработка выбора категории рецептов - ОБНОВЛЕННАЯ ВЕРСИЯ С ССЫЛКАМИ НА GOOGLE DRIVE
@dp.message_handler(lambda message: message.text in ["Завтраки", "Ужины", "Десерты", "Вегетарианские"])
async def send_recipes(message: types.Message):
    category = message.text

    # Получаем ссылку на папку из словаря
    folder_link = FOLDER_LINKS.get(category)

    if folder_link:
        # Создаем инлайн-кнопку для перехода в папку
        inline_kb = types.InlineKeyboardMarkup()
        inline_kb.add(types.InlineKeyboardButton(
            "📂 Открыть папку с рецептами",
            url=folder_link
        ))

        # Отправляем сообщение с кнопкой
        await message.answer(
            f"🍽️ Вот рецепты для категории '{category}':\n\n"
            f"Нажмите кнопку ниже, чтобы перейти в папку с рецептами на Google Drive.\n\n"
            f"В папке вы найдете:\n"
            f"• Рецепты в разных форматах\n"
            f"• Изображения блюд\n"
            f"• Дополнительные материалы",
            reply_markup=inline_kb
        )
    else:
        await message.answer(
            f"Извините, ссылка на папку с рецептами '{category}' временно недоступна.",
            reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад в меню")
        )


# 3) Расчет калорий ____________________________________________________________________________________

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Определение состояний пользователя
class UserState(StatesGroup):
    gender = State()  # Состояние для выбора пола
    age = State()  # Состояние для ввода возраста
    growth = State()  # Состояние для ввода роста
    weight = State()  # Состояние для ввода веса
    activity_level = State()  # Состояние для выбора уровня активности


# with open('Formula_San_Zeora.txt', 'r', encoding='utf-8') as file: ### - надо или нет   ???
#     text_about_calories = file.read()


# Обработка выбора Расчета калорий
@dp.message_handler(lambda message: message.text == "Здоровье")  # Обработчик для кнопки "Здоровье"
async def health_menu(message: types.Message):  # Асинхронная функция для обработки выбора

    kb = InlineKeyboardMarkup()  # Создание инлайн-клавиатуры
    button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
    button2 = InlineKeyboardButton(text='Формулы расчёта калорий', callback_data='formulas')
    button3 = InlineKeyboardButton(text='Рассчитать норму веса', callback_data='weight_in_kg')
    button4 = InlineKeyboardButton(text='Информация о весе', callback_data='weight_is_calculated')
    kb.add(button, button2)  # Добавление кнопок в инлайн-клавиатуру
    kb.add(button3, button4)  # Добавление кнопок в инлайн-клавиатуру

    await message.answer("Выберите опцию:", reply_markup=kb)  # Отправка сообщения с инлайн-клавиатурой


# @dp.message_handler(text='Рассчитать')
# async def main_menu(message: types.Message):
#     await message.answer('Выберите опцию:', reply_markup=kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    # Чтение содержимого файла
    with open('Formula_San_Zeora.txt', 'r', encoding='utf-8') as file:
        text_about_calories = file.read()

    # Отправка содержимого файла пользователю
    await call.message.answer(text_about_calories)
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call):
    await call.message.answer("Выберите Ваш пол: \n1. Мужчина\n2. Женщина")
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message: types.Message, state: FSMContext):
    gender = message.text.strip()
    if gender not in ["1", "2"]:
        await message.answer("Пожалуйста, выберите 1 для Мужчины или 2 для Женщины.")
        return
    await state.update_data(gender=gender)
    await message.answer("Введите свой возраст (от 13 до 80 лет): ")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    age = message.text.strip()
    if not age.isdigit() or not (13 <= int(age) <= 80):
        await message.answer("Пожалуйста, введите корректный возраст от 13 до 80 лет.")
        return
    await state.update_data(age=age)
    await message.answer("Введите свой рост (в см): ")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (в кг): ")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_activity_level(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer(
        "Выберите уровень активности:\n1. Минимальная активность (1.2)\n2. Слабый уровень активности (1.375)\n3. Умеренный уровень активности (1.55)\n4. Тяжелая активность (1.7)\n5. Экстремальный уровень (1.9)")
    await UserState.activity_level.set()


@dp.message_handler(state=UserState.activity_level)
async def send_calories(message: types.Message, state: FSMContext):
    activity_level = message.text.strip()
    if activity_level not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, выберите уровень активности от 1 до 5.")
        return

    await state.update_data(activity_level=activity_level)
    data = await state.get_data()

    age = int(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])
    gender = data['gender']

    # Определяем коэффициент активности
    activity_coefficients = {
        "1": 1.2,
        "2": 1.375,
        "3": 1.55,
        "4": 1.7,
        "5": 1.9
    }
    A = activity_coefficients[activity_level]

    # Расчет калорий по формуле Миффлина-Сан Жеора
    if gender == "1":  # Мужчина
        calories = (10 * weight + 6.25 * growth - 5 * age + 5) * A
    else:  # Женщина
        calories = (10 * weight + 6.25 * growth - 5 * age - 161) * A

    await message.answer(f"Ваш приблизительный суточный расход калорий: {calories:.2f} ккал")

    # Удаляем данные о пользователе после расчета
    await state.finish()  # Завершаем состояние


# ____________________________________________________________________________________________________________________
# 3a)________________________________________________________________________________________________________________

@dp.callback_query_handler(text='weight_is_calculated')
async def get_weight_calc(call: types.CallbackQuery):
    print("Обработчик weight_is_calculated вызван")  # Логирование
    # Чтение содержимого файла
    with open('Weight_calculation.txt', 'r', encoding='utf-8') as file:
        text_weight_calculation = file.read()

        # Функция для разбивки текста на части для телеграма
        def split_text(text, max_length=4095):
            return [text[i:i + max_length] for i in range(0, len(text), max_length)]

        # Разделение текста на части
        text_parts = split_text(text_weight_calculation)

        # Отправка каждой части текста
        for part in text_parts:
            await call.message.answer(part)

        await call.answer()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'weight_in_kg')
async def calculate_weight_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Подтверждение нажатия кнопки
    await callback_query.message.answer("Введите рост в см:")
    await Form.height.set()  # Установка состояния


@dp.message_handler(state=Form.height)
async def process_height(message: types.Message, state: FSMContext):
    height_cm = float(message.text)
    await state.update_data(height=height_cm)  # Сохранение роста в состоянии
    await Form.next()  # Переход к следующему состоянию
    await message.answer("Введите вес в кг:")


@dp.message_handler(state=Form.weight)
async def process_weight(message: types.Message, state: FSMContext):
    weight_kg = float(message.text)
    await state.update_data(weight=weight_kg)  # Сохранение веса в состоянии
    await Form.next()  # Переход к следующему состоянию
    await message.answer("Введите пол (1 - мужчина, 2 - женщина):")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender_input = int(message.text)
    if gender_input == 1:
        gender = 'male'
    elif gender_input == 2:
        gender = 'female'
    else:
        await message.answer("Неверный ввод. Пожалуйста, введите 1 для мужчины или 2 для женщины.")
        return

    await state.update_data(gender=gender)  # Сохранение пола в состоянии
    await Form.next()  # Переход к следующему состоянию
    await message.answer("Введите возраст:")


# @dp.message_handler(state=Form.gender)
# async def process_gender(message: types.Message, state: FSMContext):
#     gender = message.text
#     await state.update_data(gender=gender)  # Сохранение пола в состоянии
#     await Form.next()  # Переход к следующему состоянию
#     await message.answer("Введите возраст:")

@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    await state.update_data(age=age)  # Сохранение возраста в состоянии
    await Form.next()  # Переход к следующему состоянию

    # Отправка изображения и выбор типа телосложения
    await message.answer_photo(photo=open('type_of_physique.png', 'rb'),
                               caption="Введите тип телосложения:\n1 - Астенический\n2 - Нормостенический\n3 - Гиперстенический:")


# @dp.message_handler(state=Form.age)
# async def process_age(message: types.Message, state: FSMContext):
#     age = int(message.text)
#     await state.update_data(age=age)  # Сохранение возраста в состоянии
#     await Form.next()  # Переход к следующему состоянию
#     await message.answer("Введите тип телосложения (астенический/нормостенический/гиперстенический):")

@dp.message_handler(state=Form.body_type)
async def process_body_type(message: types.Message, state: FSMContext):
    body_type_input = int(message.text)
    body_type = ""

    if body_type_input == 1:
        body_type = 'asthenic'
    elif body_type_input == 2:
        body_type = 'normostenic'
    elif body_type_input == 3:
        body_type = 'hypersthenic'
    else:
        await message.answer("Неверный ввод. Пожалуйста, введите 1, 2 или 3.")
        return

    await state.update_data(body_type=body_type)  # Сохранение типа телосложения в состоянии

    # Получение всех данных из состояния
    data = await state.get_data()
    height_cm = data['height']
    weight_kg = data['weight']
    gender = data['gender']
    age = data['age']
    body_type = data['body_type']

    def calculate_weight(height_cm, gender, age, body_type):
        # Расчет нормального веса по формуле Брока
        if gender.lower() == 'male':
            normal_weight = height_cm - 110
        else:
            normal_weight = height_cm - 100

        # Корректировка по возрасту
        if 20 <= age <= 30:
            normal_weight *= 0.89  # Уменьшение на 11%
        elif age > 50:
            normal_weight *= 1.06  # Увеличение на 6%

        # Корректировка по типу телосложения
        if body_type.lower() == 'asthenic':
            normal_weight *= 0.90  # Уменьшение на 10%
        elif body_type.lower() == 'hypersthenic':
            normal_weight *= 1.10  # Увеличение на 10%

        return normal_weight

    def calculate_bmi(weight_kg, height_m):
        bmi = weight_kg / (height_m ** 2)
        return bmi

    def classify_obesity(bmi):
        if bmi < 15:
            return "Острый недостаток веса"
        elif 15 <= bmi < 20:
            return "Недостаточная масса тела"
        elif 20 <= bmi < 25:
            return "Нормальный вес"
        elif 25 <= bmi < 30:
            return "Избыточная масса тела"
        elif 30 <= bmi < 35:
            return "Ожирение 1 степени"
        elif 35 <= bmi < 40:
            return "Ожирение 2 степени"
        else:
            return "Ожирение 3 степени"

    # Выполнение расчетов
    normal_weight = calculate_weight(height_cm, gender, age, body_type)
    height_m = height_cm / 100
    bmi = calculate_bmi(weight_kg, height_m)
    obesity_classification = classify_obesity(bmi)

    excess_weight = weight_kg - normal_weight if weight_kg > normal_weight else 0

    await message.answer(f"Нормальный вес: {normal_weight:.2f} кг")
    await message.answer(f"Индекс массы тела (ИМТ): {bmi:.2f}")
    await message.answer(f"Классификация ожирения: {obesity_classification}")
    await message.answer(f"Избыточный вес до нормы: {excess_weight:.2f} кг")

    await state.finish()  # Завершение состояния


# ____________________________________________________________________________________________________________________


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
                                                        url="https://photos.google.com/share/AF1QipOzji_5ZJd4GLg28voPaFGOmj_kQNnC0ShYsTVXgZX0_4leVTeX15hpLFfdOn40xg?key=cjFFUmpRcWdVQnVKdDlaYWkwaU5rYnhIVzMzTDRB")
                             # Ссылка на папку
                         ))  # Добавление кнопки с ссылкой


# ______________________________________________________________________________________________________________________


@dp.message_handler(lambda message: message.text == "Животные")  # Обработчик для кнопки "Животные"
async def animals_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    await message.answer("Вот милые фотографии животных!",
                         )  # Ответ с фотографиями животных и кнопкой "Назад в меню"


@dp.message_handler(
    lambda message: message.text == "Дополнительные функции")  # Обработчик для кнопки "Дополнительные функции"
async def additional_features_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    await message.answer("Выберите опцию:",
                         reply_markup=additional_features_keyboard())  # Запрос выбора дополнительных функций


@dp.message_handler(lambda message: message.text == "Обратная связь")  # Обработчик для кнопки "Обратная связь"
async def feedback_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    await message.answer("Отправьте свой отзыв:",
                         )  # Ответ с запросом отзыва и кнопкой "Назад в меню"


def additional_features_keyboard():  # Функция для создания клавиатуры дополнительных функций
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создание клавиатуры
    keyboard.add("Обратная связь", "Подписка на новости", "Назад в меню")  # Добавление кнопок
    return keyboard  # Возврат клавиатуры


@dp.message_handler(
    lambda message: message.text == "Подписка на новости")  # Обработчик для кнопки "Подписка на новости"
async def subscription_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    await message.answer("Вы подписаны на новости!",
                         )  # Ответ с подтверждением подписки и кнопкой "Назад в меню"


# 2) ___________________________________________________________________________________________________________________

@dp.message_handler(lambda message: message.text == "Ссылки и ресурсы")  # Обработчик для кнопки "Ссылки и ресурсы"
async def links_resources_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    print("Обработчик 'Ссылки и ресурсы' вызван")  # Логирование
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

# ______________________________________________________________________________________________________________________


@dp.message_handler(lambda message: message.text == "Беседка")  # Обработчик для кнопки "Беседка"
async def gazebo_menu(message: types.Message):  # Асинхронная функция для обработки выбора
    print("Обработчик 'Беседка' вызван")  # Логирование
    await message.answer("Добро пожаловать в беседку! Здесь Вы можете задавать вопросы и участвовать в опросах.",
                         )  # Ответ с информацией о беседке и кнопкой "Назад в меню")


# # Запуск бота
# if __name__ == '__main__':  # Проверка, что скрипт запускается напрямую
#     start_time = datetime.now()                                                                         # Получение текущего времени
#     print(f"Запуск бота в {start_time.strftime('%H:%M:%S')} дата {start_time.strftime('%d.%m.%Y')}г.")  # Логирование с датой и временем
#     try:
#         executor.start_polling(dp, skip_updates=True)                                                   # Запуск бота и обработка обновлений
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")                                                                 # Логирование ошибок
#     finally:
#         end_time = datetime.now()                                                                       # Получение времени завершения
#         print(f"Бот завершил работу в {end_time.strftime('%H:%M:%S')} дата {end_time.strftime('%d.%m.%Y')}г.")  # Логирование завершения работы бота
#
#     executor.start_polling(dp, skip_updates=True)                                                       # Запуск бота и обработка обновлений

is_running = False

if __name__ == '__main__':  # Проверка, что скрипт запускается напрямую, а не импортируется как модуль
    start_time = datetime.now()  # Получение текущего времени для логирования
    # Вывод в консоль времени запуска бота с форматированием
    print(f"Запуск бота в {start_time.strftime('%H:%M:%S')} дата {start_time.strftime('%d.%m.%Y')} г.")

    if not is_running:  # Проверка, запущен ли бот (флаг is_running должен быть False)
        is_running = True  # Установка флага, что бот запущен, чтобы предотвратить повторный запуск
        try:
            # Запуск бота с использованием метода start_polling, который начинает опрос обновлений
            executor.start_polling(dp, skip_updates=True)
        except Exception as e:  # Обработка любых исключений, которые могут возникнуть во время работы бота
            # Логирование ошибки в консоль, если что-то пошло не так
            print(f"Произошла ошибка: {e}")
        finally:
            end_time = datetime.now()  # Получение времени завершения работы бота
            # Вывод в консоль времени завершения работы бота с форматированием
            print(f"Бот завершил работу в {end_time.strftime('%H:%M:%S')} дата {end_time.strftime('%d.%m.%Y')} г.")
            is_running = False  # Сброс флага is_running при завершении работы бота
    else:
        # Если бот уже запущен, выводим сообщение о том, что нужно завершить предыдущий экземпляр
        print("Бот уже запущен. Завершите предыдущий экземпляр перед запуском нового.")













#____________________________________________________________________________________________________________________
#  - Старая но рабочая версия
#
# import os
# from aiogram import Bot, Dispatcher, executor, types             # Импорт необходимых классов из библиотеки aiogram
# from aiogram.contrib.fsm_storage.memory import MemoryStorage     # Импорт хранилища для состояний
# import asyncio                                                   # Импорт библиотеки asyncio для асинхронного программирования
# from aiogram.dispatcher.filters.state import State, StatesGroup  # Импорт классов для работы с состояниями
# from aiogram.dispatcher import FSMContext                        # Импорт контекста состояний
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query
# from datetime import datetime                                    # Импорт модуля datetime для работы с датой и временем
#
#
# API_TOKEN = '8072047087:AAGDSoPN8p0j_fZajx3hm8QMQJ1zGsIsuic'  # Токен Вашего бота
#
# #____ПРОВЕРКА НА НАЛИЧИЕ ДРУГОГО ЭКЗАМПЛЯРА БОТА - ???_________________________________________________________________
#
# # # Путь к файлу блокировки
# # LOCK_FILE = 'bot.lock'
# #
# # # Проверка наличия другого экземпляра бота
# # if os.path.exists(LOCK_FILE):
# #     print("Бот уже запущен. Завершите предыдущий экземпляр перед запуском нового.")
# #     exit(1)
# #
# # # Создание файла блокировки
# # with open(LOCK_FILE, 'w') as f:
# #     f.write("locked")
#
# #______________________________________________________________________________________________________________________
#
# # Инициализация бота и диспетчера
# bot = Bot(token=API_TOKEN)  # Создание экземпляра бота
# storage = MemoryStorage()  # Создание хранилища для состояний
# dp = Dispatcher(bot, storage=storage)  # Создание диспетчера для обработки сообщений
#
# # Определение состояний
# class Form(StatesGroup):  # Класс для определения состояний
#     main_menu = State()  # Состояние для основного меню
#     height = State()
#     weight = State()
#     gender = State()
#     age = State()
#     body_type = State()
#
# @dp.message_handler(commands=['start'])  # Обработчик команды /start
# async def cmd_start(message: types.Message):  # Асинхронная функция для обработки команды
#     await message.answer("Добро пожаловать в bot Ava! Выберите опцию:",
#                          reply_markup=main_menu_keyboard())  # Отправка приветственного сообщения с кнопками
# # Основное меню
# def main_menu_keyboard():  # Функция для создания клавиатуры основного меню
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создание клавиатуры с возможностью изменения размера
#     keyboard.add("Рецепты", "Здоровье", "Фото канала", "Животные")  # Добавление кнопок в клавиатуру
#     keyboard.add("Дополнительные функции", "Ссылки и ресурсы", "Беседка")  # Добавление дополнительных кнопок
#     return keyboard  # Возврат созданной клавиатуры
#
#
# @dp.message_handler(lambda message: message.text == "Назад в меню")        # Обработчик для кнопки "Назад в меню"
# async def back_to_main_menu(message: types.Message):                      # Асинхронная функция для возврата в главное меню
#     await message.answer("Вы вернулись в главное меню:",
#                          reply_markup=main_menu_keyboard())               # Ответ с возвратом в главное меню
#
#
# # Обработка выбора в основном меню
# @dp.message_handler(lambda message: message.text == "Рецепты")            # Обработчик для кнопки "Рецепты"
# async def recipes_menu(message: types.Message):                           # Асинхронная функция для обработки выбора
#     await message.answer("Выберите категорию:",
#                          reply_markup=recipes_keyboard())                 # Запрос выбора категории рецептов
#
# def recipes_keyboard():  # Функция для создания клавиатуры категорий рецептов
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)             # Создание клавиатуры
#     keyboard.add("Завтраки", "Ужины", "Десерты", "Вегетарианские")   # Добавление категорий
#     keyboard.add("Назад в меню")                                           # Кнопка для возврата в основное меню
#     return keyboard               # Возврат клавиатуры
#
# # 3) Расчет калорий ____________________________________________________________________________________
#
# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
#
# # Определение состояний пользователя
# class UserState(StatesGroup):
#     gender = State()  # Состояние для выбора пола
#     age = State()     # Состояние для ввода возраста
#     growth = State()  # Состояние для ввода роста
#     weight = State()  # Состояние для ввода веса
#     activity_level = State()  # Состояние для выбора уровня активности
#
# # with open('Formula_San_Zeora.txt', 'r', encoding='utf-8') as file: ### - надо или нет   ???
# #     text_about_calories = file.read()
#
#
# # Обработка выбора Расчета калорий
# @dp.message_handler(lambda message: message.text == "Здоровье")  # Обработчик для кнопки "Здоровье"
# async def health_menu(message: types.Message):  # Асинхронная функция для обработки выбора
#
#     kb = InlineKeyboardMarkup()  # Создание инлайн-клавиатуры
#     button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
#     button2 = InlineKeyboardButton(text='Формулы расчёта калорий', callback_data='formulas')
#     button3 = InlineKeyboardButton(text='Рассчитать норму веса', callback_data='weight_in_kg')
#     button4 = InlineKeyboardButton(text='Информация о весе', callback_data='weight_is_calculated')
#     kb.add(button, button2)  # Добавление кнопок в инлайн-клавиатуру
#     kb.add(button3, button4)  # Добавление кнопок в инлайн-клавиатуру
#
#     await message.answer("Выберите опцию:", reply_markup=kb)  # Отправка сообщения с инлайн-клавиатурой
#
# # @dp.message_handler(text='Рассчитать')
# # async def main_menu(message: types.Message):
# #     await message.answer('Выберите опцию:', reply_markup=kb)
#
# @dp.callback_query_handler(text='formulas')
# async def get_formulas(call: types.CallbackQuery):
#     # Чтение содержимого файла
#     with open('Formula_San_Zeora.txt', 'r', encoding='utf-8') as file:
#         text_about_calories = file.read()
#
#     # Отправка содержимого файла пользователю
#     await call.message.answer(text_about_calories)
#     await call.answer()
#
# @dp.callback_query_handler(text='calories')
# async def set_gender(call):
#     await call.message.answer("Выберите Ваш пол: \n1. Мужчина\n2. Женщина")
#     await UserState.gender.set()
#
# @dp.message_handler(state=UserState.gender)
# async def set_age(message: types.Message, state: FSMContext):
#     gender = message.text.strip()
#     if gender not in ["1", "2"]:
#         await message.answer("Пожалуйста, выберите 1 для Мужчины или 2 для Женщины.")
#         return
#     await state.update_data(gender=gender)
#     await message.answer("Введите свой возраст (от 13 до 80 лет): ")
#     await UserState.age.set()
#
#
# @dp.message_handler(state=UserState.age)
# async def set_growth(message: types.Message, state: FSMContext):
#     age = message.text.strip()
#     if not age.isdigit() or not (13 <= int(age) <= 80):
#         await message.answer("Пожалуйста, введите корректный возраст от 13 до 80 лет.")
#         return
#     await state.update_data(age=age)
#     await message.answer("Введите свой рост (в см): ")
#     await UserState.growth.set()
#
#
# @dp.message_handler(state=UserState.growth)
# async def set_weight(message: types.Message, state: FSMContext):
#     await state.update_data(growth=message.text)
#     await message.answer("Введите свой вес (в кг): ")
#     await UserState.weight.set()
#
#
# @dp.message_handler(state=UserState.weight)
# async def set_activity_level(message: types.Message, state: FSMContext):
#     await state.update_data(weight=message.text)
#     await message.answer(
#         "Выберите уровень активности:\n1. Минимальная активность (1.2)\n2. Слабый уровень активности (1.375)\n3. Умеренный уровень активности (1.55)\n4. Тяжелая активность (1.7)\n5. Экстремальный уровень (1.9)")
#     await UserState.activity_level.set()
#
# @dp.message_handler(state=UserState.activity_level)
# async def send_calories(message: types.Message, state: FSMContext):
#     activity_level = message.text.strip()
#     if activity_level not in ["1", "2", "3", "4", "5"]:
#         await message.answer("Пожалуйста, выберите уровень активности от 1 до 5.")
#         return
#
#     await state.update_data(activity_level=activity_level)
#     data = await state.get_data()
#
#     age = int(data['age'])
#     growth = float(data['growth'])
#     weight = float(data['weight'])
#     gender = data['gender']
#
#     # Определяем коэффициент активности
#     activity_coefficients = {
#         "1": 1.2,
#         "2": 1.375,
#         "3": 1.55,
#         "4": 1.7,
#         "5": 1.9
#     }
#     A = activity_coefficients[activity_level]
#
#     # Расчет калорий по формуле Миффлина-Сан Жеора
#     if gender == "1":  # Мужчина
#         calories = (10 * weight + 6.25 * growth - 5 * age + 5) * A
#     else:  # Женщина
#         calories = (10 * weight + 6.25 * growth - 5 * age - 161) * A
#
#     await message.answer(f"Ваш приблизительный суточный расход калорий: {calories:.2f} ккал")
#
#     # Удаляем данные о пользователе после расчета
#     await state.finish()  # Завершаем состояние
# #____________________________________________________________________________________________________________________
# # 3a)________________________________________________________________________________________________________________
#
# @dp.callback_query_handler(text='weight_is_calculated')
# async def get_weight_calc(call: types.CallbackQuery):
#     print("Обработчик weight_is_calculated вызван")                            # Логирование
#     # Чтение содержимого файла
#     with open('Weight_calculation.txt', 'r', encoding='utf-8') as file:
#         text_weight_calculation = file.read()
#
#         # Функция для разбивки текста на части для телеграма
#         def split_text(text, max_length=4095):
#             return [text[i:i + max_length] for i in range(0, len(text), max_length)]
#
#         # Разделение текста на части
#         text_parts = split_text(text_weight_calculation)
#
#         # Отправка каждой части текста
#         for part in text_parts:
#             await call.message.answer(part)
#
#         await call.answer()
#
# @dp.callback_query_handler(lambda callback_query: callback_query.data == 'weight_in_kg')
# async def calculate_weight_handler(callback_query: types.CallbackQuery):
#     await callback_query.answer()  # Подтверждение нажатия кнопки
#     await callback_query.message.answer("Введите рост в см:")
#     await Form.height.set()  # Установка состояния
#
# @dp.message_handler(state=Form.height)
# async def process_height(message: types.Message, state: FSMContext):
#     height_cm = float(message.text)
#     await state.update_data(height=height_cm)  # Сохранение роста в состоянии
#     await Form.next()  # Переход к следующему состоянию
#     await message.answer("Введите вес в кг:")
#
# @dp.message_handler(state=Form.weight)
# async def process_weight(message: types.Message, state: FSMContext):
#     weight_kg = float(message.text)
#     await state.update_data(weight=weight_kg)  # Сохранение веса в состоянии
#     await Form.next()  # Переход к следующему состоянию
#     await message.answer("Введите пол (1 - мужчина, 2 - женщина):")
#
# @dp.message_handler(state=Form.gender)
# async def process_gender(message: types.Message, state: FSMContext):
#     gender_input = int(message.text)
#     if gender_input == 1:
#         gender = 'male'
#     elif gender_input == 2:
#         gender = 'female'
#     else:
#         await message.answer("Неверный ввод. Пожалуйста, введите 1 для мужчины или 2 для женщины.")
#         return
#
#     await state.update_data(gender=gender)  # Сохранение пола в состоянии
#     await Form.next()  # Переход к следующему состоянию
#     await message.answer("Введите возраст:")
#
#
# # @dp.message_handler(state=Form.gender)
# # async def process_gender(message: types.Message, state: FSMContext):
# #     gender = message.text
# #     await state.update_data(gender=gender)  # Сохранение пола в состоянии
# #     await Form.next()  # Переход к следующему состоянию
# #     await message.answer("Введите возраст:")
#
# @dp.message_handler(state=Form.age)
# async def process_age(message: types.Message, state: FSMContext):
#     age = int(message.text)
#     await state.update_data(age=age)  # Сохранение возраста в состоянии
#     await Form.next()  # Переход к следующему состоянию
#
#     # Отправка изображения и выбор типа телосложения
#     await message.answer_photo(photo=open('type_of_physique.png', 'rb'),
#                     caption="Введите тип телосложения:\n1 - Астенический\n2 - Нормостенический\n3 - Гиперстенический:")
#
#
#
# # @dp.message_handler(state=Form.age)
# # async def process_age(message: types.Message, state: FSMContext):
# #     age = int(message.text)
# #     await state.update_data(age=age)  # Сохранение возраста в состоянии
# #     await Form.next()  # Переход к следующему состоянию
# #     await message.answer("Введите тип телосложения (астенический/нормостенический/гиперстенический):")
#
# @dp.message_handler(state=Form.body_type)
# async def process_body_type(message: types.Message, state: FSMContext):
#     body_type_input = int(message.text)
#     body_type = ""
#
#     if body_type_input == 1:
#         body_type = 'asthenic'
#     elif body_type_input == 2:
#         body_type = 'normostenic'
#     elif body_type_input == 3:
#         body_type = 'hypersthenic'
#     else:
#         await message.answer("Неверный ввод. Пожалуйста, введите 1, 2 или 3.")
#         return
#
#     await state.update_data(body_type=body_type)  # Сохранение типа телосложения в состоянии
#
#     # Получение всех данных из состояния
#     data = await state.get_data()
#     height_cm = data['height']
#     weight_kg = data['weight']
#     gender = data['gender']
#     age = data['age']
#     body_type = data['body_type']
#
#     def calculate_weight(height_cm, gender, age, body_type):
#         # Расчет нормального веса по формуле Брока
#         if gender.lower() == 'male':
#             normal_weight = height_cm - 110
#         else:
#             normal_weight = height_cm - 100
#
#         # Корректировка по возрасту
#         if 20 <= age <= 30:
#             normal_weight *= 0.89  # Уменьшение на 11%
#         elif age > 50:
#             normal_weight *= 1.06  # Увеличение на 6%
#
#         # Корректировка по типу телосложения
#         if body_type.lower() == 'asthenic':
#             normal_weight *= 0.90  # Уменьшение на 10%
#         elif body_type.lower() == 'hypersthenic':
#             normal_weight *= 1.10  # Увеличение на 10%
#
#         return normal_weight
#
#     def calculate_bmi(weight_kg, height_m):
#         bmi = weight_kg / (height_m ** 2)
#         return bmi
#
#     def classify_obesity(bmi):
#         if bmi < 15:
#             return "Острый недостаток веса"
#         elif 15 <= bmi < 20:
#             return "Недостаточная масса тела"
#         elif 20 <= bmi < 25:
#             return "Нормальный вес"
#         elif 25 <= bmi < 30:
#             return "Избыточная масса тела"
#         elif 30 <= bmi < 35:
#             return "Ожирение 1 степени"
#         elif 35 <= bmi < 40:
#             return "Ожирение 2 степени"
#         else:
#             return "Ожирение 3 степени"
#     # Выполнение расчетов
#     normal_weight = calculate_weight(height_cm, gender, age, body_type)
#     height_m = height_cm / 100
#     bmi = calculate_bmi(weight_kg, height_m)
#     obesity_classification = classify_obesity(bmi)
#
#     excess_weight = weight_kg - normal_weight if weight_kg > normal_weight else 0
#
#     await message.answer(f"Нормальный вес: {normal_weight:.2f} кг")
#     await message.answer(f"Индекс массы тела (ИМТ): {bmi:.2f}")
#     await message.answer(f"Классификация ожирения: {obesity_classification}")
#     await message.answer(f"Избыточный вес до нормы: {excess_weight:.2f} кг")
#
#     await state.finish()  # Завершение состояния
#
# #____________________________________________________________________________________________________________________
#
# # Обработка выбора категории рецептов
# @dp.message_handler(lambda message: message.text in ["Завтраки", "Ужины", "Десерты", "Вегетарианские"])  # Обработчик для категорий рецептов
# async def send_recipes(message: types.Message):                             # Асинхронная функция для отправки рецептов
#     await message.answer(f"Вот несколько рецептов для {message.text}!",
#                          )                 # Ответ с предложением рецептов и кнопкой "Назад в меню"
#
#
# # 1)_________________________________________________________________________________________________________________
#
# # # Обработка других кнопок
# # @dp.message_handler(lambda message: message.text == "Фото канала")              # Обработчик для кнопки "Пейзажи"
# # async def landscapes_menu(message: types.Message):                          # Асинхронная функция для обработки выбора
# #     await message.answer("Вот красивые фотографии пейзажей!",
# #                          )                                       # Ответ с фотографиями пейзажей и кнопкой "Назад в меню"
#
#
# @dp.message_handler(lambda message: message.text == "Фото канала")  # Обработчик для кнопки "Фото канала"
# async def landscapes_menu(message: types.Message):  # Асинхронная функция для обработки выбора
#     await message.answer("Перейдите по ссылке на папку с фотографиями:",
#                          reply_markup=types.InlineKeyboardMarkup().add(
#                              types.InlineKeyboardButton("Перейти к фото",
#                              url="https://photos.google.com/share/AF1QipOzji_5ZJd4GLg28voPaFGOmj_kQNnC0ShYsTVXgZX0_4leVTeX15hpLFfdOn40xg?key=cjFFUmpRcWdVQnVKdDlaYWkwaU5rYnhIVzMzTDRB")  # Ссылка на папку
#                          ))                                                                       # Добавление кнопки с ссылкой
#
# #______________________________________________________________________________________________________________________
#
#
# @dp.message_handler(lambda message: message.text == "Животные")             # Обработчик для кнопки "Животные"
# async def animals_menu(message: types.Message):                             # Асинхронная функция для обработки выбора
#     await message.answer("Вот милые фотографии животных!",
#                          )                 # Ответ с фотографиями животных и кнопкой "Назад в меню"
#
# @dp.message_handler(lambda message: message.text == "Дополнительные функции")  # Обработчик для кнопки "Дополнительные функции"
# async def additional_features_menu(message: types.Message):                 # Асинхронная функция для обработки выбора
#     await message.answer("Выберите опцию:",
#                          reply_markup=additional_features_keyboard())       # Запрос выбора дополнительных функций
#
# @dp.message_handler(lambda message: message.text == "Обратная связь")       # Обработчик для кнопки "Обратная связь"
# async def feedback_menu(message: types.Message):                            # Асинхронная функция для обработки выбора
#     await message.answer("Отправьте свой отзыв:",
#                          )                 # Ответ с запросом отзыва и кнопкой "Назад в меню"
#
# def additional_features_keyboard():                                              # Функция для создания клавиатуры дополнительных функций
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)                   # Создание клавиатуры
#     keyboard.add("Обратная связь", "Подписка на новости", "Назад в меню")  # Добавление кнопок
#     return keyboard  # Возврат клавиатуры
#
# @dp.message_handler(lambda message: message.text == "Подписка на новости")        # Обработчик для кнопки "Подписка на новости"
# async def subscription_menu(message: types.Message):                              # Асинхронная функция для обработки выбора
#     await message.answer("Вы подписаны на новости!",
#                          )                       # Ответ с подтверждением подписки и кнопкой "Назад в меню"
#
# # 2) ___________________________________________________________________________________________________________________
#
# @dp.message_handler(lambda message: message.text == "Ссылки и ресурсы")           # Обработчик для кнопки "Ссылки и ресурсы"
# async def links_resources_menu(message: types.Message):                           # Асинхронная функция для обработки выбора
#     print("Обработчик 'Ссылки и ресурсы' вызван")                                 # Логирование
#     keyboard = InlineKeyboardMarkup()  # Создание инлайн-клавиатуры
#     keyboard.add(InlineKeyboardButton("Перейти на YouTube канал 'Все обо Всем'",
#                                        url="https://youtube.com/@elena_ivanovaaa?si=jye0JlS9ozmRTrqF"))  # Кнопка с ссылкой
#     keyboard.add(InlineKeyboardButton("Перейти на Дзен канал 'Pantera Volna'",
#                                        url="https://dzen.ru/id/64de5ea842a0d1556b524b48"))  # Кнопка с ссылкой
#     await message.answer("Вот ссылки на мои каналы!", reply_markup=keyboard)  # Ответ с клавиатурой
#
# # @dp.message_handler(lambda message: message.text == "Ссылки и ресурсы")           # Обработчик для кнопки "Ссылки и ресурсы"
# # async def links_resources_menu(message: types.Message):                           # Асинхронная функция для обработки выбора
# #     await message.answer("Вот ссылки на наши социальные сети и блог!",
# #                          )                       # Ответ с ссылками и кнопкой "Назад в меню"
#
# #______________________________________________________________________________________________________________________
#
#
# @dp.message_handler(lambda message: message.text == "Беседка")                    # Обработчик для кнопки "Беседка"
# async def gazebo_menu(message: types.Message):                                    # Асинхронная функция для обработки выбора
#     print("Обработчик 'Беседка' вызван")                                          # Логирование
#     await message.answer("Добро пожаловать в беседку! Здесь Вы можете задавать вопросы и участвовать в опросах.",
#                          )  # Ответ с информацией о беседке и кнопкой "Назад в меню"
#
#
#
# # # Запуск бота
# # if __name__ == '__main__':  # Проверка, что скрипт запускается напрямую
# #     start_time = datetime.now()                                                                         # Получение текущего времени
# #     print(f"Запуск бота в {start_time.strftime('%H:%M:%S')} дата {start_time.strftime('%d.%m.%Y')}г.")  # Логирование с датой и временем
# #     try:
# #         executor.start_polling(dp, skip_updates=True)                                                   # Запуск бота и обработка обновлений
# #     except Exception as e:
# #         print(f"Произошла ошибка: {e}")                                                                 # Логирование ошибок
# #     finally:
# #         end_time = datetime.now()                                                                       # Получение времени завершения
# #         print(f"Бот завершил работу в {end_time.strftime('%H:%M:%S')} дата {end_time.strftime('%d.%m.%Y')}г.")  # Логирование завершения работы бота
# #
# #     executor.start_polling(dp, skip_updates=True)                                                       # Запуск бота и обработка обновлений
#
# is_running = False
#
# if __name__ == '__main__':                             # Проверка, что скрипт запускается напрямую, а не импортируется как модуль
#     start_time = datetime.now()                                     # Получение текущего времени для логирования
#                                                        # Вывод в консоль времени запуска бота с форматированием
#     print(f"Запуск бота в {start_time.strftime('%H:%M:%S')} дата {start_time.strftime('%d.%m.%Y')} г.")
#
#     if not is_running:                                 # Проверка, запущен ли бот (флаг is_running должен быть False)
#         is_running = True                              # Установка флага, что бот запущен, чтобы предотвратить повторный запуск
#         try:
#                                                        # Запуск бота с использованием метода start_polling, который начинает опрос обновлений
#             executor.start_polling(dp, skip_updates=True)
#         except Exception as e:                         # Обработка любых исключений, которые могут возникнуть во время работы бота
#                                                                     # Логирование ошибки в консоль, если что-то пошло не так
#             print(f"Произошла ошибка: {e}")
#         finally:
#             end_time = datetime.now()                  # Получение времени завершения работы бота
#             # Вывод в консоль времени завершения работы бота с форматированием
#             print(f"Бот завершил работу в {end_time.strftime('%H:%M:%S')} дата {end_time.strftime('%d.%m.%Y')} г.")
#             is_running = False                         # Сброс флага is_running при завершении работы бота
#     else:
#         # Если бот уже запущен, выводим сообщение о том, что нужно завершить предыдущий экземпляр
#         print("Бот уже запущен. Завершите предыдущий экземпляр перед запуском нового.")