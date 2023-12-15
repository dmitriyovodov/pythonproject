import unittest
from unittest.mock import Mock

button_names = ["Новая задача", "Удалить задачу", "Редактировать задачу", "Посмотреть задачу", "Посмотреть все задачи",
                "Отменить действие", "Войти", "Зарегистрироваться"]


def cancelling(message, text="Действие отменено"):
    if message.text == button_names[5]:
        #default_buttons(message, text)
        return True
    return False


class Cancelling_Test(unittest.TestCase):
    def test_1(self):
        mock_message = Mock()
        mock_message.text = "Отменить действие"
        self.assertEqual(cancelling(mock_message), True)

    def test_2(self):
        mock_message = Mock()
        mock_message.text = "laskjfdlkasjlk"
        self.assertEqual(cancelling(mock_message), False)

    def test_3(self):
        mock_message = Mock()
        mock_message.text = "Новая задача"
        self.assertEqual(cancelling(mock_message), False)

    def test_4(self):
        mock_message = Mock()
        mock_message.text = "XDD"
        self.assertEqual(cancelling(mock_message), False)

    def test_5(self):
        mock_message = Mock()
        mock_message.text = "XDD"
        self.assertEqual(cancelling(mock_message), False)


if __name__ == '__main__':
    unittest.main()
