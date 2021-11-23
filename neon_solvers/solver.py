# # NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# # All trademark and other rights reserved by their respective owners
# # Copyright 2008-2021 Neongecko.com Inc.
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
import xdg.BaseDirectory
from json_database import JsonStorageXDG
from ovos_plugin_manager.language import OVOSLangTranslationFactory
from quebra_frases import sentence_tokenize


class AbstractSolver:
    def __init__(self, name, priority=50, config=None):
        self.config = config or {}
        self.supported_langs = self.config.get("supported_langs") or []
        self.default_lang = self.config.get("lang", "en")
        if self.default_lang not in self.supported_langs:
            self.supported_langs.insert(0, self.default_lang)
        self.priority = priority
        self.translator = OVOSLangTranslationFactory.create()
        self.cache = JsonStorageXDG(name + "_data",
                                    xdg_folder=xdg.BaseDirectory.xdg_cache_home,
                                    subfolder="neon_solvers")
        self.spoken_cache = JsonStorageXDG(name,
                                    xdg_folder=xdg.BaseDirectory.xdg_cache_home,
                                    subfolder="neon_solvers")

    @staticmethod
    def sentence_split(text, max_sentences=25):
        return sentence_tokenize(text)[:max_sentences]

    def get_spoken_answer(self, query, context):
        raise NotImplementedError

    def get_data(self, query, context):
        return {"short_answer": self.get_spoken_answer(query, context)}

    # search api
    def search(self, query, context=None, lang=None):
        context = context or {}
        lang = lang or context.get("lang") or self.default_lang
        lang = lang.split("-")[0]
        user_lang = lang
        # translate input to English
        if user_lang not in self.supported_langs:
            lang = self.default_lang
            query = self.translator.translate(query, lang, user_lang)

        # read from cache
        if query in self.cache:
            data = self.cache[query]
        else:
            # search data
            try:
                context["lang"] = lang
                data = self.get_data(query, context)
            except:
                return {}

        # save to cache
        self.cache[query] = data
        self.cache.store()

        # translate english output to user lang
        if user_lang not in self.supported_langs:
            return self.translator.translate_dict(data, user_lang, lang)
        return data

    # spoken answers api
    def spoken_answers(self, query, context=None, lang=None):
        context = context or {}
        lang = lang or context.get("lang") or self.default_lang
        lang = lang.split("-")[0]
        user_lang = lang

        # translate input to English
        if user_lang not in self.supported_langs:
            lang = self.default_lang
            query = self.translator.translate(query, lang, user_lang)

        # get answer
        context["lang"] = lang
        if query in self.spoken_cache:
            # read from cache
            summary = self.spoken_cache[query]
        else:
            summary = self.get_spoken_answer(query, context)
            # save to cache
            self.spoken_cache[query] = summary
            self.spoken_cache.store()

        # summarize
        if summary:
            # translate english output to user lang
            if user_lang not in self.supported_langs:
                return [self.translator.translate(utt, user_lang, lang)
                        for utt in self.sentence_split(summary)]
            else:
                return self.sentence_split(summary)

    def shutdown(self):
        """ module specific shutdown method """
        pass
