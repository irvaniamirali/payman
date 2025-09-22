import asyncio
import logging
import sys
from typing import Final

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from payman import Payman
from zibal.exceptions import ZibalGatewayError

# -----------------------------
# Configuration
# -----------------------------
TELEGRAM_BOT_TOKEN: Final[str] = "..."  # Replace with your bot token
AMOUNT: Final[int] = 10_000
CALLBACK_URL: Final[str] = "http://example.com/callback"

# -----------------------------
# Payment Gateway Setup
# -----------------------------
pay = Payman("zibal", merchant_id="zibal")  # Sandbox mode
user_track_ids: dict[int, int] = {}  # Maps Telegram user ID to Zibal track ID

# -----------------------------
# Dispatcher
# -----------------------------
dp = Dispatcher()


# -----------------------------
# Command Handlers
# -----------------------------
@dp.message(Command("pay"))
async def start_payment(message: Message) -> None:
    """
    Initiates a payment and sends the payment URL to the user.
    """
    user_id = message.from_user.id
    try:
        response = await pay.initiate_payment(
            amount=AMOUNT,
            callback_url=CALLBACK_URL,
            description="Test Payment",
        )
    except ZibalGatewayError as e:
        logging.error(f"Payment request failed for user {user_id}: {e}")
        await message.reply("Failed to initiate payment. Please try again later.")
        return

    if response.success:
        user_track_ids[user_id] = response.track_id
        payment_url = pay.get_payment_redirect_url(response.track_id)
        await message.reply(f"Payment initiated successfully! Please pay here:\n{payment_url}")
        logging.info(f"Payment started for user {user_id}, track_id: {response.track_id}")
    else:
        await message.reply(f"Payment request failed: {response.message}")
        logging.warning(f"Payment request failed for user {user_id}: {response.message}")


@dp.message(Command("verify"))
async def verify_payment(message: Message) -> None:
    """
    Verifies the payment for the user based on stored track_id.
    """
    user_id = message.from_user.id
    track_id = user_track_ids.get(user_id)

    if not track_id:
        await message.reply("You have no pending payment to verify.")
        return

    try:
        response = await pay.verify_payment(track_id=track_id)
    except ZibalGatewayError as e:
        logging.error(f"Verification error for user {user_id}, track_id {track_id}: {e}")
        await message.reply(f"Payment verification failed due to an error:\n{e}")
        return

    if response.success:
        await message.reply(f"Payment successful!\nRef ID: {response.ref_number}")
        logging.info(f"Payment verified for user {user_id}, track_id {track_id}")
        user_track_ids.pop(user_id, None)
    else:
        await message.reply(f"Payment was not completed.\nReason: {response.message}")
        logging.warning(f"Payment not completed for user {user_id}, track_id {track_id}")


# -----------------------------
# Main function
# -----------------------------
async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    logging.info("Starting Telegram bot...")
    await dp.start_polling(bot)


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="[%(asctime)s] %(levelname)s: %(message)s",
    )
    asyncio.run(main())
