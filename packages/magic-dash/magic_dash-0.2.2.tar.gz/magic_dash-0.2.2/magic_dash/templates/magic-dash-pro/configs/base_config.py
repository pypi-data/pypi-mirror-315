from typing import List


class BaseConfig:
    """应用基础配置参数"""

    # 应用基础标题
    app_title: str = "Magic Dash Pro"

    # 应用版本
    app_version: str = "0.2.2"

    # 浏览器最低版本限制规则
    min_browser_versions: List[dict] = [
        {"browser": "Chrome", "version": 88},
        {"browser": "Firefox", "version": 78},
        {"browser": "Edge", "version": 100},
    ]
