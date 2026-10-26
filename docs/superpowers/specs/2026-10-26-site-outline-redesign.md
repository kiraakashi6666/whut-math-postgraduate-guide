# 网站框架重构设计

## 目标

将公开网站重构为空白内容框架，便于作者后续逐页补充。撤下当前正文，不迁移旧内容；作者已在本地保留备份。

网站显示名称改为“WHUT 数学er 学习指南”。GitHub 仓库名和现有网址保持不变。

## 标题规则

- 导航与页面标题不显示数字编号。
- 保留作者确定的标题文字。
- 所有标题中的“WHUT”使用大写。
- 分组标题只用于导航层级，不额外创建重复的概览页面。

## 导航与文件结构

```text
首页                                      docs/index.md
引言                                      docs/introduction.md
绩点
  日常学习                                docs/gpa/daily-study.md
  课外学习                                docs/gpa/extracurricular-study.md
  期末备考                                docs/gpa/final-exam-preparation.md
保研
  三年规划                                docs/postgraduate/three-year-plan.md
  套磁
    简历                                  docs/postgraduate/recommendation/resume.md
    邮件                                  docs/postgraduate/recommendation/email.md
    和老师交流                            docs/postgraduate/recommendation/communicating.md
  笔面经验
    笔试准备                              docs/postgraduate/exams-and-interviews/written-exam.md
    面试准备                              docs/postgraduate/exams-and-interviews/interview.md
    实战案例                              docs/postgraduate/exams-and-interviews/cases.md
  其他                                    docs/postgraduate/other.md
WHUT校园生活指南
  重要地点
    校内地点                              docs/campus-life/locations/on-campus.md
    校外地点                              docs/campus-life/locations/off-campus.md
  社交
    社团                                  docs/campus-life/social/clubs.md
    活动                                  docs/campus-life/social/activities.md
  师生关系                                docs/campus-life/teacher-student-relations.md
  WHUT的网站                              docs/campus-life/websites.md
  入党                                    docs/campus-life/party-membership.md
```

## 初始页面内容

- 首页显示新网站名称、简短说明和主要栏目入口。
- 其他页面只包含对应一级标题和“内容待完善”的提示。
- 当前公开正文和不再使用的图片从最新版本中删除，不复制到新页面。

## 配置与检查

- 更新 `zensical.toml` 的站点名称、简介与完整导航。
- 更新 `README.md` 中的网站名称、目录说明和新增页面示例。
- 更新结构测试，确认全部新页面存在、标题唯一、导航完整、本地链接有效，且旧页面不再发布。
- 本地测试与 Zensical 构建通过后提交并推送至 `main`，由 GitHub Pages 自动重新发布。

## 范围边界

- 不更改仓库名和网站网址。
- 不把本地备份中的旧正文迁回网站。
- 不清理 Git 历史；旧版本仍可能通过仓库历史查看。
