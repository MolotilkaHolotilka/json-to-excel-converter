# 🚀 Деплой на Coolify (Hetzner)

## Подготовка к деплою

### 1. 📁 Структура проекта
Убедитесь, что у вас есть все файлы:
```
your-project/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

### 2. 🔧 Настройка Coolify

#### Вариант A: Через Git репозиторий (Рекомендуется)

1. **Создайте Git репозиторий:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/json-to-excel-api.git
   git push -u origin main
   ```

2. **В Coolify:**
   - Создайте новый проект
   - Выберите "Git Repository"
   - Укажите URL вашего репозитория
   - Выберите ветку (обычно `main`)

#### Вариант B: Через Dockerfile

1. **В Coolify:**
   - Создайте новый проект
   - Выберите "Dockerfile"
   - Загрузите архив с проектом или укажите путь к Dockerfile

### 3. ⚙️ Настройки в Coolify

#### Environment Variables (Переменные окружения):
```
PORT=8000
HOST=0.0.0.0
PYTHONUNBUFFERED=1
```

#### Port Configuration:
- **Internal Port:** 8000
- **External Port:** 8000 (или любой другой)

#### Health Check:
- **Path:** `/`
- **Interval:** 30s
- **Timeout:** 10s

### 4. 🐳 Docker настройки

Coolify автоматически обнаружит Dockerfile и соберет контейнер.

**Dockerfile оптимизирован для:**
- ✅ Безопасности (не root пользователь)
- ✅ Производительности (slim образ)
- ✅ Кэширования слоев
- ✅ Минимального размера

### 5. 🌐 Домен и SSL

1. **В Coolify:**
   - Перейдите в настройки проекта
   - Добавьте ваш домен (например: `api.yourdomain.com`)
   - Включите SSL (Let's Encrypt)

2. **DNS настройки:**
   ```
   api.yourdomain.com → IP вашего Hetzner сервера
   ```

### 6. 📊 Мониторинг

Coolify предоставляет встроенный мониторинг:
- Логи приложения
- Использование ресурсов
- Health checks
- Автоматические перезапуски

### 7. 🔄 Автоматический деплой

При использовании Git репозитория:
- Каждый push в main ветку автоматически запускает деплой
- Можно настроить webhooks для других веток

## 🧪 Тестирование после деплоя

### 1. Проверка здоровья:
```bash
curl https://api.yourdomain.com/
```

### 2. Тест API:
```bash
curl -X POST "https://api.yourdomain.com/convert-to-excel" \
     -H "Content-Type: application/json" \
     -d '{
       "data": [
         {
           "Category": "Test",
           "Brand": "Test Brand",
           "Model": "Test Model"
         }
       ]
     }' \
     --output "test.xlsx"
```

### 3. Документация API:
Откройте в браузере: `https://api.yourdomain.com/docs`

## 🚨 Troubleshooting

### Проблема: Приложение не запускается
**Решение:**
- Проверьте логи в Coolify
- Убедитесь, что порт 8000 открыт
- Проверьте переменные окружения

### Проблема: Ошибки при сборке Docker
**Решение:**
- Проверьте Dockerfile на синтаксические ошибки
- Убедитесь, что все файлы в .dockerignore исключены правильно

### Проблема: Медленная работа
**Решение:**
- Увеличьте ресурсы контейнера в Coolify
- Проверьте настройки health check

## 📈 Масштабирование

### Горизонтальное масштабирование:
1. В Coolify увеличьте количество реплик
2. Настройте load balancer
3. Используйте внешнюю базу данных для сессий (если нужно)

### Вертикальное масштабирование:
1. Увеличьте CPU/RAM для контейнера
2. Оптимизируйте код (кэширование, async операции)

## 🔒 Безопасность

### Рекомендации:
- ✅ Используйте HTTPS (SSL)
- ✅ Настройте firewall
- ✅ Регулярно обновляйте зависимости
- ✅ Мониторьте логи на подозрительную активность
- ✅ Ограничьте размер загружаемых файлов

### Ограничение размера файлов:
Добавьте в `main.py`:
```python
from fastapi import Request

@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.method == "POST":
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=413, detail="File too large")
    response = await call_next(request)
    return response
```

## 🎉 Готово!

Ваш API будет доступен по адресу: `https://api.yourdomain.com`

**Endpoints:**
- `GET /` - информация о API
- `POST /convert-to-excel` - конвертация JSON в Excel
- `GET /docs` - Swagger документация
- `GET /redoc` - ReDoc документация
