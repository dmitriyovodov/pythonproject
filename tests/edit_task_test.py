import unittest
from unittest.mock import Mock
from cancelling_test import cancelling
from fnmatch import fnmatch


def editTask(message):
    if cancelling(message):
        return "Действие отменено"
    deadline = message.text.strip()
    """
        if not fnmatch(deadline, "??/??/??"):
            default_buttons(message, "Дедлайн введён неправильно")
            return
        conn = sqlite3.connect("user.sql")
        cur = conn.cursor()
        cur.execute(
            'UPDATE tasks SET task = ? WHERE task_name = ? AND user_name = ? ',
            (task, task_name, user_name))
        cur.execute(
            'UPDATE tasks SET deadline = ? WHERE task_name = ? AND user_name = ? ',
            (deadline, task_name, user_name))
        conn.commit()
        cur.close()
        conn.close()
        default_buttons(message, f"Задача {task_name} изменена!")
    """
    if fnmatch(deadline, "??/??/??"):
        return "Задача изменена"
    return "Неправильно введён дедлайн"


class EditTask_Test(unittest.TestCase):
    def test_1(self):
        mock_message = Mock()
        mock_message.text = "Отменить действие"
        self.assertEqual(editTask(mock_message), "Действие отменено")

    def test_2(self):
        mock_message = Mock()
        mock_message.text = "asfdasdafas"
        self.assertEqual(editTask(mock_message), "Неправильно введён дедлайн")

    def test_3(self):
        mock_message = Mock()
        mock_message.text = "26/12/23"
        self.assertEqual(editTask(mock_message), "Задача изменена")

    def test_4(self):
        mock_message = Mock()
        mock_message.text = "12/11/2023"
        self.assertEqual(editTask(mock_message), "Неправильно введён дедлайн")

    def test_5(self):
        mock_message = Mock()
        mock_message.text = "Чётвёртое сентября две тысячи четвёртого года"
        self.assertEqual(editTask(mock_message), "Неправильно введён дедлайн")


if __name__ == '__main__':
    unittest.main()
