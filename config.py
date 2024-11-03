from pydantic import BaseModel
from typing import List, Dict
from nonebot import get_plugin_config


class Config(BaseModel):

    fishes: List[Dict] = [
        {
            "name": "破碎的CD",
            "frequency": 15,
            "weight": 100,
            "price": 0
        },
        {
            "name": "垃圾",
            "frequency": 30,
            "weight": 100,
            "price": 0
        },
        {
            "name": "浮木",
            "frequency": 5,
            "weight": 5,
            "price": 0
        },
        {
            "name": "破碎的眼镜",
            "frequency": 10,
            "weight": 1,
            "price": 0
        },
        {
            "name": "河豚",
            "frequency": 80,
            "weight": 100,
            "price": 10
        },
        {
            "name": "比目鱼",
            "frequency": 120,
            "weight": 100,
            "price": 100
        },
        {
            "name": "太阳鱼",
            "frequency": 60,
            "weight": 100,
            "price": 50
        },
        {
            "name": "小龙虾",
            "frequency": 10,
            "weight": 100,
            "price": 10
        },
        {
            "name": "水草",
            "frequency": 5,
            "weight": 100,
            "price": 10
        },{
            "name": "秋刀鱼",
            "frequency": 160,
            "weight": 100,
            "price": 425
        },{
            "name": "蜗牛",
            "frequency": 40,
            "weight": 100,
            "price": 5
        },{
            "name": "狗鱼",
            "frequency": 30,
            "weight": 100,
            "price": 20
        },{
            "name": "小嘴鲈鱼(高品质)",
            "frequency": 90,
            "weight": 100,
            "price": 120
        },{
            "name": "大水草",
            "frequency": 30,
            "weight": 100,
            "price": 20
        },{
            "name": "太阳鱼(高品质)",
            "frequency": 60,
            "weight": 100,
            "price": 75
        },{
            "name": "小嘴鲈鱼",
            "frequency": 30,
            "weight": 100,
            "price": 40
        },{
            "name": "河鲈",
            "frequency": 130,
            "weight": 100,
            "price": 95
        },{
            "name": "虹鳟鱼",
            "frequency":60,
            "weight": 100,
            "price": 75
        },{
            "name": "大嘴鲈鱼",
            "frequency": 90,
            "weight": 100,
            "price": 125
        },{
            "name": "金枪鱼",
            "frequency": 180,
            "weight": 100,
            "price": 300
        }

    ]

    fishing_limit: int = 5

    fishing_coin_name: str = "RMB"  # It means Fishing Coin.

    special_fish_enabled: bool = False

    special_fish_price: int = 5

    special_fish_probability: float = 0.01


config = get_plugin_config(Config)
