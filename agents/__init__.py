#__init__.py
from agents import dishes
from agents import pyramid

def catalog(domain, task, data, teacher, env):
    return {
        'dishes': dishes.DishesAgent,
        'pyramid': pyramid.PyramidAgent,
    }[domain](domain, task, data, teacher, env)