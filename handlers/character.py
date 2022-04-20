from contextlib import suppress

from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncio

from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from keyboards.possybility import Power
from loader import dp
from states.create_charachters import CreateCharacters
from states.power_lang import kb_client, kb_client1
from utils.api_db.initial_bd import check_id, create_characters, get_info_character, add_id


@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message):
    check = check_id(message.from_user.id)
    if check:
        pass
    else:
        add_id(message.from_user.id)
        await message.answer("Приветствую тебя 👋")
        await message.answer("Ты попал в великолепный мистический мир Алиум. Меня зовут Дорьен. Я помогу тебе на "
                             "начальных этапах разобраться в этом мире.")
        await message.answer("Сразу скажу что ты, я и такие как ты, мистическая раса Алиус. Мы отличаемся от земных "
                             "рас, таких как люди, гномы, эльфы и т.п. В нас заключена огромная сила и мы научились "
                             "ее использовать с помощью языка Python.")
        await asyncio.sleep(10)
        await message.answer("Я как твой наставник, помогу тебе научится использовать свою силу. Я обучу тебя чем "
                             "знаю, но в нашем мире, есть множество других наставников, которые так же помогут "
                             "использовать силу в углубленном смысле.")
        await message.answer("Я даю тебе возможность, использовать силу языка.")
        await message.answer("Использовав эту возможность ты сможешь взаимодействовать с миром используя прекрасный "
                             "язык Python.")
        await asyncio.sleep(10)
        await message.answer("И так, начнем с самого начала.")
        await message.answer("Я про тебя, особо нечего не знаю, но мне и другим как то надо к тебе обращаться. Назови "
                             "себя как хочешь.")
        await message.answer("Для того что бы весь мир видел что ты хочешь сообщить, требуется ввести следующую "
                             "инструкцию. ")
        await message.answer("<code>print([То что хотите вывести в мир])</code>", parse_mode='HTML')
        await asyncio.sleep(10)
        await message.answer("Конечно, к примеру я смогу вывести свое имя, использовав следующее: ")
        await message.answer('<code>print("Дорьен")</code>', parse_mode='HTML')
        await asyncio.sleep(10)
        await message.answer("Обязательно надо использовать кавычки, неважно двойные они или нет")
        await message.answer("В дальнейших уроках я те подробно объясню, зачем они нужны, а сейчас просто выведи мне "
                             "то как тебя зовут", reply_markup=kb_client)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(lambda message: message.text == "Сила языка")
async def used_power_language(message: types.Message):
    check = check_id(message.from_user.id)
    if check:
        await Power.activate.set()
        text = await message.answer("Вы активировали возможность [Сила языка]")
        asyncio.create_task(delete_message(text, 10))
    else:
        await message.answer("Пока не доступно данная возможно, попробуй вести /start")


@dp.message_handler(state=Power.activate)
async def input_code(message: types.Message, state: FSMContext):
    if message.text.startswith("print"):
        open_instr = message.text.split("print")[1]
        if open_instr.startswith("("):
            open_instr = open_instr.split("(")[1]
            if open_instr.endswith(")"):
                open_instr = open_instr.split(")")[0]
                if open_instr.startswith("'") and open_instr.endswith("'"):
                    result = open_instr.replace("'", "")
                    await Power.input_code.set()
                    async with state.proxy() as data:
                        data['result_code'] = open_instr
                    await input_login(message, state)
                elif open_instr.startswith('"') and open_instr.endswith('"'):
                    result = open_instr.replace('"', '')
                    await Power.input_code.set()
                    async with state.proxy() as data:
                        data['result_code'] = open_instr
                    await input_login(message, state)
                else:
                    await message.answer("Ошибка при сканировании строкового литерала.")
                    await Power.error.set()
                    await put_error(state=state, message=message)
            else:
                await message.answer("Мне кажется или ты забыл где то скобочку, она очень важна")
                await Power.error.set()
                await put_error(state=state, message=message)
        else:
            await message.answer("Мне кажется или ты забыл где то скобочку, она очень важна")
            await Power.error.set()
            await put_error(state=state, message=message)
    else:
        await message.answer("Ошибка при написании инструкции")
        await Power.error.set()
        await put_error(state=state, message=message)


