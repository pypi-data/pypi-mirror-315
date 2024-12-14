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
from montty.app.check.check_body import CheckBody
from montty.app.check.collect_all_check import CollectAllCheck
from montty.app.check.collect_base_check import CollectBaseCheck
from montty.app.check.collect_depend_check import CollectDependCheck
from montty.app.check.python_check import PythonCheck
from montty.app.status import Status


# -----------#
# Bash check #
# -----------#

class FakeBashCheckAlert(BashCheck):
    def __init__(self, level_index=1):
        self._header_title = 'Test Bash Check'
        self._bash_script = 'mty_util/mtyalert.sh'
        super().__init__(self._header_title, self._bash_script, level_index=1)


class FakeBashCheckWarn(BashCheck):
    def __init__(self, level_index=1):
        self._header_title = 'Test Bash Check'
        self._bash_script = 'mty_util/mtywarn.sh'
        super().__init__(self._header_title, self._bash_script, level_index=1)


class FakeBashCheckOkay(BashCheck):
    def __init__(self, level_index=1):
        self._header_title = 'Test Bash Check'
        self._bash_script = 'mty_util/mtyokay.sh'
        super().__init__(self._header_title, self._bash_script, level_index=1)


class FakeBashCheckNa(BashCheck):
    def __init__(self, level_index=1):
        self._header_title = 'Test Bash Check'
        self._bash_script = 'mty_util/mtyna.sh'
        super().__init__(self._header_title, self._bash_script, level_index=1)

# -------------#
# Python check #
# -------------#


class FakePythonCheckOkay(PythonCheck):
    def __init__(self, level_index=1):
        self._header_title = 'Test Python Check'
        super().__init__(self._header_title, level_index)

    def _run_class(self) -> None:
        pass

    def _set_class_result(self, status: Status, body: CheckBody) -> Status:
        status.set_okay()
        body.append_text("Python check passed")


class FakePythonCheckAlert(PythonCheck):
    def __init__(self, level_index=1):
        self._header_title = 'Test Python Check'
        super().__init__(self._header_title, level_index)

    def _run_class(self) -> None:
        pass

    def _set_class_result(self, status: Status, body: CheckBody) -> Status:
        status.set_alert()
        body.append_text("Python check failed")


class FakePythonCheckWarn(PythonCheck):
    def __init__(self, level_index=1):
        self._header_title = 'Test Python Check'
        super().__init__(self._header_title, level_index)

    def _run_class(self) -> None:
        pass

    def _set_class_result(self, status: Status, body: CheckBody) -> Status:
        status.set_warn()
        body.append_text("Python check warned")


class FakePythonCheckNa(PythonCheck):
    def __init__(self, level_index=1):
        self._header_title = 'Test Python Check'
        super().__init__(self._header_title, level_index)

    def _run_class(self) -> None:
        pass

    def _set_class_result(self, status: Status, body: CheckBody) -> Status:
        status.set_na()
        body.append_text("Python check na'ed")


# -----------------#
# Collection check #
# -----------------#

class FakeCollectBaseCheck(CollectBaseCheck):
    def __init__(self, level_index=0):
        self._header_title = 'Test collection base check'
        super().__init__(self._header_title,  level_index)

    # @implement
    def run_checks(self) -> None:
        pass  # pragma: no cover


class FakeCollectDependCheck(CollectDependCheck):
    def __init__(self, level_index=0):
        self._header_title = 'Test collection depend check'
        super().__init__(self._header_title,  level_index)


class FakeCollectAllCheck(CollectAllCheck):
    def __init__(self, level_index=0):
        self._header_title = 'Test collection all check'
        super().__init__(self._header_title,  level_index)
