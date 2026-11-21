"""provincecapitals 渲染测试。"""

import unittest

from provincecapitals.model import make_matching, make_quiz
from provincecapitals.render import (
    cards_html,
    matching_html,
    matching_key_html,
    quiz_html,
    quiz_key_html,
    region_table_html,
)

PAIRS = make_matching(5, seed=1)
QUESTIONS = make_quiz(3, seed=2)


class RegionTableTests(unittest.TestCase):
    def test_contains_regions(self):
        table = region_table_html()
        self.assertIn("华北", table)
        self.assertIn("西北", table)

    def test_contains_provinces(self):
        table = region_table_html()
        self.assertIn("北京市", table)
        self.assertIn("新疆维吾尔自治区", table)

    def test_contains_capitals(self):
        self.assertIn("呼和浩特", region_table_html())


class CardsTests(unittest.TestCase):
    def test_all_provinces(self):
        cards = cards_html()
        self.assertIn("广东省", cards)
        self.assertIn("台湾省", cards)

    def test_contains_grid(self):
        self.assertIn("grid", cards_html())


class MatchingTests(unittest.TestCase):
    def test_full_document(self):
        page = matching_html(PAIRS)
        self.assertTrue(page.startswith("<!DOCTYPE html>"))
        self.assertIn("</html>", page)

    def test_contains_pairs(self):
        page = matching_html(PAIRS)
        for province, capital in PAIRS:
            self.assertIn(province, page)
            self.assertIn(capital, page)

    def test_contains_answers(self):
        self.assertIn("参考答案", matching_html(PAIRS))

    def test_can_hide_answers(self):
        page = matching_html(PAIRS, include_answers=False)
        self.assertNotIn("参考答案", page)

    def test_custom_title(self):
        page = matching_html(PAIRS, title="地理小测")
        self.assertIn("地理小测", page)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            matching_html([])

    def test_escapes_html(self):
        page = matching_html([("<b>省</b>", "<i>市</i>")])
        self.assertNotIn("<b>", page)


class QuizTests(unittest.TestCase):
    def test_full_document(self):
        page = quiz_html(QUESTIONS)
        self.assertIn("<!DOCTYPE html>", page)

    def test_contains_prompts(self):
        page = quiz_html(QUESTIONS)
        for question in QUESTIONS:
            self.assertIn(str(question["prompt"]), page)

    def test_contains_radio(self):
        self.assertIn("type=\"radio\"", quiz_html(QUESTIONS))

    def test_contains_answers(self):
        self.assertIn("参考答案", quiz_html(QUESTIONS))

    def test_can_hide_answers(self):
        self.assertNotIn("参考答案", quiz_html(QUESTIONS, include_answers=False))

    def test_province_kind_stem(self):
        questions = make_quiz(2, seed=3, kind="province")
        page = quiz_html(questions)
        self.assertIn("哪个省级行政区", page)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            quiz_html([])


class KeyTests(unittest.TestCase):
    def test_matching_key(self):
        key = matching_key_html(PAIRS)
        self.assertIn(PAIRS[0][0], key)
        self.assertIn(PAIRS[0][1], key)

    def test_matching_key_empty(self):
        with self.assertRaises(ValueError):
            matching_key_html([])

    def test_quiz_key(self):
        key = quiz_key_html(QUESTIONS)
        self.assertIn(str(QUESTIONS[0]["answer"]), key)

    def test_quiz_key_empty(self):
        with self.assertRaises(ValueError):
            quiz_key_html([])


if __name__ == "__main__":
    unittest.main()
