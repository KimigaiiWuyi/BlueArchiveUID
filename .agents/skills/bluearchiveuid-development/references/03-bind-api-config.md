# 三、绑定、API、配置

> 返回 [SKILL.md](../SKILL.md)

## 绑定

好友码必须匹配：含 `:`（允许全角 `：`，入库前替换）且以 `1` 或 `2` 结尾。

```python
await BaBind.insert_uid(qid, ev.bot_id, uid, ev.group_id, is_digit=False)
```

查询：`get_uid(bot, ev, BaBind, partten=r"[A-Za-z0-9:：]+", get_user_id=True)`。
未绑定提示里要带格式示例。

WebConsole：`BaBindadmin`。

## API

`utils/ba_api.py`：`ba_api = BaseBAApi()`，`xtzx_api = XTZXApi()`。
HTTP 细节：`utils/api/request.py`。总力战：`get_rank_data.py` 的 `get_ranking_from_xtzx`。

Token：`ba_config.get_config("xtzx_token").data`。空 token 时档线不可用，提示去群申请（README：949830458）。

## 配置

`utils/ba_config.py`：`ba_config = StringConfig("BlueArchiveUID", CONFIG_PATH, CONIFG_DEFAULT)`

| 键 | 作用 |
|----|------|
| `xtzx_token` | 什亭之匣 |
| `guide_source` | 关卡攻略优先源 |
| `char_guide_source` | 角色攻略源列表 |
| `disable_xtzx_url` | 去掉档线消息里的 URL |

路径：`utils/resource_path.py`。启动 `download_ba_resource()` 填图标。
