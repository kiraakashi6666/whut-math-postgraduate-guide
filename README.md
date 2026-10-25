# WHUT 数学er保研自救指南

这是一个使用 Zensical 生成的中文文档网站。正文全部保存在 `docs/` 中，可以继续使用 Markdown 修改。

## 第一次运行

在项目目录打开终端，依次运行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install zensical
zensical serve
```

然后在浏览器打开 <http://localhost:8000>。按 `Control + C` 可以停止预览服务器。

## 以后修改文章

1. 打开 `docs/` 下对应的 `.md` 文件。
2. 使用 Markdown 修改内容并保存。
3. 在项目目录运行：

   ```bash
   source .venv/bin/activate
   zensical serve
   ```

4. 浏览器中的网页会随文件保存自动更新。

## 新增文章

先在 `docs/` 的相应目录中新建 Markdown，例如：

```text
docs/courses/new-course.md
```

文件第一行写文章标题：

```markdown
# 新课程经验
```

随后在 `zensical.toml` 的 `nav` 列表中加入页面路径，页面才会出现在左侧导航中。

## 调整文章分区

- 只修改正文或增减 `##` 小标题：直接编辑对应 Markdown，不需要修改导航。
- 把文字移动到另一个现有页面：剪切到目标 Markdown，并检查原有链接。
- 新建、删除、移动或重命名 Markdown：同时修改 `zensical.toml` 中的 `nav` 路径。
- 修改完成后先运行测试和本地预览，再提交到 GitHub。

## 与协作者共同更新

每个人开始修改前先拉取远端更新，完成后提交并推送。推荐各自在独立分支修改，通过 Pull Request 合并到 `main`；合并后 GitHub Actions 会自动重新构建并发布网站。

如果两个人直接修改同一篇 Markdown 的同一位置，Git 可能要求手动解决冲突；修改不同页面通常不会互相影响。

## 插入图片

将图片放到 `docs/assets/`，然后在 Markdown 中使用相对路径：

```markdown
![图片说明](../assets/example.png)
```

不同目录中的文章可能需要调整前面的 `../` 层级。

图片文件同样使用简短、可读的英文名，例如 `campus-course-review.png`。

## 构建网站

发布或检查前运行：

```bash
source .venv/bin/activate
zensical build
```

生成的静态网页位于 `site/`。`site/`、`.venv/` 和 Python 缓存均为本地生成内容，不需要上传。

## 内容位置

- `docs/index.md`：首页。
- `docs/fundamentals.md`：保研四要素。
- `docs/exams/`：选课、听课和期末复习。
- `docs/learning/`：英语与课程资源。
- `docs/admission/`：保研笔试、面试与案例。
- `docs/courses/`：核心课程经验。
- `source/original-guide.md`：拆分前的原始文档备份。
- `zensical.toml`：网站名称、语言、外观和左侧导航。

## 自动检查

修改目录或链接后，可以运行：

```bash
python3 -m unittest tests/test_site_structure.py
```

检查会确认所有导航页面存在、中文配置正确，并检查失效的本地图片引用。
