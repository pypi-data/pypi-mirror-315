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

#
# Dependencies:
#
#     CHECKS/PYTHON_LIBS/system_data.py
#
# Description:
#
#     Collect all based check, uses Python sub-checks which are in
#         a package under PYTHON_LIBS
#

from system_data import SystemCpuDataCheck
from system_data import SystemMemDataCheck
from system_data import SystemDiskDataCheck
from system_data import SystemNetDataCheck
from system_data import SystemBootDataCheck
from montty.app.check.root_check import RootCheck
from montty.app.check.collect_all_check import CollectAllCheck


class CheckHostCpuEtc(RootCheck, CollectAllCheck):
    def __init__(self):
        header_title = 'chk_003_cla_python_host_cpu_etc.py- HOST CPU ETC.'
        super().__init__(header_title, level_index=0)

        # You can add 1 or more filter checks if you want
        # super().add_filter_check(FilterCheck())

        super().add_check(SystemCpuDataCheck())
        super().add_check(SystemMemDataCheck())
        super().add_check(SystemDiskDataCheck())
        super().add_check(SystemNetDataCheck())
        super().add_check(SystemBootDataCheck())
