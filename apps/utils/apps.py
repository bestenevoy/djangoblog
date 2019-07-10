from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class UtilsConfig(AppConfig):
    name = 'utils'

class SuitConfig(DjangoSuitConfig):
    # 布局，垂直'vertical'还是水平'horizontal'
    layout = 'vertical'
    # 配置菜单栏
    # menu = (
    #     # ParentItem 是一级标题栏。第一个参数是标题名，children 是list形式，里面放置了二级菜单。还可以传不定参数 icon，这是图标。
    #     # ChildItem 是二级菜单栏，第一个参数是标题名。不定参数 url=（这个任务具体的函数），icon。
    #     ParentItem('Content', children=[
    #         ChildItem(model='demo.country'),
    #         ChildItem(model='demo.continent'),
    #         ChildItem(model='demo.showcase'),
    #         ChildItem('Custom view', url='/admin/custom/'),
    #     ], icon='fa fa-leaf'),
    #     ParentItem('Integrations', children=[
    #         ChildItem(model='demo.city'),
    #     ]),
    #     ParentItem('用户管理', children=[
    #         ChildItem(model='auth.user'),
    #         ChildItem('User groups', 'auth.group'),
    #     ], icon='fa fa-users'),
    #     ParentItem('账号安全', children=[
    #         ChildItem('Password change', url='admin:password_change'),
    #         ChildItem('Open Google', url='http://google.com', target_blank=True),
    #
    #     ], align_right=True, icon='fa fa-cog'),
    # )

    def ready(self):
        super(SuitConfig, self).ready()

        # DO NOT COPY FOLLOWING LINE
        # It is only to prevent updating last_login in DB for demo app
        self.prevent_user_last_login()

    def prevent_user_last_login(self):
        """
        Disconnect last login signal
        """
        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        user_logged_in.disconnect(update_last_login)