# AGENTS.md

> 本文件遵循 [AGENTS.md](https://agents.md/)：给编码 Agent 的仓库说明（README for agents）。
> 人类用户说明见 [README.md](./README.md)。**源码是唯一事实源**。
>
> 攻略源 / 好友码 / 总力战：按需读
> [`.agents/skills/bluearchiveuid-development/SKILL.md`](.agents/skills/bluearchiveuid-development/SKILL.md)，
> **不要**一次把所有 `references/` 塞进上下文。

本仓库是 **GsCore 业务插件**，独立 git。放到 `gsuid_core/plugins/BlueArchiveUID/` 安装。

## Project overview

蔚蓝档案 / 碧蓝档案：好友码绑定与箱庭查询、关卡/角色/活动攻略、总力战档线与算分、JJC 挖矿、节奏榜。

- **`Plugins(...)` 在外层 `__init__.py`**，不在内层包。内层 **没有** `__init__.py`，靠 `__full__.py` 扫描。改前缀只改外层：`force_prefix=["ba", "BA"]`，`allow_empty_prefix=False`。
- 绑定：**`BaBind`**。好友码 `code:1` 官服 / `code:2` B 服，不是纯数字 UID。
- **没有** `to_ai` / `@ai_tools`。
- 总力战档线需要配置 **什亭之匣** `xtzx_token`。
- 版本：`BlueArchiveUID/version.py` 当前 `0.4.1`。`pyproject.toml` poetry 可能仍是 `0.2.0`。

## Repository map

```
.
├── AGENTS.md / README.md / ICON.png
├── pyproject.toml / ruff.toml
├── __init__.py                         # Plugins(force_prefix=["ba","BA"])
├── __nest__.py
├── .agents/skills/bluearchiveuid-development/
└── BlueArchiveUID/                     # 无内层 __init__.py
    ├── __full__.py / version.py
    ├── bauid_user/                     # 绑定/切换/删除好友码
    ├── bauid_info/                     # 查询箱庭图
    ├── bauid_guide/                    # 关卡/角色/活动攻略
    ├── bauid_raid/                     # 总力战档线（什亭之匣）
    ├── bauid_score/                    # 算分 / 用时
    ├── bauid_jjcwk/                    # JJC 挖矿
    ├── bauid_ranklist/                 # 学生排行
    ├── bauid_etcimg/                   # 节奏榜静图
    ├── bauid_help/  bauid_startup/
    ├── tools/                          # SchaleDB json、切图
    └── utils/                          # ba_config / ba_api / database / map / resource_path
```

`bauid_score` 文件名有历史拼写：`bata_utime_to_socre.py`（socre）。`utils/map/weaponId2Nmae_map.json` 同样是历史拼写。不要「修正」文件名除非同时改 import。

运行时：`get_res_path("BlueArchiveUID")/`（config、guide、char、resource）。

## Skills

| 任务 | 读 |
|------|-----|
| 本插件 | [bluearchiveuid-development](.agents/skills/bluearchiveuid-development/SKILL.md) |
| 补 `to_ai` | Core [gscore-plugin-development](../../../.agents/skills/gscore-plugin-development/SKILL.md) |
| 代码红线 | Core 根 [`AGENTS.md`](../../../AGENTS.md) §1–§4、§1.9 |

单独 clone 时打开宿主 Core 的 `AGENTS.md`。

## Setup commands

在**本插件目录**执行。解释器指向 Core 根 `.venv`。

```sh
uv run ruff check BlueArchiveUID
uv run ruff format --check BlueArchiveUID
```

`ruff.toml`：`line-length = 120`。无 `tests/`；新逻辑补 `tests/test_*.py`。

## Code style

新代码与 Core 根 `AGENTS.md` **编号一致**，正反例以那份为准。

| 编号 | 要求 |
|------|------|
| §1.1 | 禁止 try-except 兜底。例外：下载攻略图 / 第三方 JSON |
| §1.2–1.4 | 禁止 `cast` / 自身 `type: ignore` / `getattr`·`dict.get` 兜底 |
| §1.6 | `#` 最多两行、每行 ≤88 字 |
| §1.7 | 不改 Core `system_prompt` |
| §1.8 | 禁止 `Any` |
| §1.9 | 总力战 / 青辉石等垂直词只写本插件，不写进框架词表 |
| §2 | 函数全标注；PEP 604 |
| §3 | `BaBind`：无 `__tablename__`，`@with_session`，`col()` |
| §4 | 全异步 |

行宽 120。配置默认值变量名历史拼写 **`CONIFG_DEFAULT`**，不要无意义重命名。
好友码必须含 `:`（可先把 `：` 换成 `:`）且以 `1` 或 `2` 结尾，不要改松。历史代码脏则改到哪修到哪。

## Testing

无套件。改算分解析或好友码校验时补单测，覆盖缺 `:1/:2`、官/B 服。

## 本仓库结构约定

- 嵌套加载：外层 `__nest__.py` + 内层 `__full__.py`。**不要**补空的内层 `__init__.py` 除非同时搬 `Plugins()`。
- 绑定：`BaBind.insert_uid(..., is_digit=False)`。
- 查询：`get_uid(bot, ev, BaBind, partten=r"[A-Za-z0-9:：]+")`。
- 攻略源：`guide_source` / `char_guide_source` = `hehedi` / `bawiki` / `all`。配置在 `utils/ba_config.py`（没有 `bauid_config` 包）。
- 启动：`bauid_startup/main.py` → `download_ba_resource()`。
- 学生/装备：`utils/map/*.json` 与 `tools/SchaleDB/`。

## 坑点

1. 好友码不是 UID。缺少 `:1`/`:2` 必须拒绝。
2. `bauid_etcimg` 的 `on_fullmatch(("ba节奏榜", ...))` 已含 `ba`，外层前缀再叠会变成 `ba ba节奏榜`。
3. 总力战文本含 `B`/`b` → `server_id=2`，否则官服 `1`。
4. `disable_xtzx_url`：官方 Bot 发不了未备案 URL 时关掉档线链接。
5. `总力战档位` 源码标了无用，优先维护什亭之匣命令。

## Security notes

- `xtzx_token` 只放运行时 config，禁止进 git / 日志。
- 公网 Core：`WS_TOKEN`。
