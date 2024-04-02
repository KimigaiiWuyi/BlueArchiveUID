from typing import Optional

from sqlmodel import Field
from gsuid_core.utils.database.base_models import Bind
from gsuid_core.webconsole.mount_app import PageSchema, GsAdminModel, site


class BaBind(Bind, table=True):
    uid: Optional[str] = Field(default=None, title='Ba好友码')


@site.register_admin
class BaBindadmin(GsAdminModel):
    pk_name = 'id'
    page_schema = PageSchema(
        label='Ba绑定管理',
        icon='fa fa-users',
    )  # type: ignore

    # 配置管理模型
    model = BaBind
