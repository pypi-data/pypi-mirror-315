import pytest

from makefilename import make_filename


@pytest.fixture
def examples() -> list:
    return [
        ("Team Fortress 2", "Team_Fortress_2"),
        ("Dota 2", "Dota_2"),
        ("Counter-Strike 2", "Counter_Strike_2"),
        ("Sid Meier's Civilization® IV", "Sid_Meiers_Civilization_IV"),
        ("Civilization IV®: Warlords", "Civilization_IV_Warlords"),
        ("Civilization IV: Beyond the Sword", "Civilization_IV_Beyond_the_Sword"),
        ("Sid Meier's Civilization® V", "Sid_Meiers_Civilization_V"),
        ("Sid Meier's Civilization IV: Colonization", "Sid_Meiers_Civilization_IV_Colonization"),
        ("Majesty Gold HD", "Majesty_Gold_HD"),
        ("Assassin's Creed 2", "Assassins_Creed_2"),
        ("From Dust", "From_Dust"),
        ("Tropico Reloaded", "Tropico_Reloaded"),
        ("Time of Shadows", "Time_of_Shadows"),
        ("Patrician III", "Patrician_III"),
        ("The Great Art Race", "The_Great_Art_Race"),
        ("Broken Sword 2 - the Smoking Mirror: Remastered (2010)", "Broken_Sword_2_the_Smoking_Mirror_Remastered_2010"),
        ("Broken Sword 3 - the Sleeping Dragon (2003)", "Broken_Sword_3_the_Sleeping_Dragon_2003"),
        ("Crash Time 3", "Crash_Time_3"),
        ("Puzzler World", "Puzzler_World"),
        ("Ziro", "Ziro"),
        ("Disciples III - Renaissance Steam Special Edition", "Disciples_III_Renaissance_Steam_Special_Edition"),
    ]


def test_make_filename(examples) -> None:
    for example in examples:
        assert make_filename(example[0]) == example[1]