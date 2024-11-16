from settings import BONUS_TIERS


class BonusObserver:
    """
    Наблюдатель, отвечающий за обновление уровня бонусов пользователя на основе его общих трат.
    """

    def __init__(self, user):
        """
        Инициализирует наблюдателя с пользователем, которого необходимо отслеживать.
        :param user: объект пользователя.
        """
        self.user = user

    def update(self, amount):
        """
        Обновляет общие траты пользователя и проверяет необходимость изменения бонусного уровня.
        :param amount: сумма новой транзакции.
        """
        self.user.total_spent += amount
        self._update_bonus_level()

    def _update_bonus_level(self):
        """
        Проверяет текущий уровень трат пользователя и обновляет его бонусный уровень, если это необходимо.
        """
        for level, data in sorted(BONUS_TIERS.items(), key=lambda x: x[1]['min_spend'], reverse=True):
            if self.user.total_spent >= data['min_spend']:
                if self.user.bonus_level != level:
                    self.user.bonus_level = level
                    self.user.cashback_percentage = data['cashback']
                    break