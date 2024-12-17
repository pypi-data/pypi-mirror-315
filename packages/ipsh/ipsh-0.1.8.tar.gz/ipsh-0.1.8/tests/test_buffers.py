# -*- coding: utf-8 -*-

"""
test the ipsh.buffers module
"""

import io

from unittest import TestCase

from unittest.mock import patch

from ipsh import buffers

from . import commons as tc


class Functions(TestCase):
    """Test the module function(s)"""

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_echo(self, mock_stdout: io.StringIO) -> None:
        """echo() function, version output"""
        buffers.echo("abc", "\x0d", "defg")
        self.assertEqual(mock_stdout.getvalue().strip(), "abc\x0ddefg")


class History(TestCase):
    """Test the History class"""

    def test_position(self) -> None:
        """Test the position property"""
        history = buffers.History()
        with self.subTest("initial"):
            self.assertEqual(history.position, 1)
        #
        history.add("abc")
        history.add("defg")
        with self.subTest("after adding 2 elements"):
            self.assertEqual(history.position, 3)
        #
        with self.subTest("getting relative entry"):
            self.assertEqual(history.get_relative(-1), "defg")
        #
        with self.subTest("after getting relative entry"):
            self.assertEqual(history.position, 2)
        #

    def test_len(self) -> None:
        """Test the len(history_instance) capability"""
        history = buffers.History()
        with self.subTest("initial"):
            self.assertEqual(len(history), 1)
        #
        history.add("abc")
        history.add("defg")
        with self.subTest("after adding 2 elements"):
            self.assertEqual(len(history), 3)
        #

    def test_getitem(self) -> None:
        """Test the history_instance[n] capability"""
        history = buffers.History()
        history.add("abc")
        history.add("defg")
        for idx, expected_value in ((1, "abc"), (2, "defg")):
            with self.subTest("get item", idx=idx):
                self.assertEqual(history[idx], expected_value)
            #
        #
        with self.subTest("max"):
            self.assertEqual(history[3], "")
        #
        for idx in (0, 4, -1):
            with self.subTest("get item", idx=idx):
                self.assertRaisesRegex(
                    buffers.HistoryError, "^Not available$", history.__getitem__, idx
                )
            #
        #

    def test_iter_range(self) -> None:
        """Test the history_instance.iter_range() method"""
        history = buffers.History()
        history.add("abc")
        history.add("defg")
        with self.subTest("defaults"):
            self.assertEqual(list(history.iter_range()), [(1, "abc"), (2, "defg")])
        #
        with self.subTest("last element only"):
            self.assertEqual(list(history.iter_range(start=-1)), [(2, "defg")])
        #
        with self.subTest("first element only, ignoring errors"):
            self.assertEqual(list(history.iter_range(start=0, end=1)), [(1, "abc")])
        #


