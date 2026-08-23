# 二、命令与攻略

> 返回 [SKILL.md](../SKILL.md)

均需前缀 `ba`（`bauid_etcimg` 例外，见坑点）。

| 命令 | 模块 |
|------|------|
| `绑定` / `好友码` / `切换` / `删除` | `bauid_user` |
| `查询` / `查询vlhy4mw:1` | `bauid_info` |
| `角色攻略<名>` | `bauid_guide`（按 `char_guide_source` 多源发送） |
| `攻略5-3` / `攻略H1-3` | 关卡图 |
| `活动攻略` | 活动图 |
| `总力战` / `档线` / `挡线`（可加 `B`） | 什亭之匣 |
| `总力战档位` | 旧接口，注释写「无用」 |
| `算分` / `用时` | 总力战分数↔时间 |
| `jjc挖矿` | 青辉石估算 |
| `学生排行` / `角色排名` | 排行图 |
| `帮助` / `蔚蓝档案帮助` | 帮助图 |

攻略源配置：

- `guide_source`：关卡默认源 `hehedi` | `bawiki` | `all`
- `char_guide_source`：角色攻略可多选列表

实现：`get_guide.py` / `get_char.py` / `get_event.py`，别名 `alias.py`。
