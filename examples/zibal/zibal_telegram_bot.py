import asyncio
import logging
import sys
from typing import Final

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from payman import Zibal
from payman.gateways.zibal import PaymentRequest, VerifyRequest
from payman.gateways.zibal.errors import PaymentNotSuccessfulError

# --- Configuration ---
TELEGRAM_BOT_TOKEN: Final[str] = "..."

# --- Payment Gateway Setup ---
pay = Zibal(merchant_id="zibal")  # sandbox mode
track_ids: dict[int, int] = {}

# --- Dispatcher ---
dp = Dispatcher()


@dp.message(Command("pay"))
async def start_payment(message: Message) -> None:
    request = PaymentRequest(
        amount=10_000,
        description="Test Payment",
        callback_url="http://example.com/callback",
    )

    response = await pay.payment(request)

    if response.status == 100:
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

    request = VerifyRequest(track_id=track_id)

    try:
        response = await pay.verify(request)
    except PaymentNotSuccessfulError as e:
        await message.reply(f"Payment was not completed.\n{e}")
        return
    except Exception as e:
        await message.reply(f"Unknown payment error.\n{e}")
        return

    await message.reply(f"Payment successful!\nRef ID: {response.ref_number}")
    track_ids.pop(user_id, None)


async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="[%(asctime)s] %(levelname)s: %(message)s")
    asyncio.run(main())
