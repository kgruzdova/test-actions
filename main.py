from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn
import pytz

app = FastAPI(title="Time Server API", version="1.0.0")

@app.get("/")
async def root():
    """
    Главная страница API.
    
    Возвращает информационное сообщение о сервисе.
    
    Returns:
        dict: Словарь с приветственным сообщением
    """
    return {"message": "Time Server API"}

@app.get("/time")
async def get_current_time():
    """
    Получить текущее время сервера.
    
    Возвращает текущее время сервера в различных форматах:
    - ISO формат (строка)
    - Unix timestamp (число)
    - Отформатированная строка
    
    Returns:
        dict: Словарь с текущим временем в разных форматах
            - current_time (str): Время в ISO формате
            - timestamp (float): Unix timestamp
            - formatted_time (str): Отформатированное время
    """
    current_time = datetime.now()
    return {
        "current_time": current_time.isoformat(),
        "timestamp": current_time.timestamp(),
        "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "time_zone": current_time.tzinfo
    }

@app.get("/health")
async def health_check():
    """
    Проверка состояния сервера.
    
    Эндпоинт для мониторинга работоспособности сервиса.
    Возвращает статус "healthy" и текущее время.
    
    Returns:
        dict: Словарь со статусом сервера
            - status (str): Статус сервера ("healthy")
            - timestamp (str): Время проверки в ISO формате
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/date")
async def get_date():
    """
    Получить текущую дату сервера.
    
    Возвращает текущую дату без времени в формате ISO.
    
    Returns:
        dict: Словарь с текущей датой
            - current_date (str): Дата в ISO формате (ГГГГ-ММ-ДД)
    """
    current_date = datetime.now()
    return {
        "current_date": current_date.date().isoformat(),
        "timestamp": current_date.timestamp(),
        "formatted_date": current_date.strftime("%Y-%m-%d"),
        "day": current_date.day,
        "month": current_date.month,
        "year": current_date.year,
        "weekday": current_date.weekday(),
        "weekday_number": current_date.weekday(),
        "day_of_year": current_date.timetuple().tm_yday,
    }
@app.get("/datetime")
async def get_current_datetime():
    """
    Получить текущую дату и время сервера.
    
    Возвращает текущую дату и время в формате ISO.
    
    Returns:
        dict: Словарь с текущей датой и временем
    """
    return {
        "current_datetime": datetime.now().isoformat(),
        "formatted_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().date().isoformat(),
        "time": datetime.now().time().isoformat(),
        "timestamp": datetime.now().timestamp(),
        "time_zone": datetime.now().tzinfo,
        "day": datetime.now().day,
        "month": datetime.now().month,
        "year": datetime.now().year,
        "weekday": datetime.now().weekday(),
        "hour": datetime.now().hour,
        "minute": datetime.now().minute,
        "second": datetime.now().second,
        "microsecond": datetime.now().microsecond,
        "weekday_number": datetime.now().weekday(),
        "day_of_year": datetime.now().timetuple().tm_yday
    }

@app.get("/convert")
async def convert_time(time_str: str, timezone: str):
    """
    Конвертировать время из UTC в указанный часовой пояс.
    
    Args:
        time_str (str): Время в формате "HH:MM" или "YYYY-MM-DD HH:MM"
        timezone (str): Название часового пояса (например, "Asia/Yekaterinburg", "Europe/Moscow")
        
    Returns:
        dict: Оригинальное время в UTC и сконвертированное время
    """
    try:
        # Пытаемся распарсить время (сначала HH:MM, потом полный формат)
        try:
            input_time = datetime.strptime(time_str, "%H:%M")
            # Если передано только время, берем сегодняшнюю дату
            now = datetime.now()
            input_time = input_time.replace(year=now.year, month=now.month, day=now.day)
        except ValueError:
            input_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        
        # Устанавливаем UTC для входного времени
        utc_time = pytz.utc.localize(input_time)
        
        # Находим целевой часовой пояс
        try:
            target_tz = pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            # Попробуем найти по части названия (например "Екатеринбург")
            all_timezones = pytz.all_timezones
            found_tz = None
            
            # Словарь маппинга русских названий на стандарты pytz
            russian_tz_map = {
                "екатеринбург": "Asia/Yekaterinburg",
                "москва": "Europe/Moscow",
                "калининград": "Europe/Kaliningrad",
                "новосибирск": "Asia/Novosibirsk",
                "владивосток": "Asia/Vladivostok"
            }
            
            mapped_tz = russian_tz_map.get(timezone.lower())
            if mapped_tz:
                target_tz = pytz.timezone(mapped_tz)
            else:
                # Поиск по подстроке
                for tz in all_timezones:
                    if timezone.lower() in tz.lower():
                        found_tz = tz
                        break
                if found_tz:
                    target_tz = pytz.timezone(found_tz)
                else:
                    raise HTTPException(status_code=400, detail=f"Unknown timezone: {timezone}")

        # Конвертируем
        converted_time = utc_time.astimezone(target_tz)
        
        return {
            "input_utc": time_str,
            "target_timezone": str(target_tz),
            "converted_time": converted_time.strftime("%H:%M"),
            "full_converted_datetime": converted_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid time format. Use HH:MM or YYYY-MM-DD HH:MM. Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)