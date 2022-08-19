from asyncio.log import logger
from venv import create
from telegram import ParseMode
from faker import Faker
import pyjokes
from art import text2art
from PIL import Image, ImageDraw, ImageFont

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import dotenv_values
from tempfile import NamedTemporaryFile

config = dotenv_values(".env")
fake = Faker()


def dady_jokes(update, context):
    update.message.reply_text(pyjokes.get_joke())


def message_handler(update, context):
    update.message.reply_text(
        "Welcome to the FunnyPythonBot. \nTake a look to the command menu! \nGood luck \U0001F49A"
    )


def create_image(path, content):
    print(content)
    image = Image.new("RGB", (300, 150), "black")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), content)
    path = path + ".png"
    image.save(path)
    return path


def do_art(update, context):
    with NamedTemporaryFile("r+b") as file:
        try:
            user_input = context.args[0]
            res = text2art(user_input, "rand")
            path = create_image(file.name, res)
            update.message.reply_photo(photo=open(path, "rb"))
        except:
            default_word = fake.word()
            res = text2art(default_word, "rand")
            path = create_image(file.name, res)
            update.message.reply_text(
                "Please use the following format: /art text.\nFor example /art {0} results into:".format(
                    default_word
                )
            )
            update.message.reply_photo(photo=open(path, "rb"))


def main():
    bot = Bot(config["TELEGRAM_API_TOKEN"])
    updater = Updater(bot=bot, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("dadyjokes", callback=dady_jokes))
    updater.dispatcher.add_handler(CommandHandler("art", callback=do_art))
    updater.dispatcher.add_handler(
        MessageHandler(filters=Filters.text, callback=message_handler)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
