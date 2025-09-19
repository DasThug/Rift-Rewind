import requests

RIOT_API_KEY = ""

RIOT_HEADERS = {
    "region": "europe"
}

def get_riot_by_name(gamename, tag, api_key):
    """
    Args:
        gamename (str): The name of the game.
        tag (str): The user's tag in the game.
        api_key (str): Active Riot Developer API key

    Returns:
        str: The unique identifier (PUUID) for the user, or None if not found or error occurs.
    Note:
        If the gamename contains spaces, they must be replaced with '%20' for the API request.
        Example: gamename: Das‰20Thug (space characters must be rewritten to: %20 )
    """

    if " " in gamename:
        gamename = gamename.replace(" ", "%20")
    
    try:
        url = f"https://{RIOT_HEADERS['region']}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gamename}/{tag}?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for 4xx or 5xx

        data = response.json()
        puuid = data.get("puuid")
        if puuid:
            return puuid
        else:
            print(f"[Error] PUUID not found in response for {gamename}#{tag}. Full response: {data}")
            return None

    except requests.exceptions.HTTPError:
        # If the API returned an error status
        try:
            error_data = response.json()
            error_message = error_data.get("message", response.text)
        except ValueError:
            error_message = response.text
        print(f"[Error] API error for {gamename}#{tag}: {error_message}")
    
    except requests.exceptions.RequestException as e:
        # Covers all network-related exceptions (timeout, DNS failure, etc.)
        print(f"[Error] Network error while fetching Riot ID for {gamename}#{tag}: {e}")

    except Exception as e:
        # Catches anything else unexpected
        print(f"[Error] Unexpected error while fetching Riot ID for {gamename}#{tag}: {e}")

    return None  


def get_name_by_riot(riot_id, api_key):
    """
    Args:
        riot_id (str): The unique identifier for the user.
        api_key (str): Active Riot Developer API key

    Returns:
        tuple: A tuple containing:
            - game_name (str): The name of the game.
            - game_tag (str): The user's tag in the game.
    """
    try:
        url = f"https://{RIOT_HEADERS['region']}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{riot_id}?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise error for 4xx or 5xx

        data = response.json()
        game_name = data.get("gameName")
        game_tag = data.get("tagLine")

        if game_name and game_tag:
            return (game_name, game_tag)
        else:
            print(f"[Error] Missing name or tag in response for Riot ID {riot_id}. Full response: {data}")
            return None

    except requests.exceptions.HTTPError:
        try:
            error_data = response.json()
            error_message = error_data.get("message", response.text)
        except ValueError:
            error_message = response.text
        print(f"[Error] API error for Riot ID {riot_id}: {error_message}")

    except requests.exceptions.RequestException as e:
        print(f"[Error] Network error while fetching name for Riot ID {riot_id}: {e}")

    except Exception as e:
        print(f"[Error] Unexpected error while fetching name for Riot ID {riot_id}: {e}")

    return None


def get_matches_by_id(riot_id, api_key, params=None):
    """
    Args:
        riot_id (str): The unique identifier for the user.
        api_key (str): Active Riot Developer API key
        params (dict, optional): Dictionary of query parameters to filter matches.
            Possible keys include:
                - startTime (long): Start time in epoch milliseconds.
                - endTime (long): End time in epoch milliseconds.
                - queue (int): Queue ID to filter by specific game modes.
                - type (str): Type of match (e.g., "ranked", "normal").
                - start (int): Index of the first match to return (for pagination).
                - count (int): Number of matches to return (max 100).
            If None, no filters are applied and all matches are returned.
    Returns:
        list: A list of match IDs.
    """

    params = {
            "startTime" : None,
            "endTime" : None,
            "queue" : None,
            "type" : None,
            "start" : None,
            "count" : None
        } 

    try:
        url = f"https://{RIOT_HEADERS['region']}.api.riotgames.com/lol/match/v5/matches/by-puuid/{riot_id}/ids?"
        if params == None:
            url = url + f"api_key={api_key}"
        else:
            for parameter, value in params.items():
                url = url + f"{parameter}{value}&"

            url = url + f"api_key={api_key}"

        response = requests.get(url)
        response.raise_for_status()  # Raise error for 4xx or 5xx
        data = response.json()
        return data

    except requests.exceptions.HTTPError:
        try:
            error_data = response.json()
            error_message = error_data.get("message", response.text)
        except ValueError:
            error_message = response.text
        print(f"[Error] API error for Riot ID {riot_id}: {error_message}")

    except requests.exceptions.RequestException as e:
        print(f"[Error] Network error while fetching name for Riot ID {riot_id}: {e}")

    except Exception as e:
        print(f"[Error] Unexpected error while fetching name for Riot ID {riot_id}: {e}")

    return None 


def get_match_data(match_id, api_key):
    """
    Args:
        match_id (str): The unique identifier for the match.
        api_key (str): Active Riot Developer API key

    Returns:
        dict: A dictionary containing detailed match information.
    """
    try:
        url = f"https://{RIOT_HEADERS['region']}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise error for 4xx or 5xx

        data = response.json()
        return data

    except requests.exceptions.HTTPError:
        try:
            error_data = response.json()
            error_message = error_data.get("message", response.text)
        except ValueError:
            error_message = response.text
        print(f"[Error] API error for Match ID {match_id}: {error_message}")

    except requests.exceptions.RequestException as e:
        print(f"[Error] Network error while fetching data for Match ID {match_id}: {e}")

    except Exception as e:
        print(f"[Error] Unexpected error while fetching data for Match ID {match_id}: {e}")

    return None


def get_match_timeline(match_id, api_key):
    """
    Args:
        match_id (str): The unique identifier for the match.
        api_key (str): Active Riot Developer API key

    Returns:
        dict: A dictionary containing the match timeline data.
    """
    try:
        url = f"https://{RIOT_HEADERS['region']}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise error for 4xx or 5xx

        data = response.json()
        return data

    except requests.exceptions.HTTPError:
        try:
            error_data = response.json()
            error_message = error_data.get("message", response.text)
        except ValueError:
            error_message = response.text
        print(f"[Error] API error for Match ID {match_id}: {error_message}")

    except requests.exceptions.RequestException as e:
        print(f"[Error] Network error while fetching timeline for Match ID {match_id}: {e}")

    except Exception as e:
        print(f"[Error] Unexpected error while fetching timeline for Match ID {match_id}: {e}")

    return None

if __name__ == "__main__":
    RIOT_API_KEY = ""

    if not RIOT_API_KEY or not RIOT_API_KEY.startswith("RGAPI-"):
        RIOT_API_KEY = input("Enter your Riot API Key: ")

    id = get_riot_by_name("Das Thug","gyat", RIOT_API_KEY)
    print(get_matches_by_id(id, RIOT_API_KEY, None))
