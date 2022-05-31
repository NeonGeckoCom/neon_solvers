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
from unittest.mock import Mock

from neon_solvers import AbstractSolver


class MySolver(AbstractSolver):
    def __init__(self):
        # set the "internal" language, defined by dev, not user
        # this plugin only accepts and outputs english
        config = {"lang": "en"}
        super(MySolver, self).__init__(name="MySolver", priority=100,
                                       config=config)

    # expected solver methods to be implemented
    def get_data(self, query, context):
        """
        query assured to be in self.default_lang
        return a dict response
        """
        return {"error": "404 answer not found"}

    def get_image(self, query, context=None):
        """
        query assured to be in self.default_lang
        return path/url to a single image to acompany spoken_answer
        """
        return "http://stock.image.jpg"

    def get_spoken_answer(self, query, context=None):
        """
        query assured to be in self.default_lang
        return a single sentence text response
        """
        return "The full answer is XXX"

    def get_expanded_answer(self, query, context=None):
        """
        query assured to be in self.default_lang
        return a list of ordered steps to expand the answer, eg, "tell me more"

        {
            "title": "optional",
            "summary": "speak this",
            "img": "optional/path/or/url
        }
        :return:
        """
        steps = [
            {"title": "the question", "summary": "we forgot the question", "image": "404.jpg"},
            {"title": "the answer", "summary": "but the answer is 42", "image": "42.jpg"}
        ]
        return steps


class TestSolverBaseMethods(unittest.TestCase):
    def test_internal_cfg(self):
        solver = MySolver()
        self.assertEqual(solver.default_lang, "en")

    def test_get_spoken(self):
        solver = MySolver()
        solver.get_spoken_answer = Mock()
        solver.get_spoken_answer.return_value = "42"

        solver.spoken_cache.clear()
        ans = solver.spoken_answer("some query")
        solver.get_spoken_answer.assert_called()

    def test_get_expanded(self):
        solver = MySolver()
        solver.cache.clear()
        solver.get_expanded_answer = Mock()
        solver.get_expanded_answer.return_value = []

        ans = solver.long_answer("some query")
        solver.get_expanded_answer.assert_called()

    def test_get_image(self):
        solver = MySolver()
        solver.cache.clear()
        solver.get_image = Mock()
        solver.get_image.return_value = "42.jpeg"

        ans = solver.visual_answer("some query")
        solver.get_image.assert_called()

    def test_get_data(self):
        solver = MySolver()
        solver.cache.clear()
        solver.get_data = Mock()
        solver.get_data.return_value = {}

        ans = solver.search("some query")
        solver.get_data.assert_called()

    def test_get_spoken_cache(self):
        solver = MySolver()
        solver.spoken_cache.clear()
        solver.get_spoken_answer = Mock()
        solver.get_spoken_answer.return_value = "42"

        ans = solver.spoken_answer("some query")
        solver.get_spoken_answer.assert_called()

        # now test that the cache is loaded and method not called again
        solver.get_spoken_answer = Mock()
        solver.get_spoken_answer.return_value = "42"
        ans = solver.spoken_answer("some query")
        solver.get_spoken_answer.assert_not_called()

        # clear cache, method is called again
        solver.spoken_cache.clear()
        ans = solver.spoken_answer("some query")
        solver.get_spoken_answer.assert_called()

    def test_get_data_cache(self):
        solver = MySolver()
        solver.cache.clear()
        solver.get_data = Mock()
        solver.get_data.return_value = {"dummy": "42"}

        ans = solver.search("some query")
        solver.get_data.assert_called()

        # now test that the cache is loaded and method not called again
        solver.get_data = Mock()
        solver.get_data.return_value = {"dummy": "42"}
        ans = solver.search("some query")
        solver.get_data.assert_not_called()

        # clear cache, method is called again
        solver.cache.clear()
        ans = solver.search("some query")
        solver.get_data.assert_called()

    def test_translation(self):
        solver = MySolver()
        solver.translator.translate = Mock()
        solver.translator.translate.return_value = "a wild translation appears"

        # no translation
        ans = solver.spoken_answer("some query")
        solver.translator.translate.assert_not_called()

        # translation
        ans = solver.spoken_answer("not english", context={"lang": "unk"})
        solver.translator.translate.assert_called()
