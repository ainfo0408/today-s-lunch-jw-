from flask import Flask, jsonify, render_template, request
import requests
from datetime import datetime
import re
import urllib.parse

app = Flask(__name__)

ALLERGY_MAP = {
    1: '난류', 2: '우유', 3: '메밀', 4: '땅콩', 5: '대두', 
    6: '밀', 7: '고등어', 8: '게', 9: '새우', 10: '돼지고기', 
    11: '복숭아', 12: '토마토', 13: '아황산염', 14: '호두', 
    15: '닭고기', 16: '쇠고기', 17: '오징어', 18: '조개류', 19: '잣'
}



def clean_menu_string(menu_str):
    dishes = menu_str.split('<br/>')
    cleaned_dishes = []
    
    for dish in dishes:
        allergies = []
        # Extract allergy numbers (e.g., 1.2.3.)
        matches = re.findall(r'(\d+)', dish)
        for match in matches:
            num = int(match)
            if num in ALLERGY_MAP:
                allergies.append(ALLERGY_MAP[num])
                
        # Remove numbers and dots and special characters
        clean_name = re.sub(r'[\d\.]', '', dish).strip()
        clean_name = re.sub(r'[\*\(\)]', '', clean_name).strip()
        
        # Sometimes there's empty strings after cleaning
        if clean_name:
            distinct_allergies = sorted(list(set(allergies)), key=lambda x: list(ALLERGY_MAP.values()).index(x))
            cleaned_dishes.append({
                "name": clean_name,
                "allergies": distinct_allergies
            })
            
    return cleaned_dishes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/meal')
def get_meal():
    # 자운고등학교 코드
    ATPT_OFCDC_SC_CODE = 'B10'
    SD_SCHUL_CODE = '7010703'
    
    date_str = request.args.get('date')
    if date_str:
        today = date_str
    else:
        today = datetime.now().strftime('%Y%m%d')
    
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = {
        'Type': 'json',
        'ATPT_OFCDC_SC_CODE': ATPT_OFCDC_SC_CODE,
        'SD_SCHUL_CODE': SD_SCHUL_CODE,
        'MLSV_YMD': today
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'mealServiceDietInfo' in data:
            row = data['mealServiceDietInfo'][1]['row'][0]
            menu_raw = row['DDISH_NM']
            cal_info = row['CAL_INFO']
            
            cleaned_dishes = clean_menu_string(menu_raw)
            
            return jsonify({
                "success": True,
                "date": today,
                "dishes": cleaned_dishes,
                "calories": cal_info
            })
        else:
            return jsonify({
                "success": False,
                "message": "오늘은 급식이 없는 날입니다."
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "급식 정보를 불러오는 중 오류가 발생했습니다. " + str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