class LineBuffer(TestCase):
    """Test the LineBuffer class"""

    def setUp(self):
        """Fixture: screen mock"""
        self.screen = tc.ScreenMock()

    def test_init_props(self) -> None:
        """__init__() method and properties"""
        self.screen.clear()
        prompt = " input → "
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb = buffers.LineBuffer(prompt)
        #
        with self.subTest("output"):
            self.assertEqual(self.screen.current_line, list(prompt))
        #
        with self.subTest("screen position"):
            self.assertEqual(self.screen.cursor_pos, len(prompt))
        #
        with self.subTest("buffer position"):
            self.assertEqual(lb.position, 0)
        #
        with self.subTest("value"):
            self.assertEqual(lb.value, tc.EMPTY)
        #
        with self.subTest("length"):
            self.assertEqual(len(lb), 0)
        #
        self.screen.clear()
        prompt = " → "
        preset = "preset input"
        expected_line = f"{prompt}{preset}"
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb2 = buffers.LineBuffer(prompt, initial_value=preset)
        #
        with self.subTest("output", preset=preset):
            self.assertEqual(self.screen.current_line, list(expected_line))
        #
        with self.subTest("screen position", preset=preset):
            self.assertEqual(self.screen.cursor_pos, len(expected_line))
        #
        with self.subTest("buffer position", preset=preset):
            self.assertEqual(lb2.position, len(preset))
        #
        with self.subTest("value", preset=preset):
            self.assertEqual(lb2.value, preset)
        #
        with self.subTest("length", preset=preset):
            self.assertEqual(len(lb2), len(preset))
        #

    def test_replace(self) -> None:
        """replace() method"""
        self.screen.clear()
        prompt = " → "
        preset = "preset input"
        new_value = "new"
        expected_visible = f"{prompt}{new_value}"
        expected_screen = f"{prompt}{new_value:<{len(preset)}}"
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb = buffers.LineBuffer(prompt, initial_value=preset)
            lb.replace(new_value)
        #
        with self.subTest("output", new_value=new_value):
            self.assertEqual(self.screen.current_line, list(expected_screen))
        #
        with self.subTest("screen position", new_value=new_value):
            self.assertEqual(self.screen.cursor_pos, len(expected_visible))
        #
        with self.subTest("buffer position", new_value=new_value):
            self.assertEqual(lb.position, len(new_value))
        #
        with self.subTest("value", new_value=new_value):
            self.assertEqual(lb.value, new_value)
        #
        with self.subTest("length", new_value=new_value):
            self.assertEqual(len(lb), len(new_value))
        #

    def test_insert_string(self) -> None:
        """insert_string() method"""
        self.screen.clear()
        prompt = " → "
        preset = "preset input"
        appendix = "-appendix"
        prefix = "prefix: "
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb = buffers.LineBuffer(prompt, initial_value=preset)
            with self.subTest("value", appended=tc.EMPTY):
                lb.insert_string(tc.EMPTY)
                self.assertEqual(lb.value, preset)
            #
            with self.subTest("error", appended=tc.LF):
                self.assertRaisesRegex(
                    ValueError,
                    "Can only insert fully printable strings",
                    lb.insert_string,
                    tc.LF,
                )
            #
            with self.subTest("value", appended=appendix):
                lb.insert_string(appendix)
                self.assertEqual(lb.value, f"{preset}{appendix}")
            #
            with self.subTest("value", prefix=prefix):
                lb.move_to_home()
                lb.insert_string(prefix)
                self.assertEqual(lb.value, f"{prefix}{preset}{appendix}")
            #
        #

    def test_insert(self) -> None:
        """insert() method"""
        self.screen.clear()
        prompt = " → "
        preset = "preset input"
        appended_string = " + appended full string"
        added_char = "x"
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb = buffers.LineBuffer(prompt, initial_value=preset)
            with self.subTest("value", appended=tc.EMPTY):
                lb.insert(tc.EMPTY)
                self.assertEqual(lb.value, preset)
            #
            with self.subTest("error", appended=tc.LF):
                self.assertRaisesRegex(
                    ValueError,
                    "Can only insert printable characters",
                    lb.insert,
                    tc.LF,
                )
            #
            with self.subTest("value", appended=appended_string):
                lb.insert(appended_string)
                self.assertEqual(lb.value, f"{preset}{appended_string}")
            #
            self.screen.clear()
            lb = buffers.LineBuffer(prompt, initial_value=preset)
            expected_value = f"{preset}{added_char}"
            expected_screen = f"{prompt}{expected_value}"
            with self.subTest("value", appended=added_char):
                lb.insert(added_char)
                self.assertEqual(lb.value, expected_value)
            #
            with self.subTest("output", appended=added_char):
                self.assertEqual(self.screen.current_line, list(expected_screen))
            #
            expected_value = f"{added_char}{preset}{added_char}"
            expected_screen = f"{prompt}{expected_value}"
            with self.subTest("value", prepended=added_char):
                lb.move_to_home()
                lb.insert(added_char)
                self.assertEqual(lb.value, expected_value)
            #
            with self.subTest("output", prepended=added_char):
                self.assertEqual(self.screen.current_line, list(expected_screen))
            #
        #

    def test_movements(self) -> None:
        """move_*() methods"""
        self.screen.clear()
        prompt = " → "
        preset = "preset input"
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb = buffers.LineBuffer(prompt, initial_value=preset)
            expected_position = len(preset) - 1
            with self.subTest("buffer position", expected=expected_position):
                lb.move_left()
                self.assertEqual(lb.position, expected_position)
            #
            expected_position = len(preset) - 2
            with self.subTest("buffer position", expected=expected_position):
                lb.move_left()
                self.assertEqual(lb.position, expected_position)
            #
            # last movement right does not change the position
            # but triggers an alert
            for expected_position in [len(preset) - 1, len(preset), len(preset)]:
                with self.subTest("buffer position", expected=expected_position):
                    lb.move_right()
                    self.assertEqual(lb.position, expected_position)
                #
            #
            with self.subTest("expecting alert (right movement)"):
                self.assertEqual(self.screen.alerts, 1)
            #
            expected_position = 0
            with self.subTest("buffer position", expected=expected_position):
                lb.move_to_home()
                self.assertEqual(lb.position, expected_position)
            #
            with self.subTest("buffer position unchanged", expected=expected_position):
                lb.move_left()
                self.assertEqual(lb.position, expected_position)
            #
            with self.subTest("expecting alert (left movement at home position)"):
                self.assertEqual(self.screen.alerts, 2)
            #
            expected_position = len(preset)
            with self.subTest("buffer position", expected=expected_position):
                lb.move_to_end()
                self.assertEqual(lb.position, expected_position)
            #
        #

    def test_delete_from_cursor(self) -> None:
        """delete_from_cursor() method"""
        self.screen.clear()
        prompt = " → "
        preset = "preset input"
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb = buffers.LineBuffer(prompt, initial_value=preset)
            expected_value = "pr"
            expected_screen = f"{prompt}pr          "
            with self.subTest("value", expected=expected_value):
                lb.move_to_home()
                lb.move_right()
                lb.move_right()
                lb.delete_from_cursor()
                self.assertEqual(lb.value, expected_value)
            #
            with self.subTest("output", expected=expected_screen):
                self.assertEqual(self.screen.current_line, list(expected_screen))
            #
        #

    def test_delete_to_left(self) -> None:
        """delete_to_left() method"""
        self.screen.clear()
        prompt = " → "
        preset = "preset input"
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb = buffers.LineBuffer(prompt, initial_value=preset)
            expected_value = "preset inut"
            expected_screen = f"{prompt}preset inut "
            with self.subTest("value", expected=expected_value):
                lb.move_left()
                lb.move_left()
                lb.delete_to_left()
                self.assertEqual(lb.value, expected_value)
            #
            with self.subTest("output", expected=expected_screen):
                self.assertEqual(self.screen.current_line, list(expected_screen))
            #
            with self.subTest("alert"):
                lb.move_to_home()
                lb.delete_to_left()
                self.assertEqual(self.screen.alerts, 1)
            #
            with self.subTest("unchanged value", expected=expected_value):
                self.assertEqual(lb.value, expected_value)
            #
        #

    def test_delete_to_right(self) -> None:
        """delete_to_right() method"""
        self.screen.clear()
        prompt = " → "
        preset = "preset input"
        with patch("ipsh.buffers.echo", new=self.screen.echo):
            lb = buffers.LineBuffer(prompt, initial_value=preset)
            with self.subTest("alert"):
                lb.delete_to_right()
                self.assertEqual(self.screen.alerts, 1)
            #
            with self.subTest("unchanged value", expected=preset):
                self.assertEqual(lb.value, preset)
            #
            expected_value = "preset inpt"
            expected_screen = f"{prompt}preset inpt "
            with self.subTest("value", expected=expected_value):
                lb.move_left()
                lb.move_left()
                lb.delete_to_right()
                self.assertEqual(lb.value, expected_value)
            #
            with self.subTest("output", expected=expected_screen):
                self.assertEqual(self.screen.current_line, list(expected_screen))
            #
        #
