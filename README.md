# provincecapitals

[![CI](https://github.com/eastyou/provincecapitals/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/provincecapitals/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

中国省级行政区与省会（首府）学习工具：查询、分区浏览和配对练习。

## 功能

- 收录 34 个省级行政区，包含省、自治区、直辖市和特别行政区
- 支持简称与别名：河北、内蒙古、广西、西藏、宁夏、新疆、香港、澳门等
- 省会正向查询与反向查询（含「北京市」这类带后缀写法）
- 按华北、东北、华东、华中、华南、西南、西北七个分区浏览
- 统计各分区与各类型数量
- 生成省份—省会产生连线题，附答案页
- 生成四选一选择题，支持「看省选省会」和「看省会选省」两种题型
- 自动批改并生成百分制成绩

## 安装

```bash
pip install -e .
```

也可以直接运行 `python -m provincecapitals`。

## 使用

```bash
provincecapitals capital 广东         # 广东省 的省会（首府）是 广州
provincecapitals capital 内蒙古       # 呼和浩特
provincecapitals province 广州        # 广州 对应的省级行政区是 广东省
provincecapitals info 香港            # 省会、分区、类型
provincecapitals list --region 东北
provincecapitals regions

# 连线题
provincecapitals matching --count 8 --seed 7 -o examples/sheet.html

# 选择题
provincecapitals quiz --count 6 --kind province -o examples/quiz.html
```

## 作为库使用

```python
from provincecapitals import capital_of, province_of, by_region, make_quiz

assert capital_of("广东") == "广州"
assert province_of("广州") == "广东省"
assert len(by_region("东北")) == 3
questions = make_quiz(3, seed=1, kind="capital")
assert all(len(set(q["choices"])) == 4 for q in questions)
```

## 示例

[examples/sheet.html](examples/sheet.html) 是 8 组省份—省会对连线题，附答案页。

## 测试

```bash
python -m unittest discover -s tests -v
```

共 104 项单元测试，覆盖 34 个省级行政区的正向/反向查询、别名补全、分区统计、题目唯一性、批改逻辑和 HTML 转义。CI 覆盖 Python 3.9 ~ 3.13 与三大操作系统。

## 许可

MIT © 2026 eastyou
