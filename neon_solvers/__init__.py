from neon_solvers.solver import AbstractSolver


# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2021 Neongecko.com Inc.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions
#    and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
#    and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from ovos_plugin_manager.text_transformers import find_utterance_transformer_plugins, load_utterance_transformer_plugin
from ovos_utils.log import LOG


class NeonSolversService:
    def __init__(self, bus, config=None):
        self.config_core = config or {}
        self.loaded_modules = {}
        self.has_loaded = False
        self.bus = bus
        self.config = self.config_core.get("solvers") or {}
        self.load_plugins()

    def load_plugins(self):
        for plug_name, plug in find_utterance_transformer_plugins().items():
            if plug_name in self.config:
                try:
                    self.loaded_modules[plug_name] = plug()
                    LOG.info(f"loaded question solver plugin: {plug_name}")
                except Exception as e:
                    LOG.exception(f"Failed to load question solver plugin: {plug_name}")

    @property
    def modules(self):
        return self.loaded_modules.values()

    def shutdown(self):
        pass

    def spoken_answers(self, utterance, context=None):
        for module in self.modules:
            ans = module.spoken_answers(utterance, context)
            if ans:
                return ans
