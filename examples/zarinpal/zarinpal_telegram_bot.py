import asyncio
import logging
import sys
import uuid
from typing import Final

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from payman import ZarinPal
from payman.gateways.zarinpal import PaymentRequest, VerifyRequest
from payman.gateways.zarinpal.errors import (
    SessionError,
    ZarinPalError,
)

# --- Configuration ---
TELEGRAM_BOT_TOKEN: Final[str] = "..."

# --- Payment Gateway Setup ---
pay = ZarinPal(merchant_id=str(uuid.uuid4()), sandbox=True)
authorities: dict[int, str] = {}

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

    if response.success:
        user_id = message.from_user.id
        authorities[user_id] = response.authority
        url = pay.get_payment_redirect_url(response.authority)
        await message.reply(f"Please pay here:\n{url}")
    else:
        await message.reply(f"Payment request failed: {response.message}")


@dp.message(Command("verify"))
async def verify_payment(message: Message) -> None:
    user_id = message.from_user.id
    authority = authorities.get(user_id)

    if not authority:
        await message.reply("No payment to verify.")
        return

    request = VerifyRequest(authority=authority, amount=10_000)

    try:
        response = await pay.verify(request)
        if not response.success:
            await message.reply(f"Payment was not completed.\n{e}")
            return
    except SessionError as e:
        await message.reply(f"Session error occurred.\n{e}")
        return
    except ZarinPalError as e:
        await message.reply(f"Unknown payment error.\n{e}")
        return

    await message.reply(f"Payment successful!\nRef ID: {response.ref_id}")
    authorities.pop(user_id, None)


async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="[%(asctime)s] %(levelname)s: %(message)s")
    asyncio.run(main())
