# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, SpecialRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world. 
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith

class Goal(Choice):
    """
    The goal that must be achieved in order to mark your world as completed.
    Break Curse requires Sky Realm, any 3 weapons, and all 3 of the Lady's Materials.
    All Bosses requires all areas and all weapons.
    Den of Trials requires Den of Trials and all weapons.
    """
    display_name = "Goal"
    option_break_curse = 0
    option_all_bosses = 1
    option_den_of_trials = 2
    default = 0


class RandomStartingRegion(Toggle):
    """
    Start in a random starting region with all items for that region.
    Possible starting regions are: Woodlands, Riverside, Volcano, Ice Cavern.
    Woodlands starts with the Bow and Bombs.
    Riverside starts with the Bow, Gripshot, and Water Rod.
    Volcano starts with the Bow, Boomerang, and Gust Jar.
    Ice Cavern starts with the Boomerang, Fire Gloves, and Magic Hammer.
    """
    display_name = "Randomize starting region?"

    regions = {
        "Woodlands": {
            "items": ["Bow", "Bomb"]
        },
        "Riverside": {
            "items": ["Bow", "Water Rod", "Gripshot"]
        },
        "Volcano": {
            "items": ["Boomerang", "Bow", "Gust Jar"]
            },
        "Ice Cavern": {
            "items": ["Fire Gloves", "Boomerang", "Magic Hammer"]
        }
    }


# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["goal"] = Goal
    options["random_starting_region"] = RandomStartingRegion
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options