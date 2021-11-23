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