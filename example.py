import hierarchy


@hierarchy.skill
def move_objects(num_objects):
    for cnt in range(num_objects):
        move_obj(cnt)


# @hierarchy.skill
def move_obj(step_count):
    pick_obj(step_count)
    place_obj()


@hierarchy.skill
def pick_obj(_step_count):
    print(3)
    return 3


@hierarchy.skill
def place_obj():
    print(5)
    return 5


def main():
    move_objects(3)

# class Skill(object):
#     @staticmethod
#     def step(arg, cnt, ret_name, ret_val):
#         raise NotImplementedError
#
#
# class MoveObjs(Skill):
#     @staticmethod
#     def step(arg, cnt, ret_name, ret_val):
#         [num_steps] = arg
#         if cnt < num_steps:
#             return 'MoveObj', [cnt]
#         else:
#             return None, [cnt]
#
#
# class MoveObj(Skill):
#     @staticmethod
#     def step(arg, cnt, ret_name, ret_val):
#         # [step_count] = arg
#         # if cnt == 0:
#         #     return 'PickObj', arg
#         # elif cnt == 1:
#         #     return 'PlaceObj', None
#         # else:  # cnt == 2
#         #     return None, None
#         return [
#             ('PickObj', arg),
#             ('PlaceObj', None),
#             (None, None),
#         ][cnt]
#
#
# class PickObj(Skill):
#     @staticmethod
#     def step(arg, cnt, ret_name, ret_val):
#         return None, [3]
#
#
# class PlaceObj(Skill):
#     @staticmethod
#     def step(arg, cnt, ret_name, ret_val):
#         return None, [5]
