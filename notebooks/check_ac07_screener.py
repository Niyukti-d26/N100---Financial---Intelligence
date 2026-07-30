import requests


url = "http://127.0.0.1:8000/api/v1/screener"


params = {
    "preset": "quality"
}


r = requests.get(
    url,
    params=params
)


print("Status:", r.status_code)


data = r.json()


print("Response Type:", type(data))

print("Rows Returned =", len(data))


if len(data) > 0:
    print("\nSample:")
    print(data[:3])