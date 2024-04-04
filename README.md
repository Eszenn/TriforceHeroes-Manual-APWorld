# TriforceHeroes-Manual-APWorld
A manual APWorld for implementing The Legend of Zelda: Triforce Heroes into the Archipelago randomizer.

## Prerequisites
Proper usage of this APWorld requires a save file that has beaten the game and unlocked all outfits.
You do NOT need to clear all Drablands Challenges, though it is advised to do so if you plan to play
with them enabled.

## Locations
The following are all locations that must be checked:
- Every stage completion
- Every chest within levels (excluding stage rewards)
- Completing Drablands Challenges (optional)

## Items to be Received
The following are all items that may be received:
- Every outfit (except the Hero's Tunic)
- Regions
- Weapons
- The Lady's Materials
- Stage Skips

## Goals
### Free Princess Styla from her curse
Requires obtaining Sky Realm and 3 weapons to defeat Lady Maud in Sky Temple, as well as all 3 of the
Lady's Materials to "craft" the Lady's Ensemble.
  - This adds all 3 Lady's Materials into the item pool, and removes the Lady's Ensemble from the item pool.
    The Lady's Ensemble will be available for use once all 3 Lady's Materials have been acquired.
  - Other goals do not add the Lady's Materials, and instead the Lady's Ensemble is another item that can be received.
### Defeat all bosses
Requires obtaining all 8 areas and weapons to defeat the final boss of each area.
### Clear the Den of Trials
Requires obtaining the Den of Trials and all 8 weapons.
  - Adds the Den of Trials area into the item pool.

## Custom YAML Options
### Goal
Sets the goal for your world to one of the three mentioned above
### Random Starting Region
Start in a random area with all the weapons present in that area.
Possible starting areas area:
- Woodlands (Bow and Bomb)
- Riverside (Bow, Gripshot, and Water Rod)
- Volcano (Boomerang, Bow, and Gust Jar)
- Ice Cavern (Boomerang, Fire Gloves, Magic Hammer)

The other 4 areas are not included in this list simply because they have too many weapons required to full clear the area. 
### Include Drablands Challenges
If enabled, completing Drablands Challenge are valid checks
