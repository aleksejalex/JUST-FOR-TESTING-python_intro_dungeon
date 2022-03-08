import subprocess
from dungeon import Dungeon


if __name__ == "__main__":
    # create dungeon
    hero_name = input("What is your hero name?")
    dungeon = Dungeon((10, 20), 40, hero_name)
    dungeon.create_dungeon()
    while True:
        subprocess.Popen("cls", shell=True).communicate()
        print(dungeon)
        action = input("Select an action {}> (L)EFT,"
                       " (R)IGHT, (U)P, (D)OWN, (S)SEARCH, (A)TTACK, (Q)UIT: ".format(hero_name))
        if action != "Q":
            dungeon.hero_action(action)
        else:
            print("You coward!")
            exit(0)



