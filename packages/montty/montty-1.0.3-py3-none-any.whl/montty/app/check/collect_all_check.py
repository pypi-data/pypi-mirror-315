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

from montty.app.check.collect_base_check import CollectBaseCheck
from montty.app.status import Status


class CollectAllCheck(CollectBaseCheck):
    # @implement
    def run_checks(self) -> None:
        ''' Run all of a collection of checks, irrespective of previous checks 
            status in the collection

            NOTE: A check status of NA is not allowed'''

        # Process checks

        for check in super().get_checks():
            check.run()
            status_result: Status = check.get_status()
            if status_result.is_na():
                raise ValueError(
                    "Check status cannot be NA, must be either OKAY or WARN or ALERT")

            super().get_status().merge(status_result)
            self._body.append_header(check.get_header())
            self._body.append_body(check.get_body())
