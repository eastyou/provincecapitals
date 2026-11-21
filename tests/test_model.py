"""provincecapitals 核心逻辑测试。"""

import unittest

from provincecapitals.model import (
    ALIASES,
    PROVINCES,
    REGIONS,
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


class DataTests(unittest.TestCase):
    def test_total_count(self):
        self.assertEqual(len(PROVINCES), 34)

    def test_names_unique(self):
        names = [p.name for p in PROVINCES]
        self.assertEqual(len(names), len(set(names)))

    def test_capitals_unique(self):
        capitals = [p.capital for p in PROVINCES]
        self.assertEqual(len(capitals), len(set(capitals)))

    def test_all_regions_known(self):
        for province in PROVINCES:
            with self.subTest(province=province.name):
                self.assertIn(province.region, REGIONS)

    def test_all_kinds_known(self):
        kinds = {"省", "自治区", "直辖市", "特别行政区"}
        for province in PROVINCES:
            self.assertIn(province.kind, kinds)

    def test_every_region_has_provinces(self):
        for region in REGIONS:
            with self.subTest(region=region):
                self.assertGreater(len(by_region(region)), 0)


class NormalizeTests(unittest.TestCase):
    def test_exact_name(self):
        self.assertEqual(normalize("广东省"), "广东省")

    def test_add_province_suffix(self):
        self.assertEqual(normalize("河北"), "河北省")

    def test_add_city_suffix(self):
        self.assertEqual(normalize("北京"), "北京市")

    def test_alias_inner_mongolia(self):
        self.assertEqual(normalize("内蒙古"), "内蒙古自治区")

    def test_alias_guangxi(self):
        self.assertEqual(normalize("广西"), "广西壮族自治区")

    def test_alias_xinjiang(self):
        self.assertEqual(normalize("新疆"), "新疆维吾尔自治区")

    def test_strips_spaces(self):
        self.assertEqual(normalize(" 上海 "), "上海市")

    def test_unknown(self):
        with self.assertRaises(ValueError):
            normalize("火星")

    def test_empty(self):
        with self.assertRaises(ValueError):
            normalize("   ")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            normalize(1)  # type: ignore[arg-type]

    def test_all_aliases_resolve(self):
        for alias, full in ALIASES.items():
            with self.subTest(alias=alias):
                self.assertEqual(normalize(alias), full)


class CapitalTests(unittest.TestCase):
    def test_guangdong(self):
        self.assertEqual(capital_of("广东"), "广州")

    def test_hebei(self):
        self.assertEqual(capital_of("河北省"), "石家庄")

    def test_inner_mongolia(self):
        self.assertEqual(capital_of("内蒙古"), "呼和浩特")

    def test_taiwan(self):
        self.assertEqual(capital_of("台湾"), "台北")

    def test_unknown(self):
        with self.assertRaises(ValueError):
            capital_of("火星省")

    def test_every_province_has_queryable_capital(self):
        for province in PROVINCES:
            with self.subTest(province=province.name):
                self.assertEqual(capital_of(province.name), province.capital)


class ReverseTests(unittest.TestCase):
    def test_guangzhou(self):
        self.assertEqual(province_of("广州"), "广东省")

    def test_harbin(self):
        self.assertEqual(province_of("哈尔滨"), "黑龙江省")

    def test_municipality_with_suffix(self):
        self.assertEqual(province_of("北京市"), "北京市")

    def test_unknown_city(self):
        with self.assertRaises(ValueError):
            province_of("纽约")

    def test_empty(self):
        with self.assertRaises(ValueError):
            province_of("  ")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            province_of(None)  # type: ignore[arg-type]

    def test_all_capitals_reverse(self):
        for province in PROVINCES:
            with self.subTest(capital=province.capital):
                self.assertEqual(province_of(province.capital), province.name)


class RegionTests(unittest.TestCase):
    def test_region_of_guangdong(self):
        self.assertEqual(region_of("广东"), "华南")

    def test_region_of_xinjiang(self):
        self.assertEqual(region_of("新疆"), "西北")

    def test_by_region_north_china(self):
        names = [p.name for p in by_region("华北")]
        self.assertIn("北京市", names)
        self.assertIn("内蒙古自治区", names)

    def test_by_region_unknown(self):
        with self.assertRaises(ValueError):
            by_region("南极")

    def test_regions_order(self):
        self.assertEqual(regions(), list(REGIONS))

    def test_region_counts(self):
        data = stats()
        counts = data["by_region"]
        self.assertEqual(counts["华北"], 5)
        self.assertEqual(counts["东北"], 3)

    def test_total_in_stats(self):
        self.assertEqual(stats()["total"], 34)

    def test_kind_counts(self):
        kinds = stats()["by_kind"]
        self.assertEqual(kinds["直辖市"], 4)
        self.assertEqual(kinds["特别行政区"], 2)


class MatchingTests(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(make_matching(6, seed=1)), 6)

    def test_deterministic(self):
        self.assertEqual(make_matching(5, seed=2), make_matching(5, seed=2))

    def test_pairs_are_correct(self):
        for province, capital in make_matching(6, seed=3):
            self.assertEqual(capital_of(province), capital)

    def test_zero(self):
        with self.assertRaises(ValueError):
            make_matching(0)

    def test_too_many(self):
        with self.assertRaises(ValueError):
            make_matching(40)

    def test_float_count(self):
        with self.assertRaises(TypeError):
            make_matching(2.5)  # type: ignore[arg-type]


class QuizTests(unittest.TestCase):
    def test_capital_kind(self):
        questions = make_quiz(5, seed=4, kind="capital")
        self.assertEqual(len(questions), 5)
        for question in questions:
            self.assertEqual(question["answer"], capital_of(str(question["prompt"])))

    def test_province_kind(self):
        questions = make_quiz(5, seed=4, kind="province")
        for question in questions:
            self.assertEqual(question["answer"], province_of(str(question["prompt"])))

    def test_choices_four_unique(self):
        for question in make_quiz(5, seed=5):
            self.assertEqual(len(set(question["choices"])), 4)

    def test_answer_in_choices(self):
        for question in make_quiz(5, seed=5):
            self.assertIn(question["answer"], question["choices"])

    def test_invalid_kind(self):
        with self.assertRaises(ValueError):
            make_quiz(3, kind="food")

    def test_zero_count(self):
        with self.assertRaises(ValueError):
            make_quiz(0)

    def test_too_many(self):
        with self.assertRaises(ValueError):
            make_quiz(35)


class GradeTests(unittest.TestCase):
    def setUp(self):
        self.questions = make_quiz(3, seed=6)

    def test_all_correct(self):
        answers = [str(q["answer"]) for q in self.questions]
        self.assertEqual(
            grade(self.questions, answers),
            {"correct": 3, "total": 3, "score": 100},
        )

    def test_partial(self):
        answers = [str(self.questions[0]["answer"]), "错", "错"]
        self.assertEqual(grade(self.questions, answers)["correct"], 1)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            grade(self.questions, ["广州"])

    def test_empty(self):
        with self.assertRaises(ValueError):
            grade([], [])

    def test_non_string(self):
        with self.assertRaises(TypeError):
            grade(self.questions, [1, 2, 3])  # type: ignore[list-item]

    def test_strips_answers(self):
        answers = [" %s " % q["answer"] for q in self.questions]
        self.assertEqual(grade(self.questions, answers)["correct"], 3)


class InfoTests(unittest.TestCase):
    def test_info_guangdong(self):
        info = province_info("广东")
        self.assertEqual(info.name, "广东省")
        self.assertEqual(info.capital, "广州")
        self.assertEqual(info.kind, "省")

    def test_info_hong_kong(self):
        info = province_info("香港")
        self.assertEqual(info.kind, "特别行政区")

    def test_info_unknown(self):
        with self.assertRaises(ValueError):
            province_info(" Atlantis ")


if __name__ == "__main__":
    unittest.main()
