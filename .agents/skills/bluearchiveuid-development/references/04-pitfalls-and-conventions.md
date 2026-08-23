# 四、坑点与规范

> 返回 [SKILL.md](../SKILL.md)

## 规范

新代码：Core `AGENTS.md` §1。行宽 120。
接 AI 时 `to_ai` 第一行写「蔚蓝档案」或「碧蓝档案」，`covers` 带领域前缀。
不要改松好友码校验。

## 坑

1. `Plugins` 在外层；内层无 `__init__.py`。
2. `ba节奏榜` 触发词已含 `ba`，再叠前缀会双写。
3. `bata_utime_to_socre.py` 文件名拼写不要「修正」除非同时改 import。
4. `CONIFG_DEFAULT` 历史拼写。
5. `总力战档位` 标了无用，优先维护什亭之匣命令。
6. 官方 Bot + URL：开 `disable_xtzx_url`。
7. SchaleDB json 在 `tools/`，运行时映射在 `utils/map/`；改学生 ID 要两头对齐。

## 改完自查

- [ ] 好友码示例带 `:1`/`:2`
- [ ] 新配置键进 `CONIFG_DEFAULT`
- [ ] 资源目录进 `resource_path.init_dir`
- [ ] `ruff check BlueArchiveUID`
