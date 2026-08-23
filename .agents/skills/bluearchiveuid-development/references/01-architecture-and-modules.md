# 一、架构与模块全景

> 返回 [SKILL.md](../SKILL.md)

外层：

```python
# BlueArchiveUID/__init__.py（仓库根，不是内层包）
Plugins(name="BlueArchiveUID", force_prefix=["ba", "BA"], allow_empty_prefix=False)
```

内层 `BlueArchiveUID/` **没有** `__init__.py`，有 `__full__.py`。框架按嵌套模式扫描子目录。

| 子包 | 职责 |
|------|------|
| `bauid_user` | 绑定/切换/删除好友码 |
| `bauid_info` | `查询` 箱庭图 |
| `bauid_guide` | 关卡攻略、角色攻略、活动攻略 |
| `bauid_raid` | 总力战档线（什亭之匣） |
| `bauid_score` | 算分 / 用时 |
| `bauid_jjcwk` | 竞技场挖矿（青辉石） |
| `bauid_ranklist` | 学生排行 |
| `bauid_etcimg` | 节奏榜静图 |
| `bauid_help` | 帮助 |
| `bauid_startup` | 启动下载 |
| `utils/` | `ba_config`、`ba_api`、`database`、`resource_path`、alias、map |
| `tools/` | SchaleDB 原始 json、切图压缩 |

出图：PIL（`draw_user_info_pic` 等）+ 远程攻略图（下载到 `GUIDE_PATH` / `CHAR_PATH`）。
