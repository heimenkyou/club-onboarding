# 社团新人入门任务

欢迎加入！这是给新同学准备的三道入门任务：从第一次提 PR 开始，一步步把 Git 和 Python 环境配好。

任务不难，**也不要求全部做完**——尽力完成自己能完成的部分就行。卡住了就去查资料、问 AI，或者在群里问学长。

## 开始之前：先把文档看舒服

这些文档是 Markdown 格式，用记事本打开只会看到一堆 `#`、`**`、`|`，完全看不出结构。强烈建议先花几分钟装好 VS Code，用它来阅读：

1. 下载安装 VS Code：<https://code.visualstudio.com/>，一路默认下一步即可。
   （想要中文界面：打开后按 `Ctrl + Shift + X`，搜索 `Chinese (Simplified)` 安装并重启。）
2. 把项目弄到本地，二选一：
   - 已经装了 Git：`git clone https://github.com/heimenkyou/club-onboarding`
   - 还没装 Git：在 GitHub 仓库页点绿色的 **Code** → **Download ZIP**，解压到任意文件夹。
3. 打开 VS Code，点 **File → Open Folder**（文件 → 打开文件夹），选中 `club-onboarding` 这个文件夹。
4. 在左侧点开 `README.md`，然后点编辑器**右上角的预览按钮**（图标像“放大镜 + 文档分栏”，不同版本位置略有差异），或者直接按 `Ctrl + Shift + V`，就能看到排版好的文档。
   - 想左边写、右边实时预览：先按 `Ctrl + K`，再按 `V`。
5. 后面的 `docs/stage1.md`、`docs/stage2.md`、`docs/stage3.md` 也都这样预览着看。

> 其实在 GitHub 网页上打开仓库首页，README 也是渲染好的，可以直接读；但本地预览方便你一边看一边改文件。

---

## 任务一览

| 任务 | 内容 | 需要提交的文件 | PR 标题 |
| :--: | --- | --- | --- |
| 一 | 第一次 PR | `students/学号-姓名/stage1.md` | `[Stage1] 学号-姓名` |
| 二 | 安装 Git、配置身份、用分支提交 | `students/学号-姓名/stage2.md` | `[Stage2] 专业班级-姓名-学号` |
| 三 | 安装 Python、运行脚本生成挑战码 | `students/学号-姓名/stage3/result.txt` | `[Stage3] 专业班级-姓名-学号` |

详细步骤：

- [任务一：第一次 PR](docs/stage1.md)
- [任务二：安装并配置 Git](docs/stage2.md)
- [任务三：安装 Python，生成挑战码](docs/stage3.md)

## 通用规则

1. **先建自己的文件夹**：`students/学号-姓名/`，例如 `students/20260000001-张三/`。
   学号在前、姓名在后，中间是一个英文短横线 `-`，不要空格。
2. **只改自己的文件夹**。别人的文件、根目录的 `task3.py` 和 `verify.py` 都不要动。
3. **一个任务一个 PR**，不要把三道题塞进同一个 PR。
4. PR 里的改动应该只有你这个任务相关的文件。发现自己改了别的文件，先改回去。
5. 路径和文件名必须和文档完全一致，大小写也要一致。
6. 提交前跑一下 `git status`，确认没有把密码、token 之类的文件提上来。

## 仓库结构

```text
.
├── README.md                  ← 你正在看的文件
├── docs/
│   ├── stage1.md              ← 任务一的详细步骤
│   ├── stage2.md              ← 任务二的详细步骤
│   └── stage3.md              ← 任务三的详细步骤
├── students/
│   ├── README.md              ← 个人文件夹的命名规则
│   └── 20260000001-张三/       ← 每个人一个文件夹（这里是格式示例）
│       ├── stage1.md
│       ├── stage2.md
│       └── stage3/
│           └── result.txt
├── task3.py                   ← 任务三用，直接运行，不要修改
└── verify.py                  ← 维护者检查用，同学不用管
```

