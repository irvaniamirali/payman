import asyncio
import logging
import sys
from typing import Final

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from payman import Payman
from payman.gateways.zibal.errors import ZibalError

# --- Configuration ---
TELEGRAM_BOT_TOKEN: Final[str] = "..."

# --- Payment Gateway Setup ---
AMOUNT = 10_000
CALLBACK_URL = "http://example.com/callback"

pay = Payman("zibal", merchant_id="zibal")  # sandbox mode
track_ids: dict[int, int] = {}

# --- Dispatcher ---
dp = Dispatcher()


@dp.message(Command("pay"))
async def start_payment(message: Message) -> None:
    response = await pay.payment(
        amount=AMOUNT,
        callback_url=CALLBACK_URL,
        description="Test Payment",
    )

    if response.success:
        user_id = message.from_user.id
        track_ids[user_id] = response.track_id
        url = pay.get_payment_redirect_url(response.track_id)
        await message.reply(f"Please pay here:\n{url}")
    else:
        await message.reply(f"Payment request failed: {response.message}")


@dp.message(Command("verify"))
async def verify_payment(message: Message) -> None:
    user_id = message.from_user.id
    track_id = track_ids.get(user_id)

    if not track_id:
        await message.reply("No payment to verify.")
        return

    try:
        response = await pay.verify(track_id=track_id)
        if not response.success:
            await message.reply(f"Payment was not completed.\n{e}")
            return
    except ZibalError as e:
        await message.reply(f"Unknown Zibal error.\n{e}")
        return

    await message.reply(f"Payment successful!\nRef ID: {response.ref_number}")
    track_ids.pop(user_id, None)


async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="[%(asctime)s] %(levelname)s: %(message)s")
    asyncio.run(main())
