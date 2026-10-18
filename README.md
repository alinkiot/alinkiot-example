# alinkiot-example

ALink IoT 示例与技能集合，包含文档、示例代码和可复用技能。

## 目录结构

```
alinkiot-example/
├── doc/        # 文章与技术文档
├── example/    # 示例项目
└── skills/     # 可复用技能（Kiro Skills）
```

### doc

存放技术文章、方案说明、协议分析等文档。

### example

存放完整的示例项目，每个子目录对应一个独立场景，包含可运行的代码和说明。

| 目录 | 说明 |
|------|------|
| [gaosu_gonglu_jiance](./example/gaosu_gonglu_jiance/) | 高速公路检测示例（含 3D 可视化） |

### skills

存放封装好的 Kiro Skills，可直接挂载到 Agent 使用。

| 目录 | 说明 |
|------|------|
| [solar-pv-troubleshooting](./skills/solar-pv-troubleshooting/) | 光伏设备故障排查技能 |

## 使用方式

克隆仓库后，进入对应 `example` 子目录查看各示例的 README 或直接运行。

```bash
git clone <repo-url>
cd alinkiot-example
```

## License

[Apache 2.0](./LICENSE)
