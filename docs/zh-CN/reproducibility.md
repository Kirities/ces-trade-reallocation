# 复现、数据字典与图表说明

[English version](../en/reproducibility.md)

## 执行

在仓库根目录运行。已使用 Python 3.12 执行；分析与测试仅依赖标准库，绘图另需 `requirements.txt` 中固定版本的依赖。

```sh
python scripts/analyze.py
python scripts/figures.py
python scripts/validate.py
python -m unittest discover -s tests -v
```

`python scripts/reproduce.py` 执行相同步骤。安装依赖后，无需 API 密钥、外部账户、原 PDF、Notebook 服务或网络调用。来源清单使用 SHA-256 固定归档提取数据。在线页面可能变化；更新数据时应明确提取新版本并记录日期，不静默覆盖原数据。

## 输入与输出

| 文件 | 变量与解释 |
|---|---|
| `data/raw/census_annual_extract.csv` | `partner`：越南、中国或全球；`year`：2010—2024；`us_exports_musd`、`us_imports_musd`、`us_balance_musd`：从美国角度记录的名义百万美元商品贸易值 |
| `data/raw/manifest.json` | 提取日期、来源链接、单位、方法和提取文件哈希 |
| `config/scenarios.json` | 情景网格与基准，不把任何参数称为计量估计值 |
| `results/annual_indicators.csv` | 进口总额、世界其他地区残差、比例形式的来源份额和 2017 基准指数 |
| `results/growth_decomposition.csv` | 起止年份、百万美元变化及分解项、比例形式复合增长率、百分点形式份额变化 |
| `results/scenario_grid.csv` | 校准年、弹性、关税比例、成本乘数、假定国内增加值比例，以及份额、价格指数、实际组合百分比变化、收入百分比变化、每 100 美元税收、补偿及增加值代理量 |
| `results/summary.json` | 正文使用的主要经验和模型数值 |
| `results/validation.json` | 自动数据、核算、情景重建、链接与文件检查及执行环境 |

选定的 45 行数据中没有缺失观测。`World` 是总量，与各国行相加会重复计算。越南出口和增加值代理量均不等于越南 GDP。`dva_proxy_per_100` 表示水平而非变化；不同国内增加值比例的记录共用同一进口配置。

## 图表说明

| 图表 | 证据类型 | 数据及解释 |
|---|---|---|
| `trade_reallocation` | 实际数据与派生指标 | 年度指标表；指数面板及共用尺度的份额面板。阴影仅表示 2018 年起的时期，不表示因果效果。 |
| `growth_decomposition` | 精确核算 | 分解表的 2017—2024 年行，柱形从零开始。 |
| `scenario_sensitivity` | 示意模型 | 四种弹性的确定性成本曲线，以及两种越南关税下的保留价值曲线，没有经验不确定性带。 |
| `cost_tariff_frontier` | 示意模型 | 2017 年权重、弹性为 4 的细网格；黑线表示海关价值收入增益为零。色标以零为中心。 |

PNG 用于仓库阅读，SVG 保留可编辑矢量和文字。两个语言版本共用英文图中文字。图注和替代文本明确区分观测与假设。线型和直接标注边界补充颜色编码，但不代表已取得通用无障碍认证。

## 核验能够说明什么

核验脚本检查来源哈希、完整且唯一的国家—年份键、有限数值、舍入容差内贸易差额、正的其他地区进口额、份额、分解恒等式、全情景网格重建、解析成本阈值、双语文档存在性、相对 Markdown 链接及 PNG/SVG 文件。单元测试覆盖基准恢复、海关价值与税收核算、统一价格缩放、统一关税、成本敏感性和无效输入。图表另经过视觉检查。

这些检查支持内部一致性和实际本地运行状态，不代表人工审稿、因果识别、独立数据审计、一般均衡有效性或期刊接收。本地运行也不等于已在另一台机器完成全新环境安装。
