# free_time_manager
FreeTime - это сервис, который позволяет определить свободные интервалы времени, исходя из заданных интервалов занятости.
* * *

## Стек
Python 3.11

## Установка
1. Склонируйте репозиторий 
``` 
git clone https://github.com/cement-hools/free_time_manager
```
2. Перейдите в директорию проекта:
``` 
cd free_time_manager
```


## Использование

```python
from datetime import datetime
from free_time import FreeTime

# Задайте интервалы занятости
busy_intervals = [
    {"start": "10:30", "stop": "10:50"},
    {"start": "18:40", "stop": "18:50"},
    {"start": "14:40", "stop": "15:50"},
    {"start": "16:40", "stop": "17:20"},
    {"start": "20:05", "stop": "20:20"},
]

# Создайте экземпляр сервиса FreeTime
free_time_service = FreeTime("9:00", "21:00")

# Установите интервалы занятости
free_time_service.set_busy_intervals(busy_intervals)

# Получите свободные интервалы времени
free_intervals = free_time_service.get_free_time_intervals()

# Выведите свободные интервалы времени
for interval in free_intervals:
    print(f"Free interval: {interval['start']} - {interval['stop']}")
    
# или используйте метод print_free_time
free_time_service.print_free_time()
```

## API

### Класс FreeTime 

Методы

 - ```set_busy_intervals(busy_intervals: list[dict[str, str]])```: Устанавливает интервалы занятости.
 - ```set_free_interval_minutes(minutes: int)```: Задает размер свободного времени.
 - ```get_free_time_intervals() -> list[dict[str, str]]```: Возвращает свободные интервалы времени.
 - ```print_free_time()```: Выводит в консоль свободные интервалы времени.


## Авторы
- Секачёв Максим
