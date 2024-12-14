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

import pytest
from .test_fake_checks import FakeBashCheckAlert
from .test_fake_checks import FakeBashCheckWarn
from .test_fake_checks import FakeBashCheckOkay
from .test_fake_checks import FakeBashCheckNa
from .test_fake_checks import FakePythonCheckOkay
from .test_fake_checks import FakePythonCheckAlert
from .test_fake_checks import FakePythonCheckWarn
from .test_fake_checks import FakePythonCheckNa
from .test_fake_checks import FakeCollectAllCheck


#################
# Tests - BASIC #
#################

class TestCollectAllCheckBasic():
    def test_no_content(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)
        assert not collect_all_check.get_filter_checks()
        assert not collect_all_check.get_checks()

    def test_filter_and_check_added(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(FakeBashCheckOkay())
        collect_all_check.add_check(FakePythonCheckOkay())

        assert collect_all_check.get_filter_checks()
        assert len(collect_all_check.get_filter_checks()) == 1
        assert collect_all_check.get_checks()
        assert len(collect_all_check.get_checks()) == 1


###################################
# Tests - SINGLE FILTER AND CHECK #
###################################

class TestCollectAllCheckSingle():
    #########################
    # Tests - filter passes #
    #########################

    def test_single_filter_okay_check_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(FakeBashCheckOkay())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (OKAY)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(OKAY).\n" + \
            "Exit status code is 0, this becomes status OKAY\n" + \
            "Test Python Check                                                     .(OKAY).\n" + \
            "Python check passed"

    def test_single_filter_okay_check_alert(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(FakeBashCheckOkay())
        collect_all_check.add_check(FakePythonCheckAlert())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (ALERT)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(OKAY).\n" + \
            "Exit status code is 0, this becomes status OKAY\n" + \
            "Test Python Check                                                     .(ALERT).\n" + \
            "Python check failed"

    ########################
    # Tests - filter fails #
    ########################

    def test_single_filter_na_check_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(FakeBashCheckNa())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (NA)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(NA).\n" + \
            "Exit status code is 254, this becomes status NA"

    def test_single_filter_warn_check_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(FakeBashCheckWarn())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (NA)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(WARN).\n" + \
            "Exit status code is 255, this becomes status WARN"

    def test_single_filter_alert_check_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(
            FakeBashCheckAlert())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (NA)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(ALERT).\n" + \
            "Exit status code is > 0 and < 253, this becomes status ALERT"


########################
# Tests - MULTI FILTER #
########################

class TestCollectAllCheckMultiFilter():
    def test_multi_filter_both_fail(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter checks, and check
        collect_all_check.add_filter_check(
            FakeBashCheckAlert())
        collect_all_check.add_filter_check(
            FakeBashCheckAlert())
        collect_all_check.add_check(
            FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (NA)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(ALERT).\n" + \
            "Exit status code is > 0 and < 253, this becomes status ALERT"

    def test_multi_filter_first_fails(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(FakeBashCheckAlert())
        collect_all_check.add_filter_check(FakeBashCheckOkay())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (NA)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(ALERT).\n" + \
            "Exit status code is > 0 and < 253, this becomes status ALERT"

    def test_multi_filter_second_fails(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(FakeBashCheckOkay())
        collect_all_check.add_filter_check(
            FakeBashCheckAlert())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (NA)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(OKAY).\n" + \
            "Exit status code is 0, this becomes status OKAY\n" + \
            "Test Bash Check                                                       .(ALERT).\n" + \
            "Exit status code is > 0 and < 253, this becomes status ALERT"

    def test_multi_filter_all_pass(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_filter_check(FakeBashCheckOkay())
        collect_all_check.add_filter_check(FakeBashCheckOkay())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (OKAY)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Bash Check                                                       .(OKAY).\n" + \
            "Exit status code is 0, this becomes status OKAY\n" + \
            "Test Bash Check                                                       .(OKAY).\n" + \
            "Exit status code is 0, this becomes status OKAY\n" \
            "Test Python Check                                                     .(OKAY).\n" \
            "Python check passed"


#######################
# Tests - MULTI CHECK #
#######################


class TestCollectAllCheckMultiChecks():

    ############################################
    # First check fails, second should not run #
    ############################################

    def test_multi_check_alert_alert(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_check(FakePythonCheckAlert())
        collect_all_check.add_check(FakePythonCheckAlert())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (ALERT)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Python Check                                                     .(ALERT).\n" \
            "Python check failed\n" \
            "Test Python Check                                                     .(ALERT).\n" \
            "Python check failed"

    def test_multi_check_warn_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_check(FakePythonCheckWarn())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (WARN)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Python Check                                                     .(WARN).\n" \
            "Python check warned\n" \
            "Test Python Check                                                     .(OKAY).\n" \
            "Python check passed"

    def test_multi_check_na_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add filter check, and check
        collect_all_check.add_check(FakePythonCheckNa())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        with pytest.raises(ValueError, match="Check status cannot be NA, must be either OKAY or WARN or ALERT"):
            collect_all_check.run()

    #########################################
    # First check passes, second should run #
    #########################################

    def test_multi_check_okay_alert_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add checks, no filters
        collect_all_check.add_check(FakePythonCheckOkay())
        collect_all_check.add_check(FakePythonCheckAlert())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (ALERT)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Python Check                                                     .(OKAY).\n" + \
            "Python check passed\n" + \
            "Test Python Check                                                     .(ALERT).\n" + \
            "Python check failed\n" + \
            "Test Python Check                                                     .(OKAY).\n" + \
            "Python check passed"

    def test_multi_check_okay_warn_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add checks, no filters
        collect_all_check.add_check(FakePythonCheckOkay())
        collect_all_check.add_check(FakePythonCheckWarn())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (WARN)     \n'

        # Check body
        assert str(collect_all_check.get_body()) == \
            "Test Python Check                                                     .(OKAY).\n" + \
            "Python check passed\n" + \
            "Test Python Check                                                     .(WARN).\n" + \
            "Python check warned\n" + \
            "Test Python Check                                                     .(OKAY).\n" + \
            "Python check passed"

    def test_multi_check_okay_na_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add checks, no filters
        collect_all_check.add_check(FakePythonCheckOkay())
        collect_all_check.add_check(FakePythonCheckNa())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        with pytest.raises(ValueError, match="Check status cannot be NA, must be either OKAY or WARN or ALERT"):
            collect_all_check.run()

    def test_multi_check_okay_okay_okay(self):
        collect_all_check = FakeCollectAllCheck(level_index=0)

        # Add checks, no filters
        collect_all_check.add_check(FakePythonCheckOkay())
        collect_all_check.add_check(FakePythonCheckOkay())
        collect_all_check.add_check(FakePythonCheckOkay())

        # Run the check
        collect_all_check.run()

        # Check header
        assert str(collect_all_check.get_header()) == \
            'Test collection all check                                              (OKAY)     \n'

        # Check body
        # print("vvvvvvvvvvvvvvvvvvvv")
        # print(collect_all_check.get_body())
        # print("^^^^^^^^^^^^^^^^^^^^")
        assert str(collect_all_check.get_body()) == \
            "Test Python Check                                                     .(OKAY).\n" + \
            "Python check passed\n" + \
            "Test Python Check                                                     .(OKAY).\n" + \
            "Python check passed\n" + \
            "Test Python Check                                                     .(OKAY).\n" + \
            "Python check passed"
