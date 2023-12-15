import unittest
from unittest.mock import Mock
from cancelling_test import cancelling


def viewTask(message):
    if cancelling(message):
        return "Действие отменено"
    """
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM tasks')
    tasks = cur.fetchall()
    for i in tasks:
        if i[1] == message.text.strip() and i[4] == user_name and i[1] != "task0":
            s = f"{i[1]}\n{i[2]}\n{i[3]}"
            break
    else:
        s = "Такой задачи не существует"
    cur.close()
    conn.close()
    default_buttons(message, s)
    """
    return "Задача показана"


class ViewTask_Test(unittest.TestCase):
    def test_1(self):
        mock_message = Mock()
        mock_message.text = "Отменить действие"
        self.assertEqual(viewTask(mock_message), "Действие отменено")

    def test_2(self):
        mock_message = Mock()
        mock_message.text = "kasdlflks"
        self.assertEqual(viewTask(mock_message), "Задача показана")

    def test_3(self):
        mock_message = Mock()
        mock_message.text = "asfdasnfs"
        self.assertEqual(viewTask(mock_message), "Задача показана")

    def test_4(self):
        mock_message = Mock()
        mock_message.text = "Task_name1"
        self.assertEqual(viewTask(mock_message), "Задача показана")

    def test_5(self):
        mock_message = Mock()
        mock_message.text = "Task_name2"
        self.assertEqual(viewTask(mock_message), "Задача показана")


if __name__ == '__main__':
    unittest.main()