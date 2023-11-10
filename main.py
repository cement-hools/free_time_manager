import datetime
from dataclasses import dataclass


class DateTimeMixin:
    """Работа с объектами datetime"""

    @staticmethod
    def _to_datetime(time: str) -> datetime.datetime:
        """Перевести строку времени в объект datetime."""
        try:
            return datetime.datetime.strptime(time, '%H:%M')
        except ValueError:
            raise ValueError("Invalid time format. Please use HH:MM format.")


@dataclass
class BusyInterval(DateTimeMixin):
    """Класс для представления занятого интервала времени"""
    start_time: datetime.datetime
    stop_time: datetime.datetime

    def __init__(self, start_time: str, stop_time: str):
        self.start_time = self._to_datetime(start_time)
        self.stop_time = self._to_datetime(stop_time)


class FreeTime(DateTimeMixin):
    """Свободные интервалы времени"""

    def __init__(
            self,
            start_time: str,
            stop_time: str,
            busy_intervals: list[dict[str, str]] | None = None,
            free_interval_minutes: int = 30
    ):
        self.start_time = self._to_datetime(start_time)
        self.stop_time = self._to_datetime(stop_time)
        self._free_interval_minutes = free_interval_minutes
        if busy_intervals:
            self._busy_intervals = self._create_busy_intervals(busy_intervals)
        else:
            self._busy_intervals = self._get_blank_busy()
        self._free_intervals = self._calculate_free_time()

    @staticmethod
    def _get_blank_busy() -> list[BusyInterval]:
        """Получить пустой список занятых интервалов."""
        return [BusyInterval(start_time="00:00", stop_time="00:00")]

    def _create_busy_intervals(self, busy_intervals) -> list[BusyInterval]:
        """Создать отсортированный список интервалов занятости."""
        intervals = [
            BusyInterval(
                start_time=interval["start"],
                stop_time=interval["stop"]
            )
            for interval in busy_intervals
        ]
        return self._sort_busy_list(intervals)

    def set_busy_intervals(self, busy_intervals: list[dict[str, str]]):
        """Установить время занятости."""
        self._busy_intervals = self._create_busy_intervals(busy_intervals)
        self._update_free_intervals()

    def set_free_interval_minutes(self, minutes: int):
        """Задать размер свободного времени."""
        self._free_interval_minutes = minutes
        self._update_free_intervals()

    def _update_free_intervals(self):
        """Присчитать интервалы свободного армени."""
        self._free_intervals = self._calculate_free_time()

    def _calculate_free_time(self) -> list[dict[str, str]]:
        """Расчитать свободные интервалы."""
        busy = self._busy_intervals
        busy_index = 0

        free_intervals = []

        free_window = datetime.timedelta(minutes=self._free_interval_minutes)
        current_time = self.start_time
        stop_time = self.stop_time - free_window

        while current_time <= stop_time:
            interval_start = current_time
            interval_end = interval_start + free_window
            busy_interval = busy[busy_index]

            if (
                    interval_end <= busy_interval.start_time
                    or interval_start >= busy_interval.stop_time

            ):
                free_interval = {
                    "start": str(interval_start.time()),
                    "stop": str(interval_end.time()),
                }
                free_intervals.append(free_interval)
            elif (
                    interval_end > busy_interval.start_time
                    and busy_index < len(busy) - 1

            ):
                busy_index += 1
                current_time = busy_interval.stop_time
                continue
            current_time = interval_end

        return free_intervals

    def get_free_time_intervals(self) -> list[dict[str, str]]:
        """Получить свободные интервалы времени исходя из загруженности."""
        return self._free_intervals

    def print_free_time(self):
        """Вывести в консоль свободные интервалы."""
        if not self._free_intervals:
            print("No free intervals available.")
        else:
            for interval in self._free_intervals:
                print(f"{interval['start']} - {interval['stop']}")

    @staticmethod
    def _sort_busy_list(intervals: list[BusyInterval]):
        """Отсортировать интервал занятости."""
        return sorted(intervals, key=lambda x: x.start_time)


if __name__ == '__main__':
    busy = [
        {"start": "10:30", "stop": "10:50"},
        {"start": "18:40", "stop": "18:50"},
        {"start": "14:40", "stop": "15:50"},
        {"start": "16:40", "stop": "17:20"},
        {"start": "20:05", "stop": "20:20"},
    ]

    free_time_service = FreeTime("9:00", "21:00")
    free_time_service.set_busy_intervals(busy)
    free_intervals = free_time_service.get_free_time_intervals()
    print("Free intervals:", free_intervals)
    free_time_service.print_free_time()
    print("#" * 20)
    free_time_service.set_free_interval_minutes(25)
    free_time_service.print_free_time()
