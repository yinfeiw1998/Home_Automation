@Skill
def moveObject():
    print("move Object")
    moveEverything()

def moveEverything():
    print("move Everything")
    moveTable()
    moveChair()
    moveCups()

@Skill
def moveTable():
    print("move table")

@Skill
def moveChair():
    print("move chair")

@Skill
def moveCups():
    print("move Cups")


def test():
    moveObject()