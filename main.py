from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить информацию о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # Расстояние, преодолеваемое за один шаг/гребок
    M_IN_KM = 1000  # Константа для перевода значений из метров в километры
    HOUR_IN_MIN = 60  # Константа для перевода часов в минуты

    def __init__(self,
                 action: int,  # Количество совершённых действий
                 duration: float,  # Длительность тренировки
                 weight: float  # Вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """
        Получить дистанцию в км.,
        которую преодолел пользователь за время тренировки.
        """
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения во время тренировки."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных килокалорий."""
        raise NotImplementedError('Реализован только в дочерних классах')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных килокалорий."""
        time_in_minutes = self.duration * self.HOUR_IN_MIN
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * time_in_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMH_IN_MS = 0.278
    C_IN_M = 100
    CALORIES_WEIGHT_MULTIPLIER_ONE = 0.035  # Коэффициент для подсчета калорий
    CALORIES_WEIGHT_MULTIPLIER_TWO = 0.029  # Коэффициент для подсчета калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float  # Рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных килокалорий."""
        time_in_minutes = self.duration * self.HOUR_IN_MIN
        return ((self.CALORIES_WEIGHT_MULTIPLIER_ONE * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MS)**2
                   / (self.height / self.C_IN_M))
                * self.CALORIES_WEIGHT_MULTIPLIER_TWO * self.weight)
                * time_in_minutes)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,  # Длина бассейна в метрах
                 count_pool: int  # Сколько раз пользователь переплыл бассейн
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения во время тренировки."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)
