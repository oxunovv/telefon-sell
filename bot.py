import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from config import BOT_TOKEN,ADMINS,MY_CHANNEL
from keyboard_buttons import menu_button
from aiogram.fsm.context import FSMContext
from mystate import Elon
from inline_buttons import elon_btn

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    full_name = message.from_user.full_name
    await message.answer(f"Salom, {full_name}",reply_markup=menu_button)

@dp.message(F.text == "📢 Elon berish")
async def elon_post(message: types.Message,state: FSMContext):
    await message.answer("Telefon modeli va nomini kiring...")
    await state.set_state(Elon.phone_model)

@dp.message(F.text,Elon.phone_model)
async def elon_model(message: types.Message,state: FSMContext):
    ph_model = message.text
    await state.update_data(phone_model = ph_model)
    await message.answer("Rasmini yuboring...")
    await state.set_state(Elon.image)

@dp.message(F.photo,Elon.image)
async def elon_image(message: types.Message,state: FSMContext):
    img = message.photo[-1].file_id

    await state.update_data(image = img)
    await message.answer("Telefon holatini kiriting...")
    await state.set_state(Elon.holati)

@dp.message(F.text,Elon.holati)
async def elon_holati(message: types.Message,state: FSMContext):
    holati = message.text
    await state.update_data(holati = holati)
    await message.answer("Telefoni hotirasini kiriting...")
    await state.set_state(Elon.hotira)

@dp.message(F.text,Elon.hotira)
async def elon_hotira(message: types.Message,state: FSMContext):
    hotira= message.text
    await state.update_data(hotira = hotira)
    await message.answer("Telefoni batareykasini kiriting(Iphone bolsa)...")
    await state.set_state(Elon.kridit)

@dp.message(F.text,Elon.kridit)
async def elon_kiridit(message: types.Message,state: FSMContext):
    kridit = message.text
    await state.update_data(kridit = kridit)
    await message.answer("Telefoni rangini kiriting...")
    await state.set_state(Elon.rangi)

@dp.message(F.text,Elon.rangi)
async def elon_rangi(message: types.Message,state: FSMContext):
    rangi = message.text
    await state.update_data(rangi = rangi)
    await message.answer("Dokumenti bormi📦...")
    await state.set_state(Elon.mudatli)

@dp.message(F.text,Elon.mudatli)
async def elon_mudatli(message: types.Message,state: FSMContext):
    mudatli = message.text
    await state.update_data(mudatli = mudatli)
    await message.answer("Telefon narxini kiriting...")
    await state.set_state(Elon.price)

@dp.message(F.text,Elon.price)
async def elon_price(message: types.Message,state: FSMContext):
    price = message.text
    await state.update_data(price = price)
    await message.answer("Telefon malumotizni qoldiring..")
    await state.set_state(Elon.phone_number)

@dp.message(F.text,Elon.phone_number)
async def elon_phone_number(message: types.Message,state: FSMContext):
    data = await state.get_data()
    phone_model = data.get("phone_model")
    image = data.get("image")
    holati = data.get("holati")
    hotira = data.get("hotira")
    kridit = data.get("kridit")
    rangi = data.get("rangi")
    mudatli = data.get("mudatli")
    price = data.get("price")
    phone_number = message.text
    text = f"Model📱: {phone_model}\nHolati⚙️: {holati}\nHotira📁: {hotira}GB\n🔋Batareyka: {kridit}%\nRangi: {rangi}\n📦Dokumenti bormi: {mudatli}\nNarxi: {price}\nMurojaat uchun tel: {phone_number}"
    await message.answer("Sizning Eloningiz Adminga yuborildi!!!",reply_markup=menu_button)
    await bot.send_photo(chat_id=ADMINS[0],photo=image,caption=text,reply_markup=elon_btn)
    await state.clear()


@dp.callback_query(F.data == "1")
async def elon_ber(callback: types.CallbackQuery):
    photo = callback.message.photo[-1].file_id
    text = callback.message.caption
    await bot.send_photo(chat_id=MY_CHANNEL,photo=photo,caption=text)
    await callback.answer("Kanalga joylandi 🔥")
    await callback.message.delete()


@dp.callback_query(F.data == "0")
async def elon_ber(callback: types.CallbackQuery):
    await callback.answer("Elon o'chirildi 🔥")
    await callback.message.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
