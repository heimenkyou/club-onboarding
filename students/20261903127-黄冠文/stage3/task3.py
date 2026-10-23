import time
import hashlib

student_id = "20261903127"
name = "黄冠文"
ts = int(time.time())

raw = f"{student_id}|{name}|{ts}"
challenge_code = hashlib.sha256(raw.encode()).hexdigest()

content = f"""学号：{student_id}
姓名：{name}
时间戳：{ts}
挑战码：{challenge_code}
"""

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 已生成 result.txt，包含时间戳！")
print(content)
