"""provincecapitals 命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .model import (
    REGIONS,
    capital_of,
    make_matching,
    make_quiz,
    province_info,
    province_of,
    stats,
)
from .render import matching_html, quiz_html


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="provincecapitals", description="中国省级行政区与省会：查询与配对练习"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    capital = sub.add_parser("capital", help="查询省会")
    capital.add_argument("province")

    province = sub.add_parser("province", help="根据省会反查省份")
    province.add_argument("capital")

    info = sub.add_parser("info", help="查看完整信息")
    info.add_argument("province")

    listing = sub.add_parser("list", help="列出省级行政区")
    listing.add_argument("--region", default=None, help="只显示某个分区")

    sub.add_parser("regions", help="列出地理分区与数量")

    matching = sub.add_parser("matching", help="生成连线题")
    matching.add_argument("--count", type=int, default=8)
    matching.add_argument("--seed", type=int, default=0)
    matching.add_argument("-o", "--output", required=True)
    matching.add_argument("--no-answers", action="store_true")

    quiz = sub.add_parser("quiz", help="生成选择题")
    quiz.add_argument("--count", type=int, default=6)
    quiz.add_argument("--seed", type=int, default=0)
    quiz.add_argument("--kind", choices=("capital", "province"), default="capital")
    quiz.add_argument("-o", "--output", required=True)
    quiz.add_argument("--no-answers", action="store_true")

    return parser


def _run(args: argparse.Namespace) -> int:
    if args.command == "capital":
        province = province_info(args.province)
        print("%s 的省会（首府）是 %s" % (province.name, province.capital))
        return 0
    if args.command == "province":
        print("%s 对应的省级行政区是 %s" % (args.capital.strip(), province_of(args.capital)))
        return 0
    if args.command == "info":
        province = province_info(args.province)
        print(province.name)
        print("省会：%s" % province.capital)
        print("分区：%s" % province.region)
        print("类型：%s" % province.kind)
        return 0
    if args.command == "list":
        data = stats()
        region_counts = data["by_region"]  # type: ignore[assignment]
        regions = [args.region] if args.region else list(REGIONS)
        for region in regions:
            from .model import by_region

            items = by_region(region)
            print("%s（%d）" % (region, region_counts.get(region, len(items))))
            for province in items:
                print("  %s — %s（%s）" % (province.name, province.capital, province.kind))
        return 0
    if args.command == "regions":
        data = stats()
        region_counts = data["by_region"]  # type: ignore[assignment]
        for region in REGIONS:
            print("%s：%d 个省级行政区" % (region, region_counts[region]))
        print("合计：%d 个" % data["total"])
        return 0
    if args.command == "matching":
        pairs = make_matching(args.count, args.seed)
        Path(args.output).write_text(
            matching_html(pairs, seed=args.seed, include_answers=not args.no_answers),
            encoding="utf-8",
        )
        print("已生成连线题：%s（%d 组）" % (args.output, len(pairs)))
        return 0
    if args.command == "quiz":
        questions = make_quiz(args.count, args.seed, args.kind)
        Path(args.output).write_text(
            quiz_html(questions, include_answers=not args.no_answers),
            encoding="utf-8",
        )
        print("已生成选择题：%s（%d 题）" % (args.output, len(questions)))
        return 0
    raise ValueError("未知命令：%s" % args.command)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except (TypeError, ValueError) as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
