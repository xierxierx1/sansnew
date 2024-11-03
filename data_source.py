import random
import time
import json

from sqlalchemy import select, update, delete
from sqlalchemy.sql.expression import func
from nonebot_plugin_orm import get_session

from .config import config
from .model import FishingRecord

fishing_coin_name = config.fishing_coin_name

    
def choice() -> tuple:
    config_fishes = config.fishes
    weights = [weight["weight"] for weight in config_fishes]
    choices = random.choices(
        config_fishes,
        weights=weights,
    )
    return choices[0]["name"], choices[0]["frequency"]


def get_price(fish_name: str) -> int:
    """获取鱼的价格"""
    config_fishes = config.fishes
    return next(
        (
            fish["price"]
            for fish in config_fishes
            if fish["name"] == fish_name
        ),
        0
    )

async def can_fishing(user_id: str) -> bool:
    """判断是否可以钓鱼"""
    time_now = int(time.time())
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        FishingRecord = await session.scalar(select_user)
        return True if not FishingRecord else FishingRecord.time < time_now
    
async def save_fish(user_id: str, fish_name: str) -> None:
    """向数据库写入鱼以持久化保存"""
    time_now = int(time.time())
    fishing_limit = config.fishing_limit
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        FishingRecord = await session.scalar(select_user)
        if FishingRecord:
            loads_fishes = json.loads(FishingRecord.fishes)
            try:
                loads_fishes[fish_name] += 1
            except KeyError:
                loads_fishes[fish_name] = 1
            dump_fishes = json.dumps(loads_fishes)
            user_update = update(FishingRecord).where(
                FishingRecord.user_id == user_id
            ).values(
                time=time_now + fishing_limit,
                frequency=FishingRecord.frequency + 1,
                fishes=dump_fishes
            )
            await session.execute(user_update)
            await session.commit()
            return
        data = {
            fish_name: 1
        }
        dump_fishes = json.dumps(data)
        new_FishingRecord = FishingRecord(
            user_id=user_id,
            time=time_now + fishing_limit,
            frequency=1,
            fishes=dump_fishes,
            special_fishes="{}",
            coin=0
        )
        session.add(new_FishingRecord)
        await session.commit()

async def get_stats(user_id: str) -> str:
    """获取钓鱼统计信息"""
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishing_Record = await session.scalar(select_user)
        if fishing_Record:
            return f"你钓鱼了 {fishing_Record.frequency} 次"
        return "你还没有钓过鱼，快去钓鱼吧"
    
def print_backpack(backpack: dict) -> str:
    """输出背包内容"""
    result = [
        f"{fish_name}×{str(quantity)}"
        for fish_name, quantity in backpack.items()
    ]
    return "背包:\n" + "\n".join(result)


async def get_backpack(user_id: str) -> str:
    """从数据库查询背包内容"""
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishes_Record = await session.scalar(select_user)
        if fishes_Record:
            load_fishes = json.loads(fishes_Record.fishes)
            return "你的背包里空无一物" if load_fishes == {} else print_backpack(load_fishes)
        return "你的背包里空无一物"
async def sell_fish(user_id: str, fish_name: str) -> str:
    """
    卖鱼

    参数：
      - user_id: 将要卖鱼的用户唯一标识符，用于区分谁正在卖鱼
      - fish_name: 将要卖鱼的鱼名称

    返回：
      - (str): 待回复的文本
    """
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishes_Record = await session.scalar(select_user)
        if fishes_Record := fishes_Record:
            loads_fishes = json.loads(fishes_Record.fishes)
            if fish_name in loads_fishes and loads_fishes[fish_name] > 0:
                fish_price = get_price(fish_name)
                loads_fishes[fish_name] -= 1
                if loads_fishes[fish_name] == 0:
                    del loads_fishes[fish_name]
                dump_fishes = json.dumps(loads_fishes)
                user_update = update(FishingRecord).where(
                    FishingRecord.user_id == user_id
                ).values(
                    coin=fishes_Record.coin + fish_price,
                    fishes=dump_fishes
                )
                await session.execute(user_update)
                await session.commit()
                return f"你以 {fish_price} {fishing_coin_name} / 条的价格卖出了 {fish_name}"
            return "查无此鱼"
        else:
            return "还没钓鱼就想卖鱼?"


async def get_balance(user_id: str) -> str:
    """获取余额"""
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishes_Record = await session.scalar(select_user)
        if fishes_Record:
            return f"你有 {fishes_Record.coin} {fishing_coin_name}"
        return "你什么也没有 :)"
