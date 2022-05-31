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

from neon_solver_ddg_plugin import DDGSolver
from neon_solver_wolfram_alpha_plugin import WolframAlphaSolver
from neon_solver_wikipedia_plugin import WikipediaSolver
from neon_solver_wordnet_plugin import WordnetSolver


def en():
    d = WordnetSolver()
    for sentence in d.spoken_answers("what is the definition of computer"):
        print(sentence)
        # a machine for performing calculations automatically

    d = WikipediaSolver()
    for sentence in d.spoken_answers("what is the speed of light"):
        print(sentence)
        break
        # The speed of light in vacuum, commonly denoted c, is a universal physical constant important in many areas of physics.

    d = WolframAlphaSolver()
    for sentence in d.spoken_answers("what is the speed of light"):
        print(sentence)
        # The speed of light has a value of about 300 million meters per second

    d = DDGSolver()
    for sentence in d.spoken_answers("who is Isaac Newton"):
        print(sentence)
        break
        # Sir Isaac Newton was an English mathematician, physicist, astronomer, theologian, and author widely recognised as one of the greatest mathematicians, physicists, and most influential scientists of all time.


def pt():
    d = WordnetSolver()
    for sentence in d.spoken_answers("qual é a definição de computador", lang="pt"):
        print(sentence)
        # uma máquina para realizar cálculos automaticamente

    d = WolframAlphaSolver()
    for sentence in d.spoken_answers("qual é a velocidade da luz", lang="pt"):
        print(sentence)
        # A velocidade da luz tem um valor de cerca de 300 milhões de metros por segundo

    d = WikipediaSolver()
    for sentence in d.spoken_answers("qual é a velocidade da luz", lang="pt"):
        print(sentence)
        break
        # A velocidade da luz no vácuo, comumente denotada c, é uma constante física universal importante em muitas áreas da física

    d = DDGSolver()
    for sentence in d.spoken_answers("Quem é Isaac Newton", lang="pt"):
        print(sentence)
        break
        # Sir Isaac Newton foi um matemático inglês, físico, astrônomo, teólogo e autor amplamente reconhecido como um dos maiores matemáticos, físicos e cientistas mais influentes de todos os tempos

en()
pt()