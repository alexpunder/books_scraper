import logging
import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def timer(func: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:
    """
    Декоратор для измерения времени выполнения функции и сбора статистики.

    Сохраняет состояние между вызовами декорированной функции, включая:
    - Количество вызовов
    - Общее накопленное время выполнения
    - Время каждого отдельного вызова

    Args:
        func: Функция, время выполнения которой нужно измерять

    Returns:
        Обернутую функцию с добавленной логикой замера времени
        и количеством выполнений

    Note:
        - Использует `time.perf_counter()` для точного измерения времени
        - Состояние (счетчик вызовов, общее время) сохраняется между вызовами
        - Каждый вызов логируется через logging.info()
        - Сообщение включает: имя функции, время текущего вызова, номер вызова, общее время
    """
    call_count: int = 0
    total_time: float = 0.0

    @wraps(func)
    def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
        nonlocal call_count, total_time
        call_count += 1
        start_time_inner = time.perf_counter()

        result = func(*args, **kwargs)

        end_time_inner = time.perf_counter()
        diff_time_inner = end_time_inner - start_time_inner
        total_time += diff_time_inner
        logging.info(
            f"Время выполнения функции {func.__name__}: {diff_time_inner:.2f}. "
            f"Номер операции: #{call_count}. Накопленное время: {total_time:.2f}."
        )
        return result

    return wrapper
