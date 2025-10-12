from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import tempfile
import os
from datetime import datetime

app = FastAPI(title="JSON to Excel Converter", version="1.0.0")

class ExcelData(BaseModel):
    data: List[Dict[str, Any]]

def create_formatted_excel(data: List[Dict[str, Any]]) -> str:
    """
    Создает красиво отформатированный Excel файл из JSON данных
    """
    # Создаем новую рабочую книгу
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data Export"
    
    if not data:
        return None
    
    # Получаем все уникальные ключи из данных
    all_keys = set()
    for row in data:
        all_keys.update(row.keys())
    
    # Сортируем ключи для консистентности
    headers = sorted(list(all_keys))
    
    # Стили для заголовков
    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Стили для данных
    data_font = Font(size=11)
    data_alignment = Alignment(horizontal="left", vertical="center")
    
    # Стили для границ
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Записываем заголовки
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border
    
    # Записываем данные
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, header in enumerate(headers, 1):
            value = row_data.get(header, "")
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.font = data_font
            cell.alignment = data_alignment
            cell.border = thin_border
    
    # Автоматическая настройка ширины колонок
    for col in range(1, len(headers) + 1):
        column_letter = get_column_letter(col)
        max_length = 0
        
        # Проверяем длину заголовка
        header_length = len(str(headers[col-1]))
        max_length = max(max_length, header_length)
        
        # Проверяем длину данных в колонке
        for row in range(2, len(data) + 2):
            cell_value = ws.cell(row=row, column=col).value
            if cell_value:
                max_length = max(max_length, len(str(cell_value)))
        
        # Устанавливаем ширину колонки с небольшим запасом
        ws.column_dimensions[column_letter].width = min(max_length + 2, 50)
    
    # Замораживаем первую строку (заголовки)
    ws.freeze_panes = "A2"
    
    # Создаем временный файл
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    temp_file.close()
    
    # Сохраняем файл
    wb.save(temp_file.name)
    
    return temp_file.name

@app.post("/convert-to-excel")
async def convert_to_excel(excel_data: ExcelData):
    """
    Принимает JSON данные и возвращает Excel файл
    """
    try:
        if not excel_data.data:
            raise HTTPException(status_code=400, detail="Данные не могут быть пустыми")
        
        # Создаем Excel файл
        excel_file_path = create_formatted_excel(excel_data.data)
        
        if not excel_file_path:
            raise HTTPException(status_code=500, detail="Ошибка при создании Excel файла")
        
        # Возвращаем файл
        return FileResponse(
            path=excel_file_path,
            filename=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке данных: {str(e)}")

@app.get("/")
async def root():
    """
    Главная страница с информацией о API
    """
    return {
        "message": "JSON to Excel Converter API",
        "version": "1.0.0",
        "endpoints": {
            "POST /convert-to-excel": "Конвертирует JSON данные в Excel файл",
            "GET /": "Информация о API"
        },
        "example_usage": {
            "url": "/convert-to-excel",
            "method": "POST",
            "body": {
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
                    }
                ]
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Получаем порт из переменной окружения или используем 8000 по умолчанию
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(app, host=host, port=port)
