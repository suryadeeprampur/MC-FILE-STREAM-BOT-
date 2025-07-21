# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import datetime, time
from pyrogram import Client, filters
from database.users_chats_db import db
from info import ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def pm_broadcast(bot, message):
    b_msg = await bot.ask(chat_id=message.from_user.id, text="Now Send Me Your Broadcast Message")

    try:
        users = await db.get_all_users()
        sts = await message.reply_text('Broadcasting your messages...')
        start_time = time.time()
        total_users = await db.total_users_count()

        done = 0
        blocked = 0
        deleted = 0
        failed = 0
        success = 0

        for user in users:
            user_id = int(user.get("id", 0))
            if not user_id:
                failed += 1
                done += 1
                continue

            try:
                await bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=b_msg.chat.id,
                    message_id=b_msg.id,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")]]
                    )
                )
                success += 1
            except Exception as e:
                error_str = str(e).lower()
                if "blocked" in error_str:
                    blocked += 1
                elif "chat not found" in error_str:
                    deleted += 1
                else:
                    failed += 1
            done += 1

            if done % 20 == 0:
                await sts.edit(
                    f"Broadcast in progress:\n\n"
                    f"Total Users: {total_users}\n"
                    f"Completed: {done} / {total_users}\n"
                    f"✅ Success: {success}\n"
                    f"⛔ Blocked: {blocked}\n"
                    f"🗑️ Deleted: {deleted}\n"
                    f"⚠️ Failed: {failed}"
                )

        time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
        await sts.edit(
            f"✅ Broadcast Completed:\n\n"
            f"⏱️ Time Taken: {time_taken} seconds\n"
            f"Total Users: {total_users}\n"
            f"Completed: {done} / {total_users}\n"
            f"✅ Success: {success}\n"
            f"⛔ Blocked: {blocked}\n"
            f"🗑️ Deleted: {deleted}\n"
            f"⚠️ Failed: {failed}"
        )

    except Exception as e:
        print(f"error: {e}")


@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS))
async def broadcast_group(bot, message):
    b_msg = await bot.ask(chat_id=message.from_user.id, text="Now Send Me Your Broadcast Message")
    groups = await db.get_all_chats()
    sts = await message.reply_text("Broadcasting your messages To Groups...")

    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = 0
    failed = 0
    success = 0

    for group in groups:
        group_id = int(group.get("id", 0))
        if not group_id:
            failed += 1
            done += 1
            continue

        try:
            await bot.copy_message(
                chat_id=group_id,
                from_chat_id=b_msg.chat.id,
                message_id=b_msg.id,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")]]
                )
            )
            success += 1
        except Exception:
            failed += 1
        done += 1

        if done % 20 == 0:
            await sts.edit(
                f"Broadcast in progress:\n\n"
                f"Total Groups: {total_groups}\n"
                f"Completed: {done} / {total_groups}\n"
                f"✅ Success: {success}\n"
                f"⚠️ Failed: {failed}"
            )

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(
        f"✅ Broadcast Completed:\n\n"
        f"⏱️ Time Taken: {time_taken} seconds\n"
        f"Total Groups: {total_groups}\n"
        f"Completed: {done} / {total_groups}\n"
        f"✅ Success: {success}\n"
        f"⚠️ Failed: {failed}"
            )
