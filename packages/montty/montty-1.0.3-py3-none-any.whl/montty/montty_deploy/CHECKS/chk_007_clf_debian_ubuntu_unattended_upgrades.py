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
#     BASH_SCRIPTS/mty_util/mtyhost.sh
#     BASH_SCRIPTS/mty_util/mtyservice.sh
#
# Description:
#
#     Check that the "Debian based" SystemD service - 'unattended-upgrades' is:
#         - Installed,
#         - Enabled,
#         - Active
#
#     $ sudo apt update
#     $ sudo apt dist-upgrade
#     $ sudo apt install unattended-upgrades
#

from montty.app.check.root_check import RootCheck
from montty.app.check.collect_depend_check import CollectDependCheck
from montty.app.check.bash_check import BashCheck


class CheckFilterUnattendedUpgrades(RootCheck, CollectDependCheck):
    def __init__(self):
        self._header_title = 'chk_007_clf_debian_ubuntu_unattended_upgrades.py - Check FILTER'
        super().__init__(self._header_title, level_index=0)

        super().add_filter_check(FilterCheck())
        super().add_check(CheckUnattendedUpgrades())


# --------------------------------------------------------------------
# Filter check
# --------------------------------------------------------------------

class FilterCheck(BashCheck):
    def __init__(self):
        header_title = ' (f) Filter DISTRO in "debian / ubuntu"'
        bash_script = 'mty_util/mtyhost.sh'
        arg1 = 'distro_in'
        arg2 = 'debian\nubuntu'
        super().__init__(header_title, bash_script, arg1, arg2, level_index=1)


# --------------------------------------------------------------------
# Unattened upgrades service
# --------------------------------------------------------------------

class CheckUnattendedUpgrades(BashCheck):
    def __init__(self):
        header_title = ' (f) Check Service - UNATTENDED UPGRADES'
        bash_script = 'mty_util/mtyservice.sh'
        arg1 = 'installed_enabled_active'
        arg2 = 'unattended-upgrades'
        super().__init__(header_title, bash_script, arg1, arg2, level_index=1)
