"""省会配对练习与分区表渲染。"""

from __future__ import annotations

import html
import random
from typing import Dict, Sequence, Tuple

from .model import LETTERS, PROVINCES, REGIONS


def _safe(text: object) -> str:
    return html.escape(str(text), quote=True)


def region_table_html() -> str:
    """按分区列出全部省级行政区。"""
    sections = []
    for region in REGIONS:
        items = [province for province in PROVINCES if province.region == region]
        cards = "".join(
            "<li><strong>%s</strong><span>%s · %s</span></li>"
            % (_safe(province.name), _safe(province.capital), _safe(province.kind))
            for province in items
        )
        sections.append(
            "<section><h2>%s（%d）</h2><ul class=\"cards\">%s</ul></section>"
            % (_safe(region), len(items), cards)
        )
    return "".join(sections)


def matching_key_html(pairs: Sequence[Tuple[str, str]]) -> str:
    if not pairs:
        raise ValueError("至少需要一组配对")
    items = "".join(
        "<li>%s — %s</li>" % (_safe(province), _safe(capital))
        for province, capital in pairs
    )
    return "<ol class=\"key\">%s</ol>" % items


def matching_html(
    pairs: Sequence[Tuple[str, str]],
    title: str = "省份与省会配对",
    seed: int = 0,
    include_answers: bool = True,
) -> str:
    """生成省份—省会连线题练习页。"""
    if not pairs:
        raise ValueError("至少需要一组配对")
    safe_title = _safe(title or "省份与省会配对")
    rng = random.Random(seed)
    lefts = [province for province, _ in pairs]
    rights = [capital for _, capital in pairs]
    rng.shuffle(rights)
    rows = "".join(
        "<tr><td class=\"left\">%d. %s</td><td class=\"dots\">…………</td>"
        "<td class=\"right\">%s. %s</td></tr>"
        % (
            index + 1,
            _safe(left),
            LETTERS[index % len(LETTERS)],
            _safe(rights[index]),
        )
        for index, left in enumerate(lefts)
    )
    answer_block = (
        "<section class=\"card\"><h2>参考答案</h2>%s</section>" % matching_key_html(pairs)
        if include_answers
        else ""
    )
    return (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>%s</title>\n<style>\n"
        "body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;"
        "background:#fef2f2;margin:0;padding:24px;color:#0f172a}\n"
        ".card{max-width:720px;margin:0 auto 20px;background:#fff;border-radius:16px;"
        "padding:24px;box-shadow:0 10px 24px rgba(15,23,42,.1)}\n"
        "h1{font-size:21px;margin:0 0 14px}h2{font-size:16px;margin:0 0 10px}\n"
        "table{width:100%%;border-collapse:collapse;font-size:16px}\n"
        "td{padding:10px 4px}.left{text-align:right;width:38%%}\n"
        ".right{width:38%%}.dots{text-align:center;color:#cbd5e1;font-size:12px}\n"
        ".key{line-height:1.9;font-size:14px}\n"
        "footer{font-size:12px;color:#64748b;margin-top:14px}\n"
        "</style>\n</head>\n<body>\n"
        "<section class=\"card\"><h1>%s</h1><p>把省级行政区与它的省会（首府）连起来。</p>"
        "<table>%s</table><footer>由 provincecapitals 生成 · 共 %d 组</footer></section>\n"
        "%s\n</body>\n</html>"
        % (safe_title, safe_title, rows, len(pairs), answer_block)
    )


def quiz_key_html(questions: Sequence[Dict[str, object]]) -> str:
    if not questions:
        raise ValueError("至少需要一道题")
    items = "".join(
        "<li>%d. %s（%s）</li>"
        % (index, _safe(question["answer"]), _safe(question["prompt"]))
        for index, question in enumerate(questions, start=1)
    )
    return "<ol class=\"key\">%s</ol>" % items


def quiz_html(
    questions: Sequence[Dict[str, object]],
    title: str = "省份与省会练习",
    include_answers: bool = True,
) -> str:
    """生成省份—省会选择题页面。"""
    if not questions:
        raise ValueError("至少需要一道题")
    safe_title = _safe(title or "省份与省会练习")
    blocks = []
    for index, question in enumerate(questions, start=1):
        if question.get("kind") == "province":
            stem = "“%s”是哪个省级行政区的省会（首府）？" % _safe(question["prompt"])
        else:
            stem = "“%s”的省会（首府）是：" % _safe(question["prompt"])
        options = "".join(
            "<label class=\"opt\"><input type=\"radio\" name=\"q%d\"> %s. %s</label>"
            % (index, LETTERS[position % len(LETTERS)], _safe(choice))
            for position, choice in enumerate(question["choices"])  # type: ignore[arg-type]
        )
        blocks.append(
            "<div class=\"q\"><p>%d. %s</p><div class=\"opts\">%s</div></div>"
            % (index, stem, options)
        )
    answer_block = (
        "<section class=\"card\"><h2>参考答案</h2>%s</section>" % quiz_key_html(questions)
        if include_answers
        else ""
    )
    return (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>%s</title>\n<style>\n"
        "body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;"
        "background:#f0fdf4;margin:0;padding:24px;color:#0f172a}\n"
        ".card{max-width:720px;margin:0 auto 20px;background:#fff;border-radius:16px;"
        "padding:24px;box-shadow:0 10px 24px rgba(15,23,42,.1)}\n"
        "h1{font-size:21px;margin:0 0 14px}h2{font-size:16px;margin:0 0 10px}\n"
        ".q{margin-bottom:16px}.q p{margin:0 0 6px;font-size:15px}\n"
        ".opts{display:flex;flex-wrap:wrap;gap:12px;color:#334155}\n"
        ".opt{font-size:14px;background:#f8fafc;border-radius:8px;padding:4px 10px}\n"
        ".key{line-height:1.9;font-size:14px}\n"
        "footer{font-size:12px;color:#64748b;margin-top:14px}\n"
        "</style>\n</head>\n<body>\n"
        "<section class=\"card\"><h1>%s</h1>%s"
        "<footer>由 provincecapitals 生成 · 共 %d 题</footer></section>\n"
        "%s\n</body>\n</html>"
        % (safe_title, safe_title, "".join(blocks), len(questions), answer_block)
    )


def cards_html() -> str:
    """以卡片网格展示所有省级行政区。"""
    cards = "".join(
        "<div class=\"card\"><strong>%s</strong><span>%s</span><em>%s</em></div>"
        % (
            _safe(province.name),
            _safe(province.capital),
            _safe(province.region + " · " + province.kind),
        )
        for province in PROVINCES
    )
    return "<div class=\"grid\">%s</div>" % cards
