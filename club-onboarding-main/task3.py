#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""社团入门任务 · Stage 3 · 挑战码生成器

用法（一般只需要这一条）：

    python task3.py

脚本会依次询问姓名和学号，然后在

    students/<学号>-<姓名>/stage3/result.txt

生成结果文件，里面包含一个只属于你的挑战码。

注意：

* 不要修改本文件里的 SECRET，也不要手改生成的结果文件，
  否则挑战码校验不通过（维护者会用 verify.py 检查）。
* 同一个人不同时间运行，得到的挑战码也不同，这是正常的。
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import platform
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# 计算挑战码用的固定盐值。
# 一旦修改，所有已经生成的结果文件都会失效，所以不要动它。
SECRET = b"club-onboarding-2026-stage3-v1"

BASE_DIR = Path(__file__).resolve().parent
STUDENTS_DIR = BASE_DIR / "students"

# 文件名里不允许出现的字符（Windows 的限制，顺便挡掉路径穿越）
ILLEGAL_CHARS = re.compile(r'[\\/:*?"<>|\r\n\t]')
SID_PATTERN = re.compile(r"^[0-9A-Za-z_-]{4,32}$")


def build_code(name: str, sid: str, timestamp: int) -> str:
    """根据 姓名 + 学号 + 时间戳 计算挑战码，格式为 XXXX-XXXX-XXXX-XXXX。"""
    payload = f"{name}|{sid}|{timestamp}".encode("utf-8")
    digest = hmac.new(SECRET, payload, hashlib.sha256).digest()
    raw = base64.b32encode(digest).decode("ascii").rstrip("=")[:16]
    return "-".join(raw[i : i + 4] for i in range(0, 16, 4))


def validate_name(raw: str) -> tuple[str, str | None]:
    name = ILLEGAL_CHARS.sub("", raw).strip()
    if not name:
        return "", "姓名不能为空"
    if len(name) > 20:
        return "", "姓名太长了，请输入真实姓名"
    if any(ch.isspace() for ch in name):
        return "", "姓名中间不要有空格"
    return name, None


def validate_sid(raw: str) -> tuple[str, str | None]:
    sid = raw.strip().replace(" ", "")
    if not sid:
        return "", "学号不能为空"
    if not SID_PATTERN.match(sid):
        return "", "学号只能是字母、数字、下划线或短横线（4-32 位）"
    return sid, None


def ask(prompt: str, validator) -> str:
    """循环提问，直到输入通过校验。"""
    while True:
        try:
            raw = input(prompt)
        except EOFError:
            print("\n没有读到输入，已退出。")
            raise SystemExit(1) from None
        value, error = validator(raw)
        if error is None:
            return value
        print(f"  × {error}，请重新输入。")


def confirm_overwrite() -> bool:
    try:
        answer = input("结果文件已存在，是否覆盖？[y/N] ").strip().lower()
    except EOFError:
        return False
    return answer in {"y", "yes"}


def render(name: str, sid: str, timestamp: int, code: str) -> str:
    local = datetime.fromtimestamp(timestamp).astimezone()
    offset = local.strftime("%z")
    offset_text = f"UTC{offset[:3]}:{offset[3:]}" if offset else "本地时间"
    return (
        "# 社团入门任务 · Stage 3\n"
        "（本文件由 task3.py 自动生成，请勿手动修改）\n"
        "\n"
        f"姓名：{name}\n"
        f"学号：{sid}\n"
        f"时间戳：{timestamp}\n"
        f"生成时间：{local.strftime('%Y-%m-%d %H:%M:%S')} ({offset_text})\n"
        f"Python：{platform.python_version()}\n"
        f"平台：{platform.platform()}\n"
        "\n"
        f"挑战码：{code}\n"
    )


def display_path(path: Path) -> str:
    try:
        return path.relative_to(BASE_DIR).as_posix()
    except ValueError:
        return str(path)


def force_utf8_output() -> None:
    """保证在 Windows 上重定向输入输出时也不会出现乱码。"""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


def main() -> int:
    force_utf8_output()
    print("=" * 58)
    print("社团入门任务 · Stage 3 · 挑战码生成器")
    print("=" * 58)
    print("按提示输入你的信息，回车确认。")
    print()

    name = ask("姓名：", validate_name)
    sid = ask("学号：", validate_sid)

    folder_name = f"{sid}-{name}"
    out_path = STUDENTS_DIR / folder_name / "stage3" / "result.txt"

    timestamp = int(time.time())
    code = build_code(name, sid, timestamp)

    print()
    print(f"姓名：{name}")
    print(f"学号：{sid}")
    print(f"挑战码：{code}")
    print()
    print(f"即将写入：{display_path(out_path)}")

    if out_path.exists() and not confirm_overwrite():
        print("已取消，没有写入任何文件。")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(name, sid, timestamp, code), encoding="utf-8")

    print("写入成功。")
    print()
    print("下一步（把学号换成你自己的）：")
    print("  git switch main")
    print("  git pull")
    print(f"  git switch -c stage3/{sid}")
    print(f'  git add "{display_path(out_path)}"')
    print(f'  git commit -m "[Stage3] {sid} {name}"')
    print("  git push -u origin HEAD")
    print()
    print("推送后到 GitHub 开 PR，标题：[Stage3] 专业班级-姓名-学号")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n已中断。")
        sys.exit(130)
