# Site Outline Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current public articles with an empty Markdown framework using the approved unnumbered titles and rename the displayed site to “WHUT 数学er 学习指南”.

**Architecture:** Keep Zensical as the static-site generator and `zensical.toml` as the single navigation source. Each writable leaf topic is one Markdown file; grouping titles exist only in navigation. Structure tests define the required pages, exact titles, withdrawn pages, local-link validity, and publishing configuration.

**Tech Stack:** Markdown, Zensical, TOML, Python `unittest`, GitHub Actions, GitHub Pages

## Global Constraints

- Display name must be exactly `WHUT 数学er 学习指南`.
- Visible page and navigation titles must not contain numeric prefixes.
- Every occurrence of `WHUT` in an approved title must be uppercase.
- Keep the repository name and `https://kiraakashi6666.github.io/whut-math-postgraduate-guide/` unchanged.
- Do not migrate text from the author's local backup.
- Do not rewrite Git history.
- Do not create or update dependency lockfiles.

---

### Task 1: Define the New Published Structure in Tests

**Files:**
- Modify: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: approved title-to-path mapping from the design spec
- Produces: `PAGE_TITLES`, `WITHDRAWN_PAGES`, and tests that later file/config changes must satisfy

- [ ] **Step 1: Replace the old page tuple with the exact new mapping**

```python
PAGE_TITLES = {
    "index.md": "WHUT 数学er 学习指南",
    "introduction.md": "引言",
    "gpa/daily-study.md": "日常学习",
    "gpa/extracurricular-study.md": "课外学习",
    "gpa/final-exam-preparation.md": "期末备考",
    "postgraduate/three-year-plan.md": "三年规划",
    "postgraduate/recommendation/resume.md": "简历",
    "postgraduate/recommendation/email.md": "邮件",
    "postgraduate/recommendation/communicating.md": "和老师交流",
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
```

- [ ] **Step 2: Add exact-title, navigation, and withdrawal assertions**

```python
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

def test_old_articles_and_asset_are_withdrawn(self):
    for relative_path in WITHDRAWN_PAGES:
        self.assertFalse((ROOT / "docs" / relative_path).exists(), relative_path)
    self.assertFalse((ROOT / "docs/assets/campus-course-review.png").exists())
```

- [ ] **Step 3: Update the existing image and local-Markdown-link checks**

In both checks, replace iteration over the old `PAGES` tuple with:

```python
for relative_path in PAGE_TITLES:
    page = ROOT / "docs" / relative_path
```

Remove the old course-language tests because the old articles are now withdrawn in full.

- [ ] **Step 4: Run the test and verify RED**

Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_site_structure.py`.

Expected: failures for missing new pages, the old site name, and old pages that still exist.

- [ ] **Step 5: Commit the failing test**

Run `git add tests/test_site_structure.py` and `git commit --quiet -m "Test new site outline"`.

### Task 2: Replace Old Articles with the Markdown Framework

**Files:**
- Modify: `docs/index.md`
- Create: all 19 non-homepage paths in `PAGE_TITLES`
- Delete: all paths in `WITHDRAWN_PAGES`
- Delete: `docs/assets/campus-course-review.png`
- Test: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: `PAGE_TITLES` and `WITHDRAWN_PAGES`
- Produces: the complete Markdown source tree referenced by navigation

- [ ] **Step 1: Replace the homepage**

```markdown
# WHUT 数学er 学习指南

这是一份面向武汉理工大学数学与统计学院学生的学习、保研与校园生活指南，内容由作者与朋友共同整理。

网站框架正在完善，内容将陆续更新。

## 主要内容

- [引言](introduction.md)
- 绩点
- 保研
- WHUT校园生活指南
```

- [ ] **Step 2: Create each leaf page using its exact title**

Every new leaf page uses the mapped title and this exact two-block pattern:

```markdown
# 日常学习

> 内容待完善。
```

Create every path in `PAGE_TITLES` except `index.md`; substitute only the heading text.

- [ ] **Step 3: Delete the withdrawn sources and image**

Delete every file in `WITHDRAWN_PAGES` and `docs/assets/campus-course-review.png`. Do not copy any old body text into the new files.

- [ ] **Step 4: Run the structure test**

Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_site_structure.py`.

Expected: failures only for the still-old `zensical.toml` site name and navigation.

- [ ] **Step 5: Commit the Markdown framework**

Run `git add docs` and `git commit --quiet -m "Create new Markdown outline"`.

### Task 3: Update Site Configuration and Maintainer Guide

