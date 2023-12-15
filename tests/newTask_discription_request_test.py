import unittest
from unittest.mock import Mock
from cancelling_test import cancelling
from operations_manager_test import button_names


def newTask_discription_request(message):
    if cancelling(message):
        return "Действие отменено"
    #global task_name
    task_name = message.text.strip()
    """
    if task_name in used_names:
        default_buttons(message, "Имя уже использовано, попробуйте использовать другое")
        return
    bot.send_message(message.chat.id, "Введите описание")
    bot.register_next_step_handler(message, newTask_deadline_request)
    """
    if task_name not in button_names:
        return "Введите описание задачи"
    return "Имя занято"


class EditTask_Test(unittest.TestCase):
    def test_1(self):
        mock_message = Mock()
        mock_message.text = "Отменить действие"
        self.assertEqual(newTask_discription_request(mock_message), "Действие отменено")

    def test_2(self):
        mock_message = Mock()
        mock_message.text = "Новая задача"
        self.assertEqual(newTask_discription_request(mock_message), "Имя занято")

    def test_3(self):
        mock_message = Mock()
        mock_message.text = "Удалить задачу"
        self.assertEqual(newTask_discription_request(mock_message), "Имя занято")

    def test_4(self):
        mock_message = Mock()
        mock_message.text = "Имя"
        self.assertEqual(newTask_discription_request(mock_message), "Введите описание задачи")

    def test_5(self):
        mock_message = Mock()
        mock_message.text = "Имяяя"
        self.assertEqual(newTask_discription_request(mock_message), "Введите описание задачи")


if __name__ == '__main__':
    unittest.main()
