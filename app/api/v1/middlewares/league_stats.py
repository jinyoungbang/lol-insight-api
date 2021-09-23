from .league_timeline_parser import parse_data_from_timeline


def _calculate_kda(match_info):
    """Calculates and returns KDA."""

    kills = match_info["kills"]
    deaths = match_info["deaths"]
    assists = match_info["assists"]

    if deaths == 0:
        return kills + assists

    kda = (kills + assists)/deaths
    return round(kda, 2)


def _calculate_cs_per_min(match_info):
    """Calculates and returns CS per min."""

    neutral_minions_killed = match_info["neutralMinionsKilled"]
    total_minions_killed = match_info["totalMinionsKilled"]
    minions_killed = neutral_minions_killed + total_minions_killed
    minutes_played = match_info["timePlayed"] / 60
    return round(minions_killed / minutes_played, 2)


def _calculate_dmg_per_min(match_info):
    """Calculates and returns DMG per min."""

    total_damage_dealt_to_champions = match_info["totalDamageDealtToChampions"]
    minutes_played = match_info["timePlayed"] / 60
    return round(total_damage_dealt_to_champions / minutes_played, 0)


def _calculate_gpm(match_info: dict):
    """Calculates and returns Gold per min."""

    total_gold = match_info["goldEarned"]
    minutes_played = match_info["timePlayed"] / 60
    return round(total_gold / minutes_played, 0)


def _calculate_kill_participation(match_info: dict, participant_index: int):
    """Calculates user's kill participation of the game."""

    team_id = match_info["participants"][participant_index]["teamId"]
    kills = match_info["participants"][participant_index]["kills"]
    assists = match_info["participants"][participant_index]["assists"]

    total_team_kills = 0
    for team in match_info["teams"]:
        if team["teamId"] == team_id:
            total_team_kills = team["objectives"]["champion"]["kills"]
            break

    return round(((kills+assists) / total_team_kills)*100, 0)


def _calculate_damage_to_champion_percentage(match_info: dict, participant_index: int):
    team_id = match_info["participants"][participant_index]["teamId"]
    participant_dmg = match_info["participants"][participant_index]["totalDamageDealtToChampions"]
    team_total_dmg = 0

    for participant in match_info["participants"]:
        if participant["teamId"] == team_id:
            team_total_dmg += participant["totalDamageDealtToChampions"]

    return round((participant_dmg/team_total_dmg)*100, 0)


def return_insights(match_info: dict, timeline_info: dict, participant_index: int):
    """Returns user's statistics and insights of the match.
    """

    participant_match_info = match_info["participants"][participant_index]

    timeline_insights = parse_data_from_timeline(
        timeline_info, participant_index)

    match_insights = {
        "dpm": _calculate_dmg_per_min(participant_match_info),
        "kda": _calculate_kda(participant_match_info),
        "csPerMin": _calculate_cs_per_min(participant_match_info),
        "visionScore": participant_match_info["visionScore"],
        "visionWardsBought": participant_match_info["visionWardsBoughtInGame"],
        "wardsKilled": participant_match_info["wardsKilled"],
        "wardsPlaced": participant_match_info["wardsPlaced"],
        "goldPerMin": _calculate_gpm(participant_match_info),
        "killParticipation": _calculate_kill_participation(match_info, participant_index),
        "dmgPercentage": _calculate_damage_to_champion_percentage(match_info, participant_index),
        "dmgDealtToObj": participant_match_info["damageDealtToObjectives"]
    }

    # Update all insights into main insights dict
    insights = {}
    insights.update(timeline_insights)
    insights.update(match_insights)

    return insights
