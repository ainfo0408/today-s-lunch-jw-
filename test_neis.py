import requests

url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
params = {
    'Type': 'json',
    'ATPT_OFCDC_SC_CODE': 'B10',
    'SD_SCHUL_CODE': '7010703',
    'MLSV_YMD': '20260609'
}

response = requests.get(url, params=params)
print("Status:", response.status_code)
print("Content:", response.text)
