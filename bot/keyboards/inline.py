from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard_weather():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Погода сейчас", callback_data="weather_now")
    keyboard_builder.button(text="Погода на 5 дней", callback_data="weather_5_days")

    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def get_keyboard_main():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="погода", callback_data="weather")
    keyboard_builder.adjust()
    return keyboard_builder.as_markup()


def get_back_main_menu():
    keyboard_builder = InlineKeyboardBuilder()
    # keyboard_builder.button(text="Menu", commands='menu')
    keyboard_builder.button(text="Другой город", callback_data="weather")
    keyboard_builder.adjust()
    return keyboard_builder.as_markup()


def get_keyboard_weather_5_days():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="1", callback_data="0")
    keyboard_builder.button(text="2", callback_data="1")
    keyboard_builder.button(text="3", callback_data="2")
    keyboard_builder.button(text="4", callback_data="3")
    keyboard_builder.button(text="5", callback_data="4")
    keyboard_builder.button(text="Погода на 5 дней", callback_data="5")
    keyboard_builder.button(text="Другой город", callback_data="weather")
    keyboard_builder.adjust(3, 2, 1)
    return keyboard_builder.as_markup()
