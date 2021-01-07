#__init__.py

def catalog(name):
    return {
        'dishes': dishes.DishesEnv, 
        'pyramid': pyramid.PyramidEnv,
    }[name]()