import dash
from flask import request
from user_agents import parse
from flask_login import LoginManager, UserMixin, current_user
from flask_principal import Principal, Permission, RoleNeed, identity_loaded

# 应用基础参数
from models.users import Users
from configs import BaseConfig, AuthConfig

app = dash.Dash(
    __name__,
    title=BaseConfig.app_title,
    suppress_callback_exceptions=True,
    compress=True,  # 隐式依赖flask-compress
    update_title=None,
)
server = app.server

# 设置应用密钥
app.server.secret_key = "magic-dash-pro-demo"

# 为当前应用添加flask-login用户登录管理
login_manager = LoginManager()
login_manager.init_app(app.server)

# 为当前应用添加flask-principal权限管理
principals = Principal(app.server)


class User(UserMixin):
    """flask-login专用用户类"""

    def __init__(self, id: str, user_name: str, user_role: str) -> None:
        """初始化用户信息"""

        self.id = id
        self.user_name = user_name
        self.user_role = user_role


@login_manager.user_loader
def user_loader(user_id):
    """flask-login内部专用用户加载函数"""

    # 根据当前要加载的用户id，从数据库中获取匹配用户信息
    match_user = Users.get_user(user_id)

    # 当前用户实例化
    user = User(
        id=match_user.user_id,
        user_name=match_user.user_name,
        user_role=match_user.user_role,
    )

    return user


# 定义不同用户角色
user_permissions = {role: Permission(RoleNeed(role)) for role in AuthConfig.roles}


@identity_loaded.connect_via(app.server)
def on_identity_loaded(sender, identity):
    """flask-principal身份加载回调函数"""

    identity.user = current_user

    if hasattr(current_user, "user_role"):
        identity.provides.add(RoleNeed(current_user.user_role))


@app.server.before_request
def check_browser():
    """检查浏览器版本是否符合最低要求"""

    # 提取当前请求对应的浏览器信息
    user_agent = parse(str(request.user_agent))

    # 若浏览器版本信息有效
    if user_agent.browser.version != ():
        # IE相关浏览器直接拦截
        if user_agent.browser.family == "IE":
            return (
                "<div style='font-size: 22px; color: red; position: fixed; top: 40%; left: 50%; transform: translateX(-50%);'>"
                "请不要使用IE浏览器，或开启了IE内核兼容模式的其他浏览器访问本应用</div>"
            )
        # 基于BaseConfig.min_browser_versions配置，对相关浏览器最低版本进行检查
        for rule in BaseConfig.min_browser_versions:
            # 若当前请求对应的浏览器版本，低于声明的最低支持版本
            if (
                user_agent.browser.family == rule["browser"]
                and user_agent.browser.version[0] < rule["version"]
            ):
                return (
                    "<div style='font-size: 22px; color: red; position: fixed; top: 40%; left: 50%; transform: translateX(-50%);'>"
                    "您的{}浏览器版本低于本应用最低支持版本（{}），请升级浏览器后再访问</div>"
                ).format(rule["browser"], rule["version"])
