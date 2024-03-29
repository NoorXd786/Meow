from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, MessageEntityMentionName

from . import *


async def get_full_user(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await eor(event, "Need a user to do this...")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await eor(event, f"**ERROR !!**\n\n`{str(err)}`")
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


@bot.on(mew_cmd(pattern="gpromote ?(.*)"))
@bot.on(sudo_cmd(pattern="gpromote ?(.*)", allow_sudo=True))
async def _(Meowevent):
    i = 0
    await Meowevent.get_sender()
    me = await Meowevent.client.get_me()
    Meow = await eor(Meowevent, "`Promoting globally...`")
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    f"@{me.username}" if me.username else my_mention
    await Meowevent.get_chat()
    if Meowevent.is_private:
        user = Meowevent.chat
        rank = Meowevent.pattern_match.group(1)
    else:
        Meowevent.chat.title
    try:
        user, rank = await get_full_user(Meowevent)
    except:
        pass
    if me == user:
        await Meow.edit("You can't promote yourself...")
        return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await Meow.edit("**ERROR !!**")
    if user:
        telchanel = [
            d.entity.id
            for d in await Meowevent.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        rgt = ChatAdminRights(
            add_admins=False,
            invite_users=True,
            change_info=False,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
        )
        for x in telchanel:
            try:
                await Meowevent.client(EditAdminRequest(x, user, rgt, rank))
                i += 1
                await Meow.edit(f"**Promoting User in :**  `{i}` Chats...")
            except:
                pass
    else:
        await Meow.edit("**Reply to a user !!**")
    await Meow.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Promoted Globally In** `{i}` **Chats !!**"
    )
    await bot.send_message(
        Config.LOGGER_ID,
        f"#GPROMOTE \n\n**Globally Promoted User :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`",
    )


@bot.on(mew_cmd(pattern="gdemote ?(.*)"))
@bot.on(sudo_cmd(pattern="gdemote ?(.*)", allow_sudo=True))
async def _(Meowevent):
    i = 0
    await Meowevent.get_sender()
    me = await Meowevent.client.get_me()
    Meow = await eor(Meowevent, "`Demoting Globally...`")
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    f"@{me.username}" if me.username else my_mention
    await Meowevent.get_chat()
    if Meowevent.is_private:
        user = Meowevent.chat
        rank = Meowevent.pattern_match.group(1)
    else:
        Meowevent.chat.title
    try:
        user, rank = await get_full_user(Meowevent)
    except:
        pass
    if me == user:
        await Meow.edit("You can't Demote yourself !!")
        return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await Meow.edit("**ERROR !!**")
    if user:
        telchanel = [
            d.entity.id
            for d in await Meowevent.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        rgt = ChatAdminRights(
            add_admins=None,
            invite_users=None,
            change_info=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None,
        )
        for x in telchanel:
            try:
                await Meowevent.client(EditAdminRequest(x, user, rgt, rank))
                i += 1
                await Meow.edit(f"**Demoting Globally In Chats :** `{i}`")
            except:
                pass
    else:
        await Meow.edit("**Reply to a user !!**")
    await Meow.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Demoted Globally In** `{i}` **Chats !!**"
    )
    await bot.send_message(
        Config.LOGGER_ID,
        f"#GDEMOTE \n\n**Globally Demoted :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`",
    )
