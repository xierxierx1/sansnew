from nonebot import on_command, require

require("nonebot_plugin_orm")  # noqa
from nonebot.adapters import Event, Message
from nonebot.params import CommandArg

import asyncio

from .config import Config, config
from .data_source import (
    choice,
    can_fishing,
    get_stats,
    save_fish,
    get_backpack,
    sell_fish,
    get_balance
)

fishing = on_command("fishing", aliases={"钓鱼1"}, priority=5)
stats = on_command("stats", aliases={"统计信息1"}, priority=5)
backpack = on_command("backpack", aliases={"背包1"}, priority=5)
sell = on_command("sell", aliases={"卖鱼1"}, priority=5)
balance = on_command("balance", aliases={"积分1"}, priority=5)
day=on_command("day",aliases={"签到1"},priority=5)

@day.handle()
async def _(event:Event):
    user_id=event.get_user_id()
    


@fishing.handle()
async def _(event: Event):
    user_id = event.get_user_id()
    if not await can_fishing(user_id):
        await fishing.finish("河累了, 休息一下吧")
    await fishing.send("正在钓鱼…")
    choice_result = choice()
    fish = choice_result[0]
    sleep_time = choice_result[1]
    result = f"钓到了一条{fish}, 你把它收进了背包里"
    await save_fish(user_id, fish)
    await asyncio.sleep(sleep_time)
    await fishing.finish(result)


@stats.handle()
async def _(event: Event):
    user_id = event.get_user_id()
    await stats.finish(await get_stats(user_id))


@backpack.handle()
async def _(event: Event):
    user_id = event.get_user_id()
    await backpack.finish(await get_backpack(user_id))


@sell.handle()
async def _(event: Event, arg: Message = CommandArg()):
    fish_name = arg.extract_plain_text()
    if fish_name == "":
        await sell.finish("请输入要卖出的物品的名字, 如 出售 小鱼")
    user_id = event.get_user_id()
    await sell.finish(await sell_fish(user_id, fish_name))


@balance.handle()
async def _(event: Event):
    user_id = event.get_user_id()
    await balance.finish(await get_balance(user_id))
