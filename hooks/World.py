# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from BaseClasses import MultiWorld, CollectionState
from worlds.AutoWorld import World
from .Options import RandomStartingRegion
# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value
# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem


# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#


########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names

    # Add your code here to calculate which locations to remove
    goal = get_option_value(multiworld, player, "goal")

    if goal == 0:
        locationNamesToRemove.append("Defeat all 8 Bosses")
        locationNamesToRemove.append("Clear the Den of Trials")

    elif goal == 1:
        locationNamesToRemove.append("Break the Curse on Princess Styla")
        locationNamesToRemove.append("Clear the Den of Trials")

    elif goal == 2:
        locationNamesToRemove.append("Break the Curse on Princess Styla")
        locationNamesToRemove.append("Defeat all 8 Bosses")

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names
    startingItems = []

    # Add your code here to calculate which items to remove.
    if is_option_enabled(multiworld, player, "random_starting_region"):
        regions = [key for key in RandomStartingRegion.regions.keys()]
        random_region = regions[world.random.randint(0, 3)]

        for item in item_pool:
            if item.name == random_region:
                itemNamesToRemove.append(random_region)
                startingItems.append(random_region)
                break

        for itemName in RandomStartingRegion.regions[random_region]["items"]:
            for item in item_pool:
                if item.name == itemName:
                    itemNamesToRemove.append(itemName)
                    startingItems.append(itemName)
                    break

    else:
        for item in item_pool:
            if item.name == "Woodlands":
                itemNamesToRemove.append("Woodlands")
                startingItems.append("Woodlands")
                break

        for itemName in RandomStartingRegion.regions["Woodlands"]["items"]:
            for item in item_pool:
                if item.name == itemName:
                    itemNamesToRemove.append(itemName)
                    startingItems.append(itemName)
                    break

    if is_option_enabled(multiworld, player, "random_starting_outfit"):
        random_outfit = world.random.randint(0, 37)
        outfits = ["Bear Minimum", "Big Bomb Outfit", "Boomeranger", "Cacto Clothes", "Cheer Outfit", "Cheetah Costume",
                   "Cozy Parka", "Cursed Tights", "Dapper Spinner", "Dunewalker Duds", "Energy Gear", "Fierce Deity Armor",
                   "Fire Blazer", "Goron Garb", "Gust Garb", "Hammerwear", "Hero's Tunic", "Jack of Hearts", "Kokiri Clothes",
                   "Legendary Dress", "Light Armor", "Linebeck's Uniform", "Lucky Loungewear", "Ninja Gi", "Queen of Hearts",
                   "Robowear", "Rupee Regalia", "Serpent's Toga", "Showstopper", "Spin Attack Attire", "Sword Master Suit",
                   "Sword Suit", "Timeless Tunic", "Tingle Tights", "Torrent Robe", "Tri Suit", "Zora Costume"]

        if get_option_value(multiworld, player, "goal") != 0:
            outfits.append("The Lady's Ensemble")

        startingItems.append(outfits[random_outfit])

    else:
        startingItems.append("Hero's Tunic")


    if get_option_value(multiworld, player, "goal") != 0:
        for item in item_pool:
            if item.name in ["Lady's Collar", "Lady's Glasses", "Lady's Parasol"]:
                itemNamesToRemove.append(item.name)

    else:
        itemNamesToRemove.append("Lady's Ensemble")

    if get_option_value(multiworld, player, "goal") != 2:
        for item in item_pool:
            if item.name == "Den of Trials":
                itemNamesToRemove.append("Den of Trials")

    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in startingItems:
        for item in item_pool:
            if item.name == itemName:
                multiworld.push_precollected(item)

    for itemName in itemNamesToRemove:
        for item in item_pool:
            if item.name == itemName:
                item_pool.remove(item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass
