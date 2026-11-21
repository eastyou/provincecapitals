"""provincecapitals 命令行测试。"""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from provincecapitals.cli import main


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class LookupTests(unittest.TestCase):
    def test_capital(self):
        code, out, _ = run(["capital", "广东"])
        self.assertEqual(code, 0)
        self.assertIn("广州", out)

    def test_capital_alias(self):
        code, out, _ = run(["capital", "内蒙古"])
        self.assertEqual(code, 0)
        self.assertIn("呼和浩特", out)

    def test_capital_unknown(self):
        code, _, err = run(["capital", "火星"])
        self.assertEqual(code, 2)
        self.assertIn("未知", err)

    def test_province(self):
        code, out, _ = run(["province", "广州"])
        self.assertEqual(code, 0)
        self.assertIn("广东省", out)

    def test_province_unknown(self):
        code, _, err = run(["province", "纽约"])
        self.assertEqual(code, 2)
        self.assertIn("未找到", err)

    def test_info(self):
        code, out, _ = run(["info", "香港"])
        self.assertEqual(code, 0)
        self.assertIn("特别行政区", out)
        self.assertIn("华南", out)


class ListTests(unittest.TestCase):
    def test_list_all(self):
        code, out, _ = run(["list"])
        self.assertEqual(code, 0)
        self.assertIn("华北（5）", out)
        self.assertIn("广东省", out)

    def test_list_region(self):
        code, out, _ = run(["list", "--region", "东北"])
        self.assertEqual(code, 0)
        self.assertIn("辽宁省", out)
        self.assertNotIn("广东省", out)

    def test_list_unknown_region(self):
        code, _, err = run(["list", "--region", "南极"])
        self.assertEqual(code, 2)
        self.assertIn("未知分区", err)

    def test_regions(self):
        code, out, _ = run(["regions"])
        self.assertEqual(code, 0)
        self.assertIn("合计：34 个", out)
        self.assertIn("东北：3 个", out)


class MatchingCommandTests(unittest.TestCase):
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "match.html"
            code, out, _ = run(["matching", "--count", "6", "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertIn("6 组", out)

    def test_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "a.html"
            second = Path(tmp) / "b.html"
            run(["matching", "--count", "5", "--seed", "8", "-o", str(first)])
            run(["matching", "--count", "5", "--seed", "8", "-o", str(second)])
            self.assertEqual(
                first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8")
            )

    def test_too_many(self):
        code, _, err = run(["matching", "--count", "40", "-o", "unused.html"])
        self.assertEqual(code, 2)
        self.assertIn("不能超过", err)


class QuizCommandTests(unittest.TestCase):
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "quiz.html"
            code, out, _ = run(["quiz", "--count", "5", "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertIn("5 题", out)

    def test_province_kind(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "quiz.html"
            run(["quiz", "--count", "4", "--kind", "province", "-o", str(output)])
            self.assertIn("哪个省级行政区", output.read_text(encoding="utf-8"))

    def test_no_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "quiz.html"
            run(["quiz", "--count", "3", "-o", str(output), "--no-answers"])
            self.assertNotIn("参考答案", output.read_text(encoding="utf-8"))

    def test_invalid_kind(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["quiz", "--kind", "food", "-o", "unused.html"])
        self.assertEqual(ctx.exception.code, 2)


class ParserTests(unittest.TestCase):
    def test_help(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stdout(io.StringIO()):
                main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_no_command(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main([])
        self.assertEqual(ctx.exception.code, 2)

    def test_unknown_command(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["map"])
        self.assertEqual(ctx.exception.code, 2)

    def test_quiz_requires_output(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["quiz", "--count", "3"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
