from instagram.SignupWithLogin import SignupWithLogin
from instagram.DefaultSignUp import DefaultSignUp

class WayFactory:
    ways = {
        "signupWithLogin": SignupWithLogin,
        "defaultSignUp": DefaultSignUp
    }

    def set_way(self, way, *args):
        way_class = self.ways.get(way, DefaultSignUp)
        return way_class(*args)