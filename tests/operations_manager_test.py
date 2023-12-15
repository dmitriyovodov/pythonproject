import unittest
from unittest.mock import Mock

button_names = ["Новая задача", "Удалить задачу", "Редактировать задачу", "Посмотреть задачу", "Посмотреть все задачи",
                "Отменить действие", "Войти", "Зарегистрироваться"]


def operations_manager(message):
    if message.text in button_names:
        return True
    return False


class Operations_Manager_Test(unittest.TestCase):
    def test_1(self):
        mock_message = Mock()
        mock_message.text = "Новая задача"
        self.assertEqual(operations_manager(mock_message), True)

    def test_2(self):
        mock_message = Mock()
        mock_message.text = "Редактировать задачу"
        self.assertEqual(operations_manager(mock_message), True)

    def test_3(self):
        mock_message = Mock()
        mock_message.text = "Посмотреть задачу"
        self.assertEqual(operations_manager(mock_message), True)

    def test_4(self):
        mock_message = Mock()
        mock_message.text = "Посмотреть все задачи"
        self.assertEqual(operations_manager(mock_message), True)

    def test_5(self):
        mock_message = Mock()
        mock_message.text = "LAKJFkdljsa;lkj"
        self.assertEqual(operations_manager(mock_message), False)


if __name__ == '__main__':
    unittest.main()