@dp.message_handler(state=Power.input_code)
async def input_login(message: types.Message, state: FSMContext):
    check = check_id(message.from_user.id)
    if check:
        await message.answer("Ты уже создал персонажа для этого аккаунта, а больше событий еще нет.")
    else:
        result_code = await state.get_data()
        if result_code['result_code']:
            try:
                create_characters(id=message.from_user.id, login=result_code['result_code'].replace("'", ""))
                answer = "О, прекрасное имя {}, что ж теперь я знаю как к тебе обращаться, " \
                         "можем продолжить. ".format(result_code['result_code'].replace("'", ""))
                await state.finish()
                await message.answer(answer)
                await message.answer("Теперь ты уже как минимум понимаешь, как можно использовать силу языка Python.")
                await message.answer("Но это только начало, дальше будет интересно.")
                await asyncio.sleep(5)
                await message.answer("Ты только что создал своего персонажа, он привязан к тебе и поэтому я дам тебе "
                                    "возможность, просмотра информации о своем персонаже.", reply_markup=kb_client1)
                await message.answer("Можешь попробовать, увидишь что ты из себя представляешь.")
            except Exception as e:
                await state.finish()
                await message.answer("С таким логином персонаж уже существует")


@dp.message_handler(state=Power.error)
async def put_error(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Произошла ошибка, давай попробуем снова!")


@dp.message_handler(lambda message: message.text == "Информация о персонаже")
async def info_character(message: types.Message):
    try:
        info = get_info_character(message.from_user.id)
        info = info[0]
        rank_character = None
        type_weapon = None
        if info[3] == 0:
            rank_character = "Начинающий охотник"
        elif info[3] == 1:
            rank_character = "Охотник"
        elif info[3] == 2:
            rank_character = "Опытный охотник"
        elif info[3] == 3:
            rank_character = "Охотник со стажем"
        elif info[3] == 4:
            rank_character = "Легендарный охотник"
        if info[4] == "NON":
            type_weapon = "Без оружия"
        elif info[4] == "BLD":
            type_weapon = "Ближнее оружие"
        elif info[4] == "BOW":
            type_weapon = "Дальнее оружие"
        elif info[4] == "MGC":
            type_weapon = "Магическое оружие"
        result_info = f"Раса: 🧖Алиус\nИдентификатор: {info[1]}\nИмя: {info[2]}\n🏅Уровень: {info[15]}\n" \
                      f"♥Здоровье: {info[16]}\n🎖Ранг: {rank_character}\n⚜Класс: {type_weapon}\n🏆Рейтинг: {info[5]}\n" \
                      f"⚔Убийство монстров: {info[6]}\n🏵Благославление Алиума: {info[7]}\n" \
                      f"♦Завершенные квесты: {info[8]}\n📜Найденные свитки знаний: {info[9]}\n💠Кол-во ячеек способностей:" \
                    f" {info[10]}\n🎒Кол-во ячеек в инвентаре: {info[11]}\n\n🟡Золото: {info[12]}\n💎Алмазы: " \
                    f"{info[13]}\n🪙Алиаминаты: {info[14]}\n\n🗡Урон: {info[17]}\n🪄Магический урон: {info[18]}\n" \
                    f"🔆Сила Алиума: {info[19]}\n💪🏻Сила: {info[20]}\n🦵Ловкость: {info[21]}\n🫁Выносливость: {info[22]}\n" \
                    f"👀Интуиция: {info[23]}\n🍀Удача: {info[24]}\n🧠Интеллект: {info[25]}\n🛡Защита: {info[26]}\n" \
                    f"🔮Магическая защита: {info[27]}\n💢Шанс критического урона: {info[28]}\n🩸Критический урон: {info[29]}"
        await message.answer(result_info)
    except Exception:
        await message.answer("Пока не доступно данная возможно, попробуй вести /start")
