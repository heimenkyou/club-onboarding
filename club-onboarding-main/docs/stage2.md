# 任务二：安装并配置 Git

目标：装好 Git、配置自己的身份，然后把任务二的记录用**新分支**提交上来。

| 项目 | 要求 |
| --- | --- |
| 提交文件 | `students/学号-姓名/stage2.md` |
| 分支名 | `stage2/学号` |
| commit message | 建议 `[Stage2] 学号-姓名` |
| PR 标题 | `[Stage2] 专业班级-姓名-学号` |
| PR 描述 | `本地最新 commit hash：<粘贴>` |

## 1. 安装 Git

- **Windows**：下载 <https://git-scm.com/download/win>，一路默认安装即可。
- **macOS**：终端执行 `xcode-select --install`，或 `brew install git`。
- **Linux**：`sudo apt install git`（Debian/Ubuntu），或使用对应发行版的包管理器。

装完打开一个**新的**终端窗口，验证：

```bash
git --version
```

能输出版本号（例如 `git version 2.43.0`）就说明装好了。

## 2. 配置身份

Git 每次 commit 都会记录作者，所以必须先配好：

```bash
git config --global user.name "张三"
git config --global user.email "你的邮箱@example.com"
```

建议 `user.name` 用真实姓名，`user.email` 用你注册 GitHub 的邮箱（这样 GitHub 才能把 commit 认成你的）。

检查是否生效：

```bash
git config user.name
git config user.email
```

> 这两条命令的输出，就是后面 `stage2.md` 里要填的内容。

## 3. clone 你自己的 fork

```bash
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名
```

注意 clone 的是**你的 fork**，不是主仓库，否则你没有推送权限。

## 4. 新建分支 `stage2/学号`

```bash
git switch main
git pull
git switch -c stage2/20260000001
```

`-c` 表示新建并切换。用 `git branch` 确认当前已在 `stage2/20260000001` 上。

## 5. 新建 `students/学号-姓名/stage2.md`

文件内容（把命令的真实输出填进去）：

```markdown
姓名：张三
学号：20260000001
专业班级：计算机科学与技术 2026 级 1 班
git --version：git version 2.43.0
git config user.name：张三
git config user.email：zhangsan@example.com
```

要求：

- 六个字段都要有，不能空着。
- `git --version` 要填**命令的真实输出**，不能只写 `2.43.0`。
- 姓名、学号必须和文件夹名一致。

## 6. 提交并推送

```bash
git add "students/20260000001-张三/stage2.md"
git commit -m "[Stage2] 20260000001-张三"
git push -u origin HEAD
```

第一次推送新分支时用 `git push -u origin HEAD`，它会把本地分支和远端同名分支关联起来。

## 7. 拿到 commit hash

推送之后执行：

```bash
git log -1 --format=%H
```

会得到一串 40 位的十六进制字符，例如：

```text
a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

这就是 PR 描述里要填的“本地最新 commit hash”。

> 要在 **commit 之后**再执行。如果之后又提交了新的 commit，记得重新取一次。

## 8. 开 PR

1. 主仓库 → **Pull requests** → **New pull request** → **compare across forks**。
2. base：主仓库 `main`；head：你的 fork，compare 分支选 `stage2/20260000001`。
3. 标题：`[Stage2] 计算机科学与技术 2026 级 1 班-张三-20260000001`
4. 描述：

```text
本地最新 commit hash：a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

## 提交前检查

- [ ] `git --version` 能正常运行
- [ ] `git config user.name` / `user.email` 有值，且和 `stage2.md` 里写的一致
- [ ] 分支名是 `stage2/学号`
- [ ] PR 的 head 分支选的是 `stage2/学号`，不是 `main`
- [ ] 改动只有 `stage2.md`，没有顺手改别的文件
- [ ] PR 描述里有完整的 40 位 commit hash
