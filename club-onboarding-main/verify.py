#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""社团入门任务检查脚本（维护者用）

用法：

    python verify.py                       # 检查 students/ 下所有文件夹
    python verify.py students/20260000001-张三
    python verify.py students/a students/b # 检查指定文件夹
    python verify.py --json                # 输出 JSON，方便接 CI

判定规则：

    Stage 1  stage1.md 存在，五个字段齐全且非空，姓名/学号与文件夹名一致
    Stage 2  stage2.md 存在，六个字段齐全，git 版本和邮箱格式看起来正常
    Stage 3  stage3/result.txt 存在，挑战码与 姓名+学号+时间戳 重新计算的结果一致

退出码：

    0  所有已提交的检查项都通过（未提交不算失败）
    1  至少有一项检查失败
    2  用法错误或找不到目录

提示：如果同学的 PR 里只改了自己的文件夹，直接在 PR 页面点 “Checkout” 拉下来
      再跑这个脚本最省事；也可以把仓库 clone 到本地后执行。
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import re
import sys
from pathlib import Path

# 必须与 task3.py 中的 SECRET 完全一致
SECRET = b"club-onboarding-2026-stage3-v1"

BASE_DIR = Path(__file__).resolve().parent
STUDENTS_DIR = BASE_DIR / "students"

STAGE1_KEYS = ["姓名", "学号", "专业班级", "为什么想加入", "遇到问题一般怎么查"]
STAGE2_KEYS = [
    "姓名",
    "学号",
    "专业班级",
    "git --version",
    "git config user.name",
    "git config user.email",
]

KEY_LINE = re.compile(r"^\s*(?:[-*+]\s+)?([^:：]{1,40}?)\s*[:：]\s*(.*?)\s*$")
GIT_VERSION = re.compile(r"^(?:git\s+version\s+)?\d+\.\d+", re.IGNORECASE)
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

STATUS_PASS = "pass"
STATUS_FAIL = "fail"
STATUS_MISSING = "missing"

STATUS_TEXT = {
    STATUS_PASS: "[OK]",
    STATUS_FAIL: "[FAIL]",
    STATUS_MISSING: "[--]",
}


# --------------------------------------------------------------------------- #
# 挑战码（与 task3.py 保持一致）
# --------------------------------------------------------------------------- #
def build_code(name: str, sid: str, timestamp: int) -> str:
    payload = f"{name}|{sid}|{timestamp}".encode("utf-8")
    digest = hmac.new(SECRET, payload, hashlib.sha256).digest()
    raw = base64.b32encode(digest).decode("ascii").rstrip("=")[:16]
    return "-".join(raw[i : i + 4] for i in range(0, 16, 4))


# --------------------------------------------------------------------------- #
# markdown 字段解析
# --------------------------------------------------------------------------- #
def normalize_key(text: str) -> str:
    return re.sub(r"[\s`*]+", "", text).lower()


def clean_value(text: str) -> str:
    return text.strip().strip("`*").strip().strip("|").strip()


def parse_fields(text: str) -> dict[str, str]:
    """把 “键：值” 形式的行（也支持 - 列表和 markdown 表格）解析成字典。"""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        pairs: list[tuple[str, str]] = []
        if line.startswith("|") and line.endswith("|") and line.count("|") >= 3:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            body = "".join(cells)
            if len(cells) >= 2 and body and not set(body) <= set("-: "):
                pairs.append((cells[0], " ".join(cells[1:])))
        else:
            match = KEY_LINE.match(line)
            if match:
                pairs.append((match.group(1), match.group(2)))

        for key, value in pairs:
            key = normalize_key(key)
            if key and key not in fields:
                fields[key] = clean_value(value)
    return fields


def get(fields: dict[str, str], key: str) -> str:
    return fields.get(normalize_key(key), "")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


# --------------------------------------------------------------------------- #
# 各项检查
# --------------------------------------------------------------------------- #
def check_identity(folder: Path, name: str, sid: str) -> list[str]:
    """姓名、学号是否与文件夹名 “学号-姓名” 一致。"""
    expected_sid, sep, expected_name = folder.name.partition("-")
    if not sep or not expected_sid or not expected_name:
        return [f"文件夹名不符合 “学号-姓名” 格式：{folder.name}"]

    problems = []
    if sid and sid != expected_sid:
        problems.append(f"学号 “{sid}” 与文件夹名里的 “{expected_sid}” 不一致")
    if name and name != expected_name:
        problems.append(f"姓名 “{name}” 与文件夹名里的 “{expected_name}” 不一致")
    return problems


def check_stage1(folder: Path) -> tuple[str, list[str]]:
    path = folder / "stage1.md"
    if not path.is_file():
        return STATUS_MISSING, []

    fields = parse_fields(read_text(path))
    problems = [f"缺少字段或内容为空：{key}" for key in STAGE1_KEYS if not get(fields, key)]
    problems += check_identity(folder, get(fields, "姓名"), get(fields, "学号"))

    if problems and not fields:
        problems.append("没有解析到任何字段，请确认文件是 UTF-8 编码、格式为 “字段：内容”")
    return (STATUS_FAIL if problems else STATUS_PASS), problems


