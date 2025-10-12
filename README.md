# JSON to Excel Converter API

FastAPI приложение для конвертации JSON данных в красиво отформатированные Excel файлы.

## Возможности

- Прием JSON данных через POST запрос
- Автоматическое создание Excel файла с красивым форматированием
- Автоматическая настройка ширины колонок
- Заморозка заголовков
- Стилизованные заголовки с цветом и границами
- Автоматическое именование файлов с временной меткой

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
python main.py
```

Или с помощью uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Использование

### Запуск сервера
После запуска сервер будет доступен по адресу: `http://localhost:8000`

### API Endpoints

#### GET /
Получить информацию о API и примеры использования.

#### POST /convert-to-excel
Конвертировать JSON данные в Excel файл.

**Тело запроса:**
```json
{
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
    }
  ]
}
```

**Ответ:** Excel файл (.xlsx)

### Пример использования с curl

```bash
curl -X POST "http://localhost:8000/convert-to-excel" \
     -H "Content-Type: application/json" \
     -d '{
       "data": [
         {
           "Category": "Vacuum cleaner vertical",
           "Brand": "Samsung",
           "Model": "VS20B95973B/GE",
           "DDP (RUB)": 106972,
           "Valid Until": "2025-10-01"
         }
       ]
     }' \
     --output "export.xlsx"
```

### Пример использования с Python requests

```python
import requests

url = "http://localhost:8000/convert-to-excel"
data = {
    "data": [
        {
            "Category": "Vacuum cleaner vertical",
            "Brand": "Samsung",
            "Model": "VS20B95973B/GE",
            "DDP (RUB)": 106972,
            "Valid Until": "2025-10-01"
        }
    ]
}

response = requests.post(url, json=data)
if response.status_code == 200:
    with open("export.xlsx", "wb") as f:
        f.write(response.content)
    print("Excel файл сохранен как export.xlsx")
```

## Форматирование Excel

Создаваемый Excel файл включает:

- **Заголовки**: Синий фон, белый текст, жирный шрифт, центрирование
- **Данные**: Стандартный шрифт, выравнивание по левому краю
- **Границы**: Тонкие границы вокруг всех ячеек
- **Ширина колонок**: Автоматическая настройка на основе содержимого
- **Заморозка**: Заголовки остаются видимыми при прокрутке
- **Именование файлов**: Автоматическое с временной меткой

## Документация API

После запуска сервера документация доступна по адресам:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
