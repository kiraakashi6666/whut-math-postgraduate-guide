import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE_TITLES = {
    "index.md": "WHUT 数学er 学习指南",
    "introduction.md": "引言",
    "gpa/daily-study.md": "日常学习",
    "gpa/extracurricular-study.md": "课外学习",
    "gpa/final-exam-preparation.md": "期末备考",
    "postgraduate/must-known.md": "保研须知",
    "postgraduate/recommendation/resume.md": "简历和PPT",
    "postgraduate/recommendation/email.md": "套磁",
    "postgraduate/exams-and-interviews/written-exam.md": "笔试准备",
    "postgraduate/exams-and-interviews/interview.md": "面试准备",
    "postgraduate/exams-and-interviews/cases.md": "实战案例",
    "postgraduate/other.md": "其他",
    "campus-life/locations/on-campus.md": "校内地点",
    "campus-life/locations/off-campus.md": "校外地点",
    "campus-life/social/clubs.md": "社团",
    "campus-life/social/activities.md": "活动",
    "campus-life/teacher-student-relations.md": "师生关系",
    "campus-life/websites.md": "WHUT的网站",
    "campus-life/party-membership.md": "入党",
}
WITHDRAWN_PAGES = (
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
)


class SiteStructureTest(unittest.TestCase):
    def test_expected_pages_exist_with_exact_titles(self):
        for relative_path, title in PAGE_TITLES.items():
            text = (ROOT / "docs" / relative_path).read_text(encoding="utf-8")
            headings = [line for line in text.splitlines() if line.startswith("# ")]
            self.assertEqual([f"# {title}"], headings)

    def test_config_uses_new_name_chinese_theme_and_all_pages(self):
        config = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))
        project = config["project"]
        self.assertEqual("WHUT 数学er 学习指南", project["site_name"])
        self.assertEqual("zh", project["theme"]["language"])
        self.assertEqual("classic", project["theme"]["variant"])
        self.assertEqual("site", project["site_dir"])
        nav_text = str(project["nav"])
        for relative_path in PAGE_TITLES:
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
        for relative_path in PAGE_TITLES:
            page = ROOT / "docs" / relative_path
            text = page.read_text(encoding="utf-8")
            self.assertNotIn("app.notion.com", text)
            for target in re.findall(r"!\[[^]]*\]\(([^)]+)\)", text):
                if "://" not in target:
                    self.assertTrue((page.parent / target).resolve().exists(), target)

    def test_local_markdown_links_exist(self):
        for relative_path in PAGE_TITLES:
            page = ROOT / "docs" / relative_path
            text = page.read_text(encoding="utf-8")
            for target in re.findall(r"(?<!!)\[[^]]*\]\(([^)]+\.md)(?:#[^)]+)?\)", text):
                self.assertTrue((page.parent / target).resolve().exists(), target)

    def test_old_articles_and_asset_are_withdrawn(self):
        for relative_path in WITHDRAWN_PAGES:
            self.assertFalse((ROOT / "docs" / relative_path).exists(), relative_path)
        self.assertFalse((ROOT / "docs/assets/campus-course-review.png").exists())


if __name__ == "__main__":
    unittest.main()
