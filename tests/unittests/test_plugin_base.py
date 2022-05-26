import unittest

from neon_solvers import AbstractSolver


class MySolver(AbstractSolver):
    def __init__(self):
        # set the "internal" language, defined by dev, not user
        # this plugin only accepts and outputs english
        config = {"lang": "en"}
        super(MySolver, self).__init__(name="MySolver", priority=100,
                                       config=config)
        self.get_data_called = False
        self.get_image_called = False
        self.get_spoken_called = False
        self.get_expanded_called = False

    # expected solver methods to be implemented
    def get_data(self, query, context):
        """
        query assured to be in self.default_lang
        return a dict response
        """
        self.get_data_called = True
        return {"error": "404 answer not found"}

    def get_image(self, query, context=None):
        """
        query assured to be in self.default_lang
        return path/url to a single image to acompany spoken_answer
        """
        self.get_image_called = True
        return "http://stock.image.jpg"

    def get_spoken_answer(self, query, context=None):
        """
        query assured to be in self.default_lang
        return a single sentence text response
        """
        self.get_spoken_called = True
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
        self.get_expanded_called = True
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
        self.assertFalse(solver.get_data_called)
        self.assertFalse(solver.get_image_called)
        self.assertFalse(solver.get_spoken_called)
        self.assertFalse(solver.get_expanded_called)

        ans = solver.spoken_answer("some query")
        self.assertTrue(solver.get_spoken_called)
        self.assertFalse(solver.get_data_called)
        self.assertFalse(solver.get_image_called)
        self.assertFalse(solver.get_expanded_called)

    def test_get_expanded(self):
        solver = MySolver()
        self.assertFalse(solver.get_data_called)
        self.assertFalse(solver.get_image_called)
        self.assertFalse(solver.get_spoken_called)
        self.assertFalse(solver.get_expanded_called)

        ans = solver.long_answer("some query")
        self.assertFalse(solver.get_spoken_called)
        self.assertFalse(solver.get_data_called)
        self.assertFalse(solver.get_image_called)
        self.assertTrue(solver.get_expanded_called)

    def test_get_image(self):
        solver = MySolver()
        self.assertFalse(solver.get_data_called)
        self.assertFalse(solver.get_image_called)
        self.assertFalse(solver.get_spoken_called)
        self.assertFalse(solver.get_expanded_called)

        ans = solver.visual_answer("some query")
        self.assertFalse(solver.get_spoken_called)
        self.assertFalse(solver.get_data_called)
        self.assertTrue(solver.get_image_called)
        self.assertFalse(solver.get_expanded_called)

    def test_get_data(self):
        solver = MySolver()
        self.assertFalse(solver.get_data_called)
        self.assertFalse(solver.get_image_called)
        self.assertFalse(solver.get_spoken_called)
        self.assertFalse(solver.get_expanded_called)

        ans = solver.search("some query")
        self.assertFalse(solver.get_spoken_called)
        self.assertTrue(solver.get_data_called)
        self.assertFalse(solver.get_image_called)
        self.assertFalse(solver.get_expanded_called)