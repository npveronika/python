from atomix_class import *

# D:\Home\Veronika\python\atomix>python -m pytest atomix_test.py -vv -x



class MockView:
    def __init__(self):
        self.calls = ""
    def draw_background(self, i, j):
        self.calls = 'draw_background'
    def draw_wall(self, i, j):
        self.calls = 'draw_wall'


class TestModel:

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.view = MockView()
        self.direct = ""
        self.mol = list()
        self.molecule = list()

    def test_draw_background_model(self):
        self.model = Model([[BG]], self.mol, self.direct, self.molecule, self.view)
        self.model.draw_background_model()
        assert self.view.calls == "draw_background"

    def test_draw_wall_model(self):
        self.model = Model([[W]], self.mol, self.direct, self.molecule, self.view)
        self.model.draw_wall_model()
        assert self.view.calls == "draw_wall"

    def test_draw_atom(self):
        pass

    def test_model_class_init_func(self):
        test_cursor = Cursor()
        assert test_cursor.i == 1

