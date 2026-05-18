import csv
import requests

# ============ 配置区 ============
LOGIN_URL = "https://api.claw3.ai/api/v1/user/login"
EMAIL_FILE = "emails.csv"          # 邮箱来源文件
OUTPUT_FILE = "tokens.csv"         # token输出文件
TOKEN_COUNT = 90                    # 要生成的token数量，0表示全部
CODE = "888888"                    # 验证码
SEND_TOKEN = "optional-provider-token"
# ================================

def login(email: str) -> dict:
    payload = {
        "email": email,
        "code": CODE,
        "sendToken": SEND_TOKEN
    }
    resp = requests.post(LOGIN_URL, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def extract_token(resp_json: dict) -> str:
    # 尝试常见的响应结构
    if "token" in resp_json:
        return resp_json["token"]
    if "data" in resp_json and isinstance(resp_json["data"], dict):
        if "token" in resp_json["data"]:
            return resp_json["data"]["token"]
    # 如果都没找到，打印响应让用户确认
    raise ValueError(f"无法从响应中提取token: {resp_json}")


def main():
    # 读取邮箱
    emails = []
    with open(EMAIL_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emails.append(row["email"])

    # 按配置截取数量
    if TOKEN_COUNT > 0:
        emails = emails[:TOKEN_COUNT]

    print(f"共需处理 {len(emails)} 个邮箱")

    # 逐个登录并收集token
    results = []
    for i, email in enumerate(emails):
        try:
            resp_json = login(email)
            token = extract_token(resp_json)
            results.append({"email": email, "token": token})
            print(f"[{i+1}/{len(emails)}] {email} -> 成功")
        except Exception as e:
            print(f"[{i+1}/{len(emails)}] {email} -> 失败: {e}")

    # 写入output
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "token"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n完成！成功获取 {len(results)} 个token，已写入 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
