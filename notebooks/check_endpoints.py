import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

endpoints = [
    "/companies/TCS",
    "/companies/TCS/pl",
    "/companies/TCS/bs",
    "/companies/TCS/cashflow",
    "/companies/TCS/ratios",
    "/companies/TCS/documents",
    "/companies/TCS/peers/compare",
    "/companies/TCS/tearsheet",
    "/portfolio/stats",
    "/screener",
    "/sectors"
]

for endpoint in endpoints:
    try:
        r = requests.get(BASE_URL + endpoint)

        print("\n" + "=" * 60)
        print(endpoint)
        print("Status:", r.status_code)

        if r.status_code == 200:
            data = r.json()

            if isinstance(data, list):
                print("Rows:", len(data))

            elif isinstance(data, dict):
                print("Keys:", list(data.keys())[:10])

            else:
                print(type(data))

        else:
            print(r.text[:500])

    except Exception as e:
        print(endpoint)
        print("ERROR:", e)