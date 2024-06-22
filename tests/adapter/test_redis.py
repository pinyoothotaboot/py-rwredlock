import unittest
import uuid
from adapter.redis import Broker
from libs.exceptions.empty_string_exception import EmptyStringException
from libs.constants.error_codes import ERROR_EMPTY_STRING


class TestRedis(unittest.TestCase):
    _ID: str = "1234-abcd"
    _broker: Broker

    def setUp(self):
        self._broker = Broker()

    def tearDown(self):
        del self._broker

    def test_set_with_data_passed(self):
        message = "HELLO WORLD"
        do_set = self._broker.set(self._ID, message, 10)
        self.assertEqual(do_set, True)

    def test_set_with_empty_id_failed(self):
        with self.assertRaises(EmptyStringException) as cm:
            message = "HELLO WORLD"
            self._broker.set("", message, 10)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The id is empty")

    def test_set_with_empty_value_failed(self):
        with self.assertRaises(EmptyStringException) as cm:
            message = ""
            self._broker.set(self._ID, message, 10)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The value is empty")

    def test_get_with_data_passed(self):
        message = "HELLO WORLD"
        do_set = self._broker.set(self._ID, message, 10)
        resp = self._broker.get(self._ID)
        self.assertEqual(do_set, True)
        self.assertEqual(resp, message)

    def test_get_with_empty_id_failed(self):
        message = "HELLO WORLD"
        do_set = self._broker.set(self._ID, message, 10)
        self.assertEqual(do_set, True)

        with self.assertRaises(EmptyStringException) as cm:
            resp = self._broker.get("")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The id is empty")

    def test_delete_with_data_passed(self):
        message = "HELLO WORLD"
        do_set = self._broker.set(self._ID, message, 10)
        do_del = self._broker.delete(self._ID)
        self.assertEqual(do_set, True)
        self.assertEqual(do_del, True)

    def test_delete_with_empty_id_failed(self):
        message = "HELLO WORLD"
        do_set = self._broker.set(self._ID, message, 10)
        self.assertEqual(do_set, True)

        with self.assertRaises(EmptyStringException) as cm:
            do_del = self._broker.delete("")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The id is empty")

    def test_increase_with_data_passed(self):
        inc_id = f"{self._ID}:INC:{uuid.uuid4()}"
        inc = self._broker.increase(inc_id)
        self.assertEqual(inc, 1)

    def test_increase_with_empty_id_failed(self):
        with self.assertRaises(EmptyStringException) as cm:
            inc = self._broker.increase("")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The id is empty")

    def test_decrease_with_data_passed(self):
        inc_id = f"{self._ID}:INC:{uuid.uuid4()}"
        inc = self._broker.increase(inc_id)
        dec = self._broker.decrease(inc_id)
        self.assertEqual(inc, 1)
        self.assertEqual(dec, 0)

    def test_decrease_with_empty_id_failed(self):
        with self.assertRaises(EmptyStringException) as cm:
            inc = self._broker.decrease("")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The id is empty")

    def test_publish_with_data_passed(self):
        payload = "HELLO PAYLOAD"
        do_pub = self._broker.publish(self._ID, payload)
        self.assertEqual(do_pub, True)

    def test_publish_with_empty_id_failed(self):
        payload = "HELLO PAYLOAD"
        with self.assertRaises(EmptyStringException) as cm:
            do_pub = self._broker.publish("", payload)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The id is empty")

    def test_publish_with_empty_payload_failed(self):
        payload = ""
        with self.assertRaises(EmptyStringException) as cm:
            do_pub = self._broker.publish(self._ID, payload)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The payload is empty")

    def test_subscribe_with_empty_id_failed(self):
        with self.assertRaises(EmptyStringException) as cm:
            message = self._broker.subscribe("", 5)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, ERROR_EMPTY_STRING)
        self.assertEqual(the_exception.message, "The id is empty")


if __name__ == "__main__":
    unittest.main()
