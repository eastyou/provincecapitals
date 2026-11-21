"""provincecapitals：省级行政区与省会查询及练习生成。"""

from .model import (
    PROVINCES,
    REGIONS,
    Province,
    by_region,
    capital_of,
    grade,
    make_matching,
    make_quiz,
    normalize,
    province_info,
    province_of,
    region_of,
    regions,
    stats,
)
from .render import (
    cards_html,
    matching_html,
    matching_key_html,
    quiz_html,
    quiz_key_html,
    region_table_html,
)

__all__ = [
    "PROVINCES",
    "REGIONS",
    "Province",
    "by_region",
    "capital_of",
    "grade",
    "make_matching",
    "make_quiz",
    "normalize",
    "province_info",
    "province_of",
    "region_of",
    "regions",
    "stats",
    "cards_html",
    "matching_html",
    "matching_key_html",
    "quiz_html",
    "quiz_key_html",
    "region_table_html",
]

__version__ = "0.1.0"
