import time

from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User

from . import *


@bot.on(mew_cmd(pattern="stats$"))
@bot.on(sudo_cmd(pattern="stats$", allow_sudo=True))
async def stats(
    event: NewMessage.Event,
) -> None:  # pylint: disable = R0912, R0914, R0915
    if event.fwd_from:
        return
    Meow = await edit_or_reply(event, "`cσℓℓεcтιηg sтαтs...`")
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            # if participants_count > largest_group_member_count:
            #     largest_group_member_count = participants_count
            if entity.creator or entity.admin_rights:
                # if participants_count > largest_group_with_admin:
                #     largest_group_with_admin = participants_count
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"🌠**ѕtαtѕ fσr  {full_name}**🌠\n\n"
    response += f"☪️ **prívαtє chαtѕ:** {private_chats} \n"
    response += f"🔻   `υsεяs: {private_chats - bots}` \n"
    response += f"🔺   `вσтs: {bots}` \n"
    response += f"💟 **grσupѕ:** {groups} \n"
    response += f"💟 **chαnnєlѕ:** {broadcast_channels} \n"
    response += f"☪️  **αdmínѕ ín grσupѕ:** {admin_in_groups} \n"
    response += f"🔻   `cяεαтσя: {creator_in_groups}` \n"
    response += f"🔺   `α∂мιη яιgнтs: {admin_in_groups - creator_in_groups}` \n"
    response += f"💟  **αdmín ín chαnnєlѕ:** {admin_in_broadcast_channels} \n"
    response += f"🔻   `cяεαтεя: {creator_in_channels}` \n"
    response += (
        f"🔹   `αdmín ríghtѕ: {admin_in_broadcast_channels - creator_in_channels}` \n"
    )
    response += f"☪️ **υηяεα∂:** {unread} \n"
    response += f"☪️ **υηяεα∂ мεηтισηs:** {unread_mentions} \n\n"
    response += f"💟   __It Took:__ {stop_time:.02f}s \n"
    response += f"✨ **ρσωεяε∂ вү ** {mew_channel} 🌠"
    await Meow.edit(response)


def make_mention(user):
    return f"@{user.username}" if user.username else inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "Meow"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


CmdHelp("stats").add_command(
    "stats", None, "Shows you the count of your groups, channels, private chats, etc."
).add_info("Statistics Of Account").add_warning("✅ Harmless Module.").add()