**Files:**
- Modify: `zensical.toml`
- Modify: `README.md`
- Test: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: the Markdown paths created in Task 2
- Produces: exact sidebar hierarchy and editing documentation

- [ ] **Step 1: Replace the project name, description, and navigation**

```toml
site_name = "WHUT 数学er 学习指南"
site_description = "面向武汉理工大学数学与统计学院学生的学习、保研与校园生活指南"
nav = [
  { "首页" = "index.md" },
  { "引言" = "introduction.md" },
  { "绩点" = [
    { "日常学习" = "gpa/daily-study.md" },
    { "课外学习" = "gpa/extracurricular-study.md" },
    { "期末备考" = "gpa/final-exam-preparation.md" },
  ] },
  { "保研" = [
    { "三年规划" = "postgraduate/three-year-plan.md" },
    { "套磁" = [
      { "简历" = "postgraduate/recommendation/resume.md" },
      { "邮件" = "postgraduate/recommendation/email.md" },
      { "和老师交流" = "postgraduate/recommendation/communicating.md" },
    ] },
    { "笔面经验" = [
      { "笔试准备" = "postgraduate/exams-and-interviews/written-exam.md" },
      { "面试准备" = "postgraduate/exams-and-interviews/interview.md" },
      { "实战案例" = "postgraduate/exams-and-interviews/cases.md" },
    ] },
    { "其他" = "postgraduate/other.md" },
  ] },
  { "WHUT校园生活指南" = [
    { "重要地点" = [
      { "校内地点" = "campus-life/locations/on-campus.md" },
      { "校外地点" = "campus-life/locations/off-campus.md" },
    ] },
    { "社交" = [
      { "社团" = "campus-life/social/clubs.md" },
      { "活动" = "campus-life/social/activities.md" },
    ] },
    { "师生关系" = "campus-life/teacher-student-relations.md" },
    { "WHUT的网站" = "campus-life/websites.md" },
    { "入党" = "campus-life/party-membership.md" },
  ] },
]
```

Keep `site_url`, `site_dir`, copyright, exclusions, theme, and theme features unchanged.

- [ ] **Step 2: Update `README.md` without changing the editing workflow**

Change the H1 to `# WHUT 数学er 学习指南`. Use `docs/gpa/new-topic.md` and `# 新主题` in the new-page example. Replace the content-location list with:

```markdown
- `docs/index.md`：首页。
- `docs/introduction.md`：引言。
- `docs/gpa/`：日常学习、课外学习与期末备考。
- `docs/postgraduate/`：三年规划、套磁、笔面经验与其他事项。
- `docs/campus-life/`：地点、社交、师生关系、WHUT 网站与入党。
- `zensical.toml`：网站名称、语言、外观和左侧导航。
```

Retain the environment, preview, collaboration, image, build, and test instructions.

- [ ] **Step 3: Run all tests and verify GREEN**

Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_site_structure.py`.

Expected: all tests pass.

- [ ] **Step 4: Build and check formatting**

Run `.venv/bin/zensical build --clean`, then `git diff --check`.

Expected: `No issues found`, successful build, and no whitespace errors.

- [ ] **Step 5: Commit configuration and guide changes**

Run `git add zensical.toml README.md tests/test_site_structure.py` and `git commit --quiet -m "Configure new site outline"`.

### Task 4: Publish and Verify GitHub Pages

**Files:**
- No source changes expected

**Interfaces:**
- Consumes: tested commits from Tasks 1–3
- Produces: updated `main` branch and deployed public site

- [ ] **Step 1: Verify the complete local state immediately before publishing**

Run the full unit test, `.venv/bin/zensical build --clean`, and `git status --short --branch`.

Expected: tests pass, build reports no issues, and the branch is ahead of `origin/main` only by the new commits.

- [ ] **Step 2: Push the tested commits**

Run `git push --quiet origin main` and require exit code 0.

- [ ] **Step 3: Poll the public site for the new deployment**

At `https://kiraakashi6666.github.io/whut-math-postgraduate-guide/`, verify that the page contains `WHUT 数学er 学习指南` and does not contain `WHUT 数学er保研自救指南`. Verify that `/campus-life/party-membership/` contains `入党` and that `/exams/course-selection/` is absent from the new generated site.

- [ ] **Step 4: Report publication result and history limitation**

Report the live URL, test count, successful clean build, and new outline availability. State that old content was removed from the current site and branch but remains in Git history because history rewriting was explicitly out of scope.
