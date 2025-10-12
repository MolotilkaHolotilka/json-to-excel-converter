import requests
import json

# URL вашего API
url = "http://localhost:8000/convert-to-excel"

# Тестовые данные (ваш пример)
test_data = {
    "data": [
        {
            "Category": "Vacuum cleaner vertical",
            "Brand": "Samsung",
            "Model": "VS20B95973B/GE",
            "Color": "",
            "DDP (RUB)": 106972,
            "Valid Until": "2025-10-01",
            "Markup Serb": 0.07,
            "Markup RU": 0.18,
            "Exchange Rate": 95.67,
            "Qty Offered": 18,
            "Date Offered": "08.10.2025",
            "Qty Ordered": 0,
            "Date Ordered": ""
        },
        {
            "Category": "Vacuum cleaner vertical",
            "Brand": "Samsung",
            "Model": "VS20B95823W/WA",
            "Color": "",
            "DDP (RUB)": 68601,
            "Valid Until": "2025-10-01",
            "Markup Serb": 0.07,
            "Markup RU": 0.18,
            "Exchange Rate": 95.67,
            "Qty Offered": 27,
            "Date Offered": "08.10.2025",
            "Qty Ordered": 0,
            "Date Ordered": ""
        },
        {
            "Category": "Vacuum cleaner vertical",
            "Brand": "Samsung",
            "Model": "VS20B75ACR5/GE",
            "Color": "",
            "DDP (RUB)": 43475,
            "Valid Until": "2025-10-01",
            "Markup Serb": 0.07,
            "Markup RU": 0.18,
            "Exchange Rate": 95.67,
            "Qty Offered": 25,
            "Date Offered": "08.10.2025",
            "Qty Ordered": 0,
            "Date Ordered": ""
        }
    ]
}

try:
    print("🚀 Отправляю запрос к API...")
    response = requests.post(url, json=test_data)
    
    if response.status_code == 200:
        # Сохраняем Excel файл
        filename = "my_export.xlsx"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Excel файл создан: {filename}")
        print(f"📊 Размер файла: {len(response.content)} байт")
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(f"Ответ: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Не удается подключиться к серверу")
    print("💡 Убедитесь, что сервер запущен: python main.py")
except Exception as e:
    print(f"❌ Ошибка: {e}")
