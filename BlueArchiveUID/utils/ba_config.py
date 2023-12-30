# 先导入基础配置模型
from typing import Dict

# 设定一个配置文件（json）保存文件路径
from gsuid_core.data_store import get_res_path

# 然后添加到GsCore网页控制台中
from gsuid_core.utils.plugins_config.gs_config import StringConfig
from gsuid_core.utils.plugins_config.models import (
    GSC,
    GsStrConfig,
    GsListStrConfig,
)

# 建立自己插件的CONFIG_DEFAULT
# 名字无所谓, 类型一定是Dict[str, GSC]，以下为示例，可以添加无数个配置
CONIFG_DEFAULT: Dict[str, GSC] = {
    'xtzx_token': GsStrConfig(
        '什亭之匣Token',
        'ba总力战需求该token获取信息',
        '',
    ),
    'guide_source': GsStrConfig(
        '优先攻略源',
        '选择默认优先攻略源',
        'hehedi',
        ['hehedi', 'bawiki'],
    ),
    'char_guide_source': GsListStrConfig(
        '发送角色攻略源',
        '可选择多个',
        ['hehedi', 'bawiki'],
        ['hehedi', 'bawiki'],
    ),
}

CONFIG_PATH = get_res_path('BlueArchiveUID') / 'config.json'

# 分别传入 配置总名称（不要和其他插件重复），配置路径，以及配置模型
ba_config = StringConfig('BlueArchiveUID', CONFIG_PATH, CONIFG_DEFAULT)
