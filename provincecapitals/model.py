"""中国省级行政区与省会（首府）数据、查询和练习。"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Province:
    """一个省级行政区及其省会（或直辖市、特别行政区本身）。"""

    name: str
    capital: str
    region: str
    kind: str


PROVINCES: Tuple[Province, ...] = (
    Province("北京市", "北京", "华北", "直辖市"),
    Province("天津市", "天津", "华北", "直辖市"),
    Province("河北省", "石家庄", "华北", "省"),
    Province("山西省", "太原", "华北", "省"),
    Province("内蒙古自治区", "呼和浩特", "华北", "自治区"),
    Province("辽宁省", "沈阳", "东北", "省"),
    Province("吉林省", "长春", "东北", "省"),
    Province("黑龙江省", "哈尔滨", "东北", "省"),
    Province("上海市", "上海", "华东", "直辖市"),
    Province("江苏省", "南京", "华东", "省"),
    Province("浙江省", "杭州", "华东", "省"),
    Province("安徽省", "合肥", "华东", "省"),
    Province("福建省", "福州", "华东", "省"),
    Province("江西省", "南昌", "华东", "省"),
    Province("山东省", "济南", "华东", "省"),
    Province("台湾省", "台北", "华东", "省"),
    Province("河南省", "郑州", "华中", "省"),
    Province("湖北省", "武汉", "华中", "省"),
    Province("湖南省", "长沙", "华中", "省"),
    Province("广东省", "广州", "华南", "省"),
    Province("广西壮族自治区", "南宁", "华南", "自治区"),
    Province("海南省", "海口", "华南", "省"),
    Province("香港特别行政区", "香港", "华南", "特别行政区"),
    Province("澳门特别行政区", "澳门", "华南", "特别行政区"),
    Province("重庆市", "重庆", "西南", "直辖市"),
    Province("四川省", "成都", "西南", "省"),
    Province("贵州省", "贵阳", "西南", "省"),
    Province("云南省", "昆明", "西南", "省"),
    Province("西藏自治区", "拉萨", "西南", "自治区"),
    Province("陕西省", "西安", "西北", "省"),
    Province("甘肃省", "兰州", "西北", "省"),
    Province("青海省", "西宁", "西北", "省"),
    Province("宁夏回族自治区", "银川", "西北", "自治区"),
    Province("新疆维吾尔自治区", "乌鲁木齐", "西北", "自治区"),
)

REGIONS: Tuple[str, ...] = ("华北", "东北", "华东", "华中", "华南", "西南", "西北")

ALIASES: Dict[str, str] = {
    "内蒙古": "内蒙古自治区",
    "广西": "广西壮族自治区",
    "西藏": "西藏自治区",
    "宁夏": "宁夏回族自治区",
    "新疆": "新疆维吾尔自治区",
    "香港": "香港特别行政区",
    "澳门": "澳门特别行政区",
}

_BY_NAME: Dict[str, Province] = {province.name: province for province in PROVINCES}
_CAPITALS: Dict[str, Province] = {province.capital: province for province in PROVINCES}

LETTERS = ("A", "B", "C", "D")


def _require_text(value: object, name: str = "名称") -> str:
    if not isinstance(value, str):
        raise TypeError("%s 必须是字符串" % name)
    text = value.strip()
    if not text:
        raise ValueError("%s 不能为空" % name)
    return text


def normalize(name: str) -> str:
    """把简称、别名补全成完整的省级行政区名称。"""
    text = _require_text(name)
    if text in _BY_NAME:
        return text
    if text in ALIASES:
        return ALIASES[text]
    for suffix in ("省", "市"):
        candidate = text + suffix
        if candidate in _BY_NAME:
            return candidate
    raise ValueError("未知省级行政区：%s" % text)


def province_info(name: str) -> Province:
    """查询省级行政区的完整信息。"""
    return _BY_NAME[normalize(name)]


def capital_of(name: str) -> str:
    """返回省会（首府）名称。"""
    return province_info(name).capital


def province_of(capital: str) -> str:
    """根据省会（首府）反查省级行政区。"""
    text = _require_text(capital)
    if text in _CAPITALS:
        return _CAPITALS[text].name
    if text.endswith("市") and text[:-1] in _CAPITALS:
        return _CAPITALS[text[:-1]].name
    raise ValueError("未找到该城市对应的省级行政区：%s" % text)


def region_of(name: str) -> str:
    """返回所属地理分区。"""
    return province_info(name).region


def by_region(region: str) -> List[Province]:
    """列出某个地理分区的全部省级行政区。"""
    text = _require_text(region, "分区")
    if text not in REGIONS:
        raise ValueError("未知分区：%s（可选：%s）" % (text, "、".join(REGIONS)))
    return [province for province in PROVINCES if province.region == text]


def regions() -> List[str]:
    """按固定顺序返回地理分区名称。"""
    return list(REGIONS)


def stats() -> Dict[str, object]:
    """统计省级行政区总数、分区数量与类型数量。"""
    by_region_counts = {
        region: len([p for p in PROVINCES if p.region == region]) for region in REGIONS
    }
    by_kind: Dict[str, int] = {}
    for province in PROVINCES:
        by_kind[province.kind] = by_kind.get(province.kind, 0) + 1
    return {
        "total": len(PROVINCES),
        "by_region": by_region_counts,
        "by_kind": by_kind,
    }


def make_matching(
    count: int = 8, seed: Optional[int] = None
) -> List[Tuple[str, str]]:
    """生成省份—省会连线题。"""
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("题目数量必须是整数")
    if count <= 0:
        raise ValueError("题目数量必须大于 0")
    if count > len(PROVINCES):
        raise ValueError("题目数量不能超过 %d" % len(PROVINCES))
    rng = random.Random(seed)
    picked = rng.sample(list(PROVINCES), count)
    return [(province.name, province.capital) for province in picked]


def make_quiz(
    count: int = 6,
    seed: Optional[int] = None,
    kind: str = "capital",
) -> List[Dict[str, object]]:
    """生成选择题：根据省份选省会，或根据省会选省份。"""
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("题目数量必须是整数")
    if count <= 0:
        raise ValueError("题目数量必须大于 0")
    if count > len(PROVINCES):
        raise ValueError("题目数量不能超过 %d" % len(PROVINCES))
    if kind not in ("capital", "province"):
        raise ValueError("题型只能是 capital 或 province")
    rng = random.Random(seed)
    picked = rng.sample(list(PROVINCES), count)
    questions: List[Dict[str, object]] = []
    for province in picked:
        if kind == "capital":
            prompt, answer = province.name, province.capital
            pool = [item.capital for item in PROVINCES]
        else:
            prompt, answer = province.capital, province.name
            pool = [item.name for item in PROVINCES]
        distractors = [item for item in pool if item != answer]
        choices = rng.sample(distractors, 3) + [answer]
        rng.shuffle(choices)
        questions.append(
            {
                "prompt": prompt,
                "answer": answer,
                "choices": choices,
                "kind": kind,
            }
        )
    return questions


def grade(
    questions: Sequence[Dict[str, object]], answers: Sequence[str]
) -> Dict[str, int]:
    """按顺序批改选择题。"""
    if not questions:
        raise ValueError("没有可批改的题目")
    if len(questions) != len(answers):
        raise ValueError("答案数量与题目数量不一致")
    correct = 0
    for question, answer in zip(questions, answers):
        if not isinstance(answer, str):
            raise TypeError("答案必须是字符串")
        if answer.strip() == str(question["answer"]).strip():
            correct += 1
    total = len(questions)
    return {"correct": correct, "total": total, "score": round(correct * 100 / total)}
