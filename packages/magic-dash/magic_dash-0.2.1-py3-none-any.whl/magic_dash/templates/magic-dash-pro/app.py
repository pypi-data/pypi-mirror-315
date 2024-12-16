import dash
from dash import html, set_props, dcc
import feffery_antd_components as fac
import feffery_utils_components as fuc
from flask_login import current_user, logout_user
from dash.dependencies import Input, Output, State

from server import app
from views import core_pages, login
from configs import RouterConfig  # 路由配置参数
from views.status_pages import _404, _500  # 各状态页面


app.layout = lambda: fuc.FefferyTopProgress(
    [
        # 全局消息提示
        fac.Fragment(id="global-message"),
        # 全局重定向
        fac.Fragment(id="global-redirect"),
        # 全局页面重载
        fac.Fragment(id="global-reload"),
        # 根节点url监听
        fuc.FefferyLocation(id="root-url"),
        # 应用根容器
        html.Div(
            id="root-container",
        ),
    ],
    listenPropsMode="include",
    includeProps=["root-container.children"],
    minimum=0.33,
    color="#1677ff",
)


def handle_root_router_error(e):
    """处理根节点路由错误"""

    set_props(
        "root-container",
        {
            "children": _500.render(e),
        },
    )


@app.callback(
    Output("root-container", "children"),
    Input("root-url", "pathname"),
    State("root-url", "trigger"),
    prevent_initial_call=True,
    on_error=handle_root_router_error,
)
def root_router(pathname, trigger):
    """根节点路由控制"""

    # 在动态路由切换时阻止根节点路由更新
    if trigger != "load":
        return dash.no_update

    # 无需校验登录状态的公共页面
    if pathname == "/404-demo":
        return _404.render()

    elif pathname == "/500-demo":
        return _500.render()

    elif pathname == "/login":
        return login.render()

    elif pathname == "/logout":
        # 当前用户登出
        logout_user()

        # 重定向至登录页面
        set_props(
            "global-redirect",
            {"children": dcc.Location(pathname="/login", id="global-redirect")},
        )
        return dash.no_update

    # 登录状态校验：若当前用户未登录
    if not current_user.is_authenticated:
        # 重定向至登录页面
        set_props(
            "global-redirect",
            {"children": dcc.Location(pathname="/login", id="global-redirect")},
        )

        return dash.no_update

    # 检查当前访问目标pathname是否为有效页面
    if pathname in RouterConfig.valid_pathnames.keys():
        # 处理核心功能页面渲染
        return core_pages.render()

    # 返回404状态页面
    return _404.render()


if __name__ == "__main__":
    # 非正式环境下开发调试预览用
    # 生产环境推荐使用gunicorn启动
    app.run(debug=True)
