import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.md",
    "fundamentals.md",
    "exams/course-selection.md",
    "exams/classes-and-notes.md",
    "exams/final-review.md",
    "learning/english.md",
    "learning/finding-courses.md",
    "admission/information.md",
    "admission/written-test.md",
    "admission/interview.md",
    "admission/cases.md",
    "courses/calculus.md",
    "courses/linear-algebra.md",
    "courses/other-courses.md",
)


class SiteStructureTest(unittest.TestCase):
    def test_expected_pages_exist_and_have_one_title(self):
        for relative_path in PAGES:
            text = (ROOT / "docs" / relative_path).read_text(encoding="utf-8")
            self.assertEqual(1, sum(line.startswith("# ") for line in text.splitlines()))

    def test_config_uses_chinese_classic_theme_and_all_pages(self):
        config = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))
        project = config["project"]
        self.assertEqual("zh", project["theme"]["language"])
        self.assertEqual("classic", project["theme"]["variant"])
        self.assertEqual("site", project["site_dir"])
        nav_text = str(project["nav"])
        for relative_path in PAGES:
            self.assertIn(relative_path, nav_text)

    def test_internal_project_docs_are_excluded_from_the_site(self):
        config = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))
        exclude_docs = config["project"]["exclude_docs"]
        self.assertIsInstance(exclude_docs, str)
        self.assertIn("superpowers/", exclude_docs.splitlines())

    def test_github_pages_deployment_is_configured(self):
        config = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))
        self.assertEqual(
            "https://kiraakashi6666.github.io/whut-math-postgraduate-guide/",
            config["project"]["site_url"],
        )
        workflow = (ROOT / ".github/workflows/docs.yml").read_text(encoding="utf-8")
        self.assertIn("zensical build --clean", workflow)
        self.assertIn("actions/deploy-pages@v5", workflow)

    def test_content_has_no_notion_links_or_missing_local_images(self):
        for relative_path in PAGES:
            page = ROOT / "docs" / relative_path
            text = page.read_text(encoding="utf-8")
            self.assertNotIn("app.notion.com", text)
            for target in re.findall(r"!\[[^]]*\]\(([^)]+)\)", text):
                if "://" not in target:
                    self.assertTrue((page.parent / target).resolve().exists(), target)


if __name__ == "__main__":
    unittest.main()