## 怎么算通过

- 每个任务单独看，**完成一个算一个**。
- 维护者会在合并前跑 `python verify.py`，检查字段是否齐全、姓名学号是否和文件夹名匹配、挑战码是否由 `task3.py` 真实生成。
- 任务一、二的小问题（比如错别字）会直接在 PR 里评论，改完再提一次 commit 就行。
- 任务三的挑战码**每个人都不一样**，抄别人的结果文件会被查出来。

## 常见问题

**Q：我不会用命令行，命令在哪敲？**
在项目文件夹里右键 → 在终端中打开（Windows 11），或者用 VS Code 打开项目后按 `Ctrl` + 反引号键（键盘左上角 `Esc` 下面那个）打开内置终端。

**Q：`git push` 让我登录，密码是什么？**
GitHub 已经不支持用账号密码推送。Windows 安装 Git 时自带 Git Credential Manager，一般会弹浏览器让你授权；如果命令行要求输入密码，请使用 Personal Access Token，而不是账号密码。

**Q：Fork 之后主仓库又更新了，需要同步吗？**
不需要。你的 PR 只和你改的文件有关。

**Q：任务一为什么不用新建分支？**
任务一就是练习“从 fork 的默认分支直接提 PR”这条最简单的路径。从任务二开始才要求新建分支。

**Q：任务二/三建分支时，该从哪个分支切出来？**
从 fork 的默认分支（一般是 `main`）切。先 `git switch main`、`git pull`，再 `git switch -c stage2/学号`。

**Q：我忘了建分支，直接在主分支上改了怎么办？**
不用慌，改动还在。执行 `git switch -c stage2/学号` 新建分支，未提交的改动会自动带过去。

**Q：任务二的 PR 还没合并，能不能先做任务三？**
可以。任务三也从 `main` 切分支，两个 PR 的改动互不干扰。前一个合并后再 `git pull` 更新本地 `main` 即可。

**Q：提交后发现写错了怎么办？**
直接改文件，再 `git add` + `git commit` + `git push`，PR 会自动更新，不需要关掉重开。

**Q：终端里中文显示成乱码？**
Windows 上先执行 `chcp 65001` 切换到 UTF-8，或者直接用 Windows Terminal / VS Code 的终端。

**Q：`python` 提示“不是内部或外部命令”？**
安装 Python 时没勾选 “Add python.exe to PATH”。重新运行安装包选 Modify 勾上，或者手动把 Python 加进环境变量。

**Q：任务三的脚本会改我别的文件吗？**
不会。它只会在 `students/学号-姓名/stage3/` 下创建一个 `result.txt`。

## 维护者：怎么检查提交

```bash
python verify.py                       # 检查 students/ 下所有人
python verify.py students/20260000001-张三   # 只检查一个人
python verify.py --json                # 机器可读输出
```

脚本会逐项检查 `stage1.md`、`stage2.md`、`stage3/result.txt`：

- 字段是否齐全、是否为空；
- 姓名、学号是否和文件夹名 `学号-姓名` 一致；
- 任务二的 git 版本、邮箱格式是否像真实输出；
- 任务三的挑战码是否能用同样的算法重新算出来（手改过的文件会失败）。

未提交的任务不算失败，退出码为 `0`；只要有一项检查不通过，退出码为 `1`，方便以后接 CI。

## 学习资源

- Git 官方文档（中文）：<https://git-scm.com/book/zh/v2>
- GitHub Skills（交互式练习）：<https://skills.github.com/>
- 廖雪峰 Git 教程：<https://www.liaoxuefeng.com/wiki/896043488029600>
- Python 官方教程（中文）：<https://docs.python.org/zh-cn/3/tutorial/>
- B 站搜索关键词：`git 使用教程`、`github 使用教程`、`python 安装教程`、`提交 PR`

> 搜索引擎和 AI 是正经工具，不是作弊。遇到报错，**把完整的报错信息贴进去搜**，比只搜“git 报错”有效得多。