def check_stage2(folder: Path) -> tuple[str, list[str]]:
    path = folder / "stage2.md"
    if not path.is_file():
        return STATUS_MISSING, []

    fields = parse_fields(read_text(path))
    problems = [f"缺少字段或内容为空：{key}" for key in STAGE2_KEYS if not get(fields, key)]

    version = get(fields, "git --version")
    if version and not GIT_VERSION.match(version):
        problems.append(f"git --version 看起来不是命令输出：“{version}”")

    email = get(fields, "git config user.email")
    if email and not EMAIL.match(email):
        problems.append(f"邮箱格式看起来不对：“{email}”")

    problems += check_identity(folder, get(fields, "姓名"), get(fields, "学号"))

    if problems and not fields:
        problems.append("没有解析到任何字段，请确认文件是 UTF-8 编码、格式为 “字段：内容”")
    return (STATUS_FAIL if problems else STATUS_PASS), problems


def check_stage3(folder: Path) -> tuple[str, list[str]]:
    path = folder / "stage3" / "result.txt"
    if not path.is_file():
        return STATUS_MISSING, []

    fields = parse_fields(read_text(path))
    problems: list[str] = []

    name = get(fields, "姓名")
    sid = get(fields, "学号")
    timestamp = get(fields, "时间戳")
    code = get(fields, "挑战码")

    if not name:
        problems.append("缺少字段：姓名")
    if not sid:
        problems.append("缺少字段：学号")
    if not timestamp:
        problems.append("缺少字段：时间戳（请重新运行 task3.py，不要手写）")
    elif not timestamp.isdigit():
        problems.append(f"时间戳不是整数：“{timestamp}”")
    if not code:
        problems.append("缺少字段：挑战码")

    if name and sid and timestamp.isdigit() and code:
        expected = build_code(name, sid, int(timestamp))
        actual = re.sub(r"[^0-9A-Za-z]", "", code).upper()
        if actual != expected.replace("-", ""):
            problems.append("挑战码校验失败（文件可能被手改过，请重新运行 task3.py）")

    problems += check_identity(folder, name, sid)
    return (STATUS_FAIL if problems else STATUS_PASS), problems


CHECKERS = [
    ("Stage 1", "stage1.md", check_stage1),
    ("Stage 2", "stage2.md", check_stage2),
    ("Stage 3", "stage3/result.txt", check_stage3),
]


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #
def collect(arguments: list[str]) -> tuple[list[Path], str | None]:
    if arguments:
        folders = [Path(arg) for arg in arguments]
        for folder in folders:
            if not folder.is_dir():
                return [], f"目录不存在：{folder}"
        return folders, None

    if not STUDENTS_DIR.is_dir():
        return [], f"找不到目录：{STUDENTS_DIR}"

    folders = sorted(
        item
        for item in STUDENTS_DIR.iterdir()
        if item.is_dir() and not item.name.startswith(".") and item.name != "__pycache__"
    )
    return folders, None


def run(folders: list[Path]) -> list[dict]:
    results = []
    for folder in folders:
        stages = []
        for label, relative, checker in CHECKERS:
            status, problems = checker(folder)
            stages.append(
                {
                    "stage": label,
                    "file": relative,
                    "status": status,
                    "problems": problems,
                }
            )
        results.append({"folder": folder.as_posix(), "name": folder.name, "stages": stages})
    return results


def print_report(results: list[dict]) -> None:
    if not results:
        print("students/ 下还没有任何同学文件夹。")
        return

    for result in results:
        print(result["name"])
        for stage in result["stages"]:
            marker = STATUS_TEXT[stage["status"]]
            prefix = f"  {stage['stage']:<7} {marker:<6}"
            if stage["status"] == STATUS_MISSING:
                print(f"{prefix} 未提交 {stage['file']}")
                continue
            print(f"{prefix} {stage['file']}")
            for problem in stage["problems"]:
                print(f"         - {problem}")
        print()

    total = len(results)
    counts = {label: {STATUS_PASS: 0, STATUS_FAIL: 0, STATUS_MISSING: 0} for label, _, _ in CHECKERS}
    for result in results:
        for stage in result["stages"]:
            counts[stage["stage"]][stage["status"]] += 1

    print("=" * 58)
    print(f"共检查 {total} 个文件夹")
    for label, _, _ in CHECKERS:
        c = counts[label]
        print(
            f"  {label}：通过 {c[STATUS_PASS]} / 失败 {c[STATUS_FAIL]}"
            f" / 未提交 {c[STATUS_MISSING]}"
        )

    failed = sum(1 for result in results for stage in result["stages"] if stage["status"] == STATUS_FAIL)
    if failed:
        print(f"发现 {failed} 个失败项，需要同学修改。")
    else:
        print("所有已提交的内容都通过了检查。")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="检查社团入门任务的提交情况")
    parser.add_argument("folders", nargs="*", help="要检查的学生文件夹，默认检查 students/ 下全部")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    folders, error = collect(args.folders)
    if error:
        print(error, file=sys.stderr)
        return 2

    results = run(folders)

    if args.json:
        print(json.dumps({"students": results}, ensure_ascii=False, indent=2))
    else:
        print_report(results)

    has_failure = any(
        stage["status"] == STATUS_FAIL for result in results for stage in result["stages"]
    )
    return 1 if has_failure else 0


if __name__ == "__main__":
    sys.exit(main())
