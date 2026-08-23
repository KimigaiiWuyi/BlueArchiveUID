---
name: bluearchiveuid-development
description: >
  当用户要求"维护/开发 BlueArchiveUID"、"蔚蓝档案/碧蓝档案插件"、"ba绑定好友码"、
  "总力战档线/算分/用时"、"hehedi/bawiki 攻略"、"什亭之匣 token"、"JJC挖矿"、
  "BaBind"、"改 BlueArchiveUID 有哪些坑"时触发此 SKILL。
  凡是改动 `gsuid_core/plugins/BlueArchiveUID` 的任务都应优先读取此 SKILL。
---

# BlueArchiveUID 插件开发与维护指南（核心入口）

> 源码是唯一事实源。按表打开**一篇** `references/`。

## 谁该读

| 任务 | 文档 |
|------|------|
| 改本插件 | **本 SKILL** |
| 补 `to_ai` | Core `gscore-plugin-development` §10 |
| 代码红线 | [`AGENTS.md`](../../../AGENTS.md) |

## 文档目录索引

| 章节 | 主题 | 链接 |
|------|------|------|
| 一 | 架构与模块 | [references/01-architecture-and-modules.md](./references/01-architecture-and-modules.md) |
| 二 | 命令与攻略 | [references/02-commands-and-guides.md](./references/02-commands-and-guides.md) |
| 三 | 绑定、API、配置 | [references/03-bind-api-config.md](./references/03-bind-api-config.md) |
| 四 | 坑点与规范 | [references/04-pitfalls-and-conventions.md](./references/04-pitfalls-and-conventions.md) |

## 关键概念速记

- 前缀 `ba` / `BA`。`Plugins` 在**外层** `__init__.py`。
- 好友码 `xxxx:1` 官服 / `xxxx:2` B 服。表是 `BaBind`。
- 攻略源 hehedi / bawiki。总力战档线要 `xtzx_token`。
- 无 `to_ai`。
