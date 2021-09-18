def return_kda(match_info):
    kills = match_info["kills"]
    deaths = match_info["deaths"]
    assists = match_info["assists"]

    if deaths == 0:
        return kills + assists

    kda = (kills + assists)/deaths
    return round(kda, 2)


def return_cs_per_min(match_info):
    neutral_minions_killed = match_info["neutralMinionsKilled"]
    total_minions_killed = match_info["totalMinionsKilled"]
    minions_killed = neutral_minions_killed + total_minions_killed
    minutes_played = match_info["timePlayed"] / 60
    return round(minions_killed / minutes_played, 2)


def return_dmg_per_min(match_info):
    total_damage_dealt_to_champions = match_info["totalDamageDealtToChampions"]
    minutes_played = match_info["timePlayed"] / 60
    return round(total_damage_dealt_to_champions / minutes_played, 0)


def return_match_insight(match_info):
    """
    TODO:
    - Gold Per Min (GPM)
    - DMG%
    - Solo Kills
    - Kill Participation (KP)
    - CS Difference @ 15 (CSD@15)
    - XP Difference @ 15 (XPD@15)
    - Gold Difference @ 15 (GD@15)
    """
    return {
        "dpm": return_dmg_per_min(match_info),
        "kda": return_kda(match_info),
        "csPerMin": return_cs_per_min(match_info),
        "visionScore": match_info["visionScore"],
        "visionWardsBought": match_info["visionWardsBoughtInGame"],
        "wardsKilled": match_info["wardsKilled"],
        "wardsPlaced": match_info["wardsPlaced"]
    }
