#__init__.py
from envs import dishes
from envs import pyramid

def catalog(name):
    return {
        'dishes': dishes.DishesEnv, 
        'pyramid': pyramid.PyramidEnv,
    }[name]()