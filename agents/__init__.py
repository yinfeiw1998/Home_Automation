#__init__.py

def catalog(name, env):
    return {
        'dishes': dishes.DishesAgent,
        'pyramid': pyramid.PyramidAgent,
    }[name](env)