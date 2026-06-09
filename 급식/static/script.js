document.addEventListener('DOMContentLoaded', () => {
    const datePicker = document.getElementById('date-picker');
    const loader = document.getElementById('loader');
    const mealContainer = document.getElementById('meal-container');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');
    
    const menuList = document.getElementById('menu-list');
    const caloriesDisplay = document.getElementById('calories-display');

    // 현재 날짜를 기본값으로 설정
    const today = new Date();
    // 로컬 타임존 기준으로 xxxx-xx-xx 포맷 만들기
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    
    if (datePicker) {
        datePicker.value = formattedDate;
        datePicker.addEventListener('change', (e) => {
            fetchMealData(e.target.value.replace(/-/g, ''));
        });
    }

    // 데이터 가져오기
    function fetchMealData(dateStr) {
        if (!dateStr) {
            dateStr = datePicker ? datePicker.value.replace(/-/g, '') : `${year}${month}${day}`;
        }
        
        loader.classList.remove('hidden');
        mealContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');

        // 캐시를 방지하기 위해 타임스탬프 추가
        fetch(`/api/meal?date=${dateStr}&v=` + new Date().getTime())
            .then(response => response.json())
            .then(data => {
                loader.classList.add('hidden');

                if (data.success) {
                    renderMeal(data);
                } else {
                    showError(data.message);
                }
            })
            .catch(error => {
                loader.classList.add('hidden');
                showError('서버 연결에 실패했습니다.');
                console.error('Error fetching meal data:', error);
            });
    }

    // 화면 렌더링
    function renderMeal(data) {
        // 메뉴 리스트 추가
        menuList.innerHTML = '';
        data.dishes.forEach(dishInfo => {
            const li = document.createElement('li');
            
            const headerDiv = document.createElement('div');
            headerDiv.className = 'dish-header';
            headerDiv.textContent = dishInfo.name;
            li.appendChild(headerDiv);

            if (dishInfo.allergies && dishInfo.allergies.length > 0) {
                const tagsWrapper = document.createElement('div');
                tagsWrapper.className = 'dish-allergy-tags';
                
                const allergyLabel = document.createElement('span');
                allergyLabel.className = 'allergy-label';
                allergyLabel.textContent = '※ 알레르기 주의:';
                tagsWrapper.appendChild(allergyLabel);

                dishInfo.allergies.forEach(allergy => {
                    const tag = document.createElement('span');
                    tag.className = 'allergy-tag inline-tag';
                    tag.textContent = allergy;
                    tagsWrapper.appendChild(tag);
                });
                li.appendChild(tagsWrapper);
            }
            
            menuList.appendChild(li);
        });

        // 칼로리 설정
        caloriesDisplay.textContent = data.calories;
        mealContainer.classList.remove('hidden');
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.classList.remove('hidden');
    }

    // 실행
    fetchMealData();
});
