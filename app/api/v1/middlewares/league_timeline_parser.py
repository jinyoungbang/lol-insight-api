def parse_data_from_timeline(data: dict, participant_index: int):
    """Parses out specific information from match timeline data."""
    frames = data["info"]["frames"]

    if len(frames) <= 15:
        frame_at_15 = data["info"]["frames"][-1]
    else:
        frame_at_15 = data["info"]["frames"][15]
    participant_frames_at_15 = frame_at_15["participantFrames"]

    # Add one from idx as timeline data's index starts from 1
    participant_index += 1
    # Finds out participants index for same role
    if participant_index < 6:
        opponent_index = participant_index + 5
    else:
        opponent_index = participant_index - 5

    # Parse out stats for same role
    participant_frame_stats = participant_frames_at_15[str(participant_index)]
    opponent_frame_stats = participant_frames_at_15[str(opponent_index)]

    gd_at_15 = participant_frame_stats["totalGold"] - \
        opponent_frame_stats["totalGold"]
    xpd_at_15 = participant_frame_stats["xp"] - opponent_frame_stats["xp"]
    csd_at_15 = (participant_frame_stats["jungleMinionsKilled"] +
                 participant_frame_stats["minionsKilled"]) - (opponent_frame_stats["jungleMinionsKilled"] +
                                                              opponent_frame_stats["minionsKilled"])
    return {
        "gd@15": gd_at_15,
        "xpd@15": xpd_at_15,
        "csd@15": csd_at_15
    }
