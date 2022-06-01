# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
from pprint import pprint

from lichecker import LicenseChecker

# these packages dont define license in setup.py
# manually verified and injected
license_overrides = {
    "kthread": "MIT",
    'yt-dlp': "Unlicense",
    'pyxdg': 'GPL-2.0',
    'ptyprocess': 'ISC license',
    'psutil': 'BSD3'
}
# explicitly allow these packages that would fail otherwise
whitelist = []

# validation flags
allow_nonfree = False
allow_viral = False
allow_unknown = False
allow_unlicense = True
allow_ambiguous = False

pkg_name = "neon_solvers"


class TestLicensing(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        licheck = LicenseChecker(pkg_name,
                                 license_overrides=license_overrides,
                                 whitelisted_packages=whitelist,
                                 allow_ambiguous=allow_ambiguous,
                                 allow_unlicense=allow_unlicense,
                                 allow_unknown=allow_unknown,
                                 allow_viral=allow_viral,
                                 allow_nonfree=allow_nonfree)
        print("Package", pkg_name)
        print("Version", licheck.version)
        print("License", licheck.license)
        print("Transient Requirements (dependencies of dependencies)")
        pprint(licheck.transient_dependencies)
        self.licheck = licheck

    def test_license_compliance(self):
        print("Package Versions")
        pprint(self.licheck.versions)

        print("Dependency Licenses")
        pprint(self.licheck.licenses)

        self.licheck.validate()
