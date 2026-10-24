# 任务一：第一次 PR

目标：把一份自我介绍，通过 Pull Request 的形式提交到这个仓库。这是你在这个社团留下的第一个 commit。

| 项目 | 要求 |
| --- | --- |
| 提交文件 | `students/学号-姓名/stage1.md` |
| commit message | `[Stage1] 学号-姓名` |
| PR 标题 | `[Stage1] 学号-姓名` |
| PR 描述 | 随意，一句话即可 |
| head 分支 | 你 fork 仓库的默认分支（一般是 `main`） |

> 本文示例统一用 `20260000001-张三`，请换成你自己的学号和姓名（中文姓名直接写中文）。

## 1. Fork 主仓库

打开主仓库页面，点右上角的 **Fork** → **Create fork**。

完成后你会有一个自己的副本：`https://github.com/你的用户名/仓库名`。后面所有改动都提交到这个副本上。

## 2. 新建个人文件夹

两条路，选一条就行。

### A. 网页操作（不用装任何东西）

1. 在你的 fork 页面点 **Add file** → **Create new file**。
2. 文件名输入：`students/20260000001-张三/stage1.md`
   输入 `/` 的时候 GitHub 会自动把前面部分变成目录。
3. 在下面的大输入框里写内容（见第 3 步）。

### B. 命令行

```bash
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名
mkdir -p "students/20260000001-张三"
```

Windows PowerShell 里 `mkdir` 同样可用；路径含中文时记得加引号。

## 3. 写 `stage1.md`

内容就是五行，每行一个字段：

```markdown
姓名：张三
学号：20260000001
专业班级：计算机科学与技术 2026 级 1 班
为什么想加入：想在社团里学点真东西，也认识一些一起折腾的同学。
遇到问题一般怎么查：先看报错信息，再搜官方文档和搜索引擎，实在不行问 AI 或群里问学长。
```

要求：

- 五个字段都要有，**不能空着**。
- 冒号用中文 `：` 或英文 `:` 都可以。
- 姓名、学号必须和文件夹名一致。
- 文件用 UTF-8 编码保存（网页编辑不用管，默认就是）。

## 4. 提交

**网页操作**：页面下方填 commit message：

```text
[Stage1] 学号-姓名
```

例如 `[Stage1] 20260000001-张三`，然后点 **Commit changes**，提交到 `main` 分支。

**命令行**：

```bash
git add "students/20260000001-张三/stage1.md"
git commit -m "[Stage1] 20260000001-张三"
git push
```

## 5. 开 PR

1. 打开**主仓库**（不是你的 fork）的 **Pull requests** 页，点 **New pull request**。
2. 点 **compare across forks**。
3. 设置：
   - base repository：主仓库，base 分支 `main`
   - head repository：你的 fork，compare 分支 `main`
4. 标题填：`[Stage1] 20260000001-张三`
5. 描述随便写一句，比如“任务一已完成，请查收。”
6. 点 **Create pull request**。

## 提交前检查

- [ ] 改动只有 `students/学号-姓名/stage1.md` 这一个文件
- [ ] 文件名、路径完全正确（是 `stage1.md`，不是 `Stage1.md`）
- [ ] 五个字段都填了，姓名、学号和文件夹名一致
- [ ] commit message 和 PR 标题都是 `[Stage1] 学号-姓名`
- [ ] PR 的 head 分支是 fork 的默认分支 `main`
