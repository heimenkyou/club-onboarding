# 任务三：安装 Python，生成你的挑战码

目标：装好 Python，运行仓库里的 `task3.py`。脚本会根据你的姓名和学号生成一个**只属于你**的挑战码，并写进结果文件。

| 项目 | 要求 |
| --- | --- |
| 提交文件 | `students/学号-姓名/stage3/result.txt` |
| 分支名 | `stage3/学号` |
| commit message | `[Stage3] 学号 姓名` |
| PR 标题 | `[Stage3] 专业班级-姓名-学号` |
| PR 描述 | 贴一下你的挑战码 |

## 1. 安装 Python

- **Windows**：下载 <https://www.python.org/downloads/>，安装时**务必勾选 “Add python.exe to PATH”**。
- **macOS**：`brew install python`，或从官网下载安装包。
- **Linux**：`sudo apt install python3`（多数发行版已自带）。

装完**重新打开终端**，验证：

```bash
python --version
```

macOS / Linux 上可能需要用 `python3 --version`。能看到 `Python 3.x.x` 就说明好了。

## 2. 运行 `task3.py`

先确保在仓库根目录（也就是能看到 `task3.py` 的那一层）：

```bash
git switch main
git pull
python task3.py
```

Windows 上如果 `python` 不行，试试 `py task3.py`；macOS / Linux 用 `python3 task3.py`。

按提示输入：

```text
姓名：张三
学号：20260000001
```

脚本会自动创建 `students/20260000001-张三/stage3/result.txt`，内容大致如下：

```text
# 社团入门任务 · Stage 3
（本文件由 task3.py 自动生成，请勿手动修改）

姓名：张三
学号：20260000001
时间戳：1760000000
生成时间：2026-10-20 12:34:56 (UTC+08:00)
Python：3.12.4
平台：Windows-11-10.0.22631-SP0

挑战码：ABCD-EFGH-IJKL-MNOP
```

> `result.txt` 是脚本写的，**不要手改**。改了挑战码就对不上，检查会不通过。
> 每个人生成的挑战码都不同，同一个人不同时间运行也会不同，这是正常的。

## 3. 建分支并提交

```bash
git switch -c stage3/20260000001
git add "students/20260000001-张三/stage3/result.txt"
git commit -m "[Stage3] 20260000001 张三"
git push -u origin HEAD
```

## 4. 开 PR

1. 主仓库 → **Pull requests** → **New pull request** → **compare across forks**。
2. base：主仓库 `main`；head：你的 fork，compare 分支选 `stage3/20260000001`。
3. 标题：`[Stage3] 计算机科学与技术 2026 级 1 班-张三-20260000001`
4. 描述里贴一下挑战码：

```text
挑战码：ABCD-EFGH-IJKL-MNOP
```

## 提交前检查

- [ ] `python --version` 能正常输出
- [ ] `students/学号-姓名/stage3/result.txt` 存在，且是脚本生成的（没有手改）
- [ ] 分支名是 `stage3/学号`
- [ ] commit message 是 `[Stage3] 学号 姓名`
- [ ] PR 标题是 `[Stage3] 专业班级-姓名-学号`
- [ ] PR 里只有 `stage3/result.txt` 这一个新增文件
