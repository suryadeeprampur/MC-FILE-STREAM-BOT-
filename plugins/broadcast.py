from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from bot import bot
from database.users_chats_db import db
from info import ADMINS
import asyncio

@bot.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def pm_broadcast(_, message: Message):
    await message.reply_chat_action(ChatAction.TYPING)
    users = await db.get_all_users()
    done = 0
    failed = 0
    success = 0

    # Ask admin for the message to broadcast
    try:
        b_msg = await bot.ask(
            chat_id=message.from_user.id,
            text="📢 Send me the message you want to broadcast.",
            filters=filters.text | filters.media,
            timeout=300
        )
    except Exception as e:
        await message.reply(f"❌ Error:\n{e}")
        return

    await message.reply("✅ Broadcasting started...")

    # 🔘 Define inline button
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")]
    ])

    for user in users:
        user_id = int(user["id"])
        try:
            if b_msg.text:
                await bot.send_message(
                    chat_id=user_id,
                    text=b_msg.text.markdown,
                    disable_web_page_preview=True,
                    reply_markup=button
                )
            elif b_msg.photo:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=b_msg.photo.file_id,
                    caption=b_msg.caption.markdown if b_msg.caption else None,
                    reply_markup=button
                )
            elif b_msg.video:
                await bot.send_video(
                    chat_id=user_id,
                    video=b_msg.video.file_id,
                    caption=b_msg.caption.markdown if b_msg.caption else None,
                    reply_markup=button
                )
            elif b_msg.document:
                await bot.send_document(
                    chat_id=user_id,
                    document=b_msg.document.file_id,
                    caption=b_msg.caption.markdown if b_msg.caption else None,
                    reply_markup=button
                )
            else:
                failed += 1
                continue

            success += 1

        except Exception:
            failed += 1

        done += 1
        if done % 20 == 0:
            await asyncio.sleep(1)

    await message.reply_text(
        f"✅ Broadcast complete!\n\n"
        f"👤 Total: {len(users)}\n"
        f"📬 Success: {success}\n"
        f"❌ Failed: {failed}"
       )
