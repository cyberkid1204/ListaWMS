# !/usr/bin/env python
# -*-   coding:utf-8   -*-
# Author     ：NanZhou
# version    ：python 3.11
# =============================================
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "127.0.0.1",
                "port": "5434",
                "user": "postgres",
                "password": "123456",
                "database": "test1",
                "min_size": 1,  # 连接池中的最小连接数
                "max_size": 10,  # 连接池中的最大连接数
                "schema": "wms"
            },
        },
    },
    "apps": {
        "ListaWMS": {
            "models": ["models.user", "models.inbound", "aerich.models"],
            "default_connection": "default",
            "schemas": ["user", "inbound", "order"],
        }
    },
    "use_tz": True,  # 是否使用时区
    # 设置欧洲时区
    "timezone": "Europe/Berlin",
    "generate_schemas": True,  # 是否生成表格
}
