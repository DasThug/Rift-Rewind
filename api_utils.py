import requests

RIOT_API_KEY = ""

RIOT_HEADERS = {
    "region": "europe"
}

def get_riot_by_name(gamename, tag, api_key):
    """
    gamename: Das‰20Thug (space characters must be rewritten to: %20 )
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




if __name__ == "__main__":
    RIOT_API_KEY = ""

    if not RIOT_API_KEY or not RIOT_API_KEY.startswith("RGAPI-"):
        RIOT_API_KEY = input("Enter your Riot API Key: ")

    id = get_riot_by_name("Das Thug","gyat", RIOT_API_KEY)
    # print(get_league_data_by_id(id, RIOT_API_KEY))
