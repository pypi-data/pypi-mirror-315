# MIT License
#
# Copyright (c) 2024-2025 Gwyn Davies
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR,
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from montty.app.check.bash_check import BashCheck
from .test_fake_checks import FakeCollectBaseCheck
from .test_fake_checks import FakePythonCheckOkay


#########
# Tests #
#########


class TestCollectbaseCheck():

    def test_get_filter_check(self):
        collection_check = FakeCollectBaseCheck(level_index=0)
        assert not collection_check.get_filter_checks()
        assert not collection_check.get_checks()

        collection_check.add_filter_check(BashCheck("title", "bask_script"))
        collection_check.run()
        # Check we now have a filter check, but still no checks
        assert collection_check.get_filter_checks()
        assert len(collection_check.get_filter_checks()) == 1
        assert not collection_check.get_checks()
        assert len(collection_check.get_checks()) == 0

    def test_get_check(self):
        collection_check = FakeCollectBaseCheck(level_index=0)
        assert not collection_check.get_filter_checks()
        assert not collection_check.get_checks()

        collection_check.add_check(FakePythonCheckOkay())
        collection_check.run()
        # Check we now have a check, but no filter checks
        assert not collection_check.get_filter_checks()
        assert len(collection_check.get_filter_checks()) == 0
        assert collection_check.get_checks()
        assert len(collection_check.get_checks()) == 1

    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_na(self):
        collection_check = FakeCollectBaseCheck(
            level_index=0)
        collection_check.run()

        string = str(collection_check.get_header())
        assert string.startswith('Test collection base check')
        assert '(NA)' in string
        assert string.endswith('\n')

        assert str(collection_check.get_body()) == ''
        assert collection_check.get_status().is_na()

        string = collection_check.get_output()
        assert string.startswith('Test collection base check')
        assert '(NA)' in string
        assert string.endswith('\n')

        assert collection_check.get_level().get_index() == 0
        assert str(collection_check.get_level()) == '     '


#########
# Level #
#########

    # Ignore warning for accessing internal members
    # pylint: disable=W0212

    def test_na_has_level_1(self):
        collection_check = FakeCollectBaseCheck(level_index=1)
        collection_check.run()

        string = str(collection_check.get_header())
        assert string.startswith('Test collection base check')
        assert '(NA)' in string
        assert string.endswith('\n')

        assert str(collection_check.get_body()) == ''
        assert collection_check.get_status().is_na()

        string = collection_check.get_output()
        assert string.startswith('Test collection base check')
        assert '.(NA).' in string
        assert string.endswith('\n')

        assert collection_check.get_level().get_index() == 1
        assert str(collection_check.get_level()) == '    .'
