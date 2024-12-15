import asyncio # For async functions
import aiohttp  # For async HTTP requests
import json # For JSON parsing
import re # For regex
from aiohttp.client_exceptions import ClientError # For handling exceptions

# Constants
RETY_LIMIT = 3 # Number of times to retry a request

def convert_view_count(view_count):
    """ Convert Youtube View Count to an integer """

    if not isinstance(view_count, str):
        return 0
    try:
        number_str = re.sub("[^0-9KkMmBbTt,.]", "", view_count)

        if "K" in number_str or "k" in number_str:
            return int(float(number_str.replace("K", "").replace("k", "")) * 1000)
        elif "M" in number_str or "m" in number_str:
            return int(float(number_str.replace("M", "").replace("m", "")) * 1000000)
        elif "B" in number_str or "b" in number_str:
            return int(float(number_str.replace("B", "").replace("b", "")) * 1000000000)
        elif "T" in number_str or "t" in number_str:
            return int(float(number_str.replace("T", "").replace("t", "")) * 1000000000000)
        else:
            return int(float(number_str.replace(",", "")))
    except ValueError:
        pass
    return 0

async def error_handling(session, url, retries=RETY_LIMIT):
    """ Handle errors in async requests """

    for _ in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        except(ClientError, asyncio.TimeoutError):
            await asyncio.sleep(1)
    return None

async def _fetch_view_count(title, artist = ""):
    """ Fetch the view count of a Youtube video """

    # Preprocess inputs (Remove special characters)
    if not isinstance(title, str):
        title = str(title)
    if not isinstance(artist, str):
        artist = str(artist)
    
    title = re.sub("[^\w\s]", "", title)
    artist = re.sub("[^\w\s]", "", artist)

    search_query = f"{title} {artist}".strip()
    search_query = "+".join(search_query.split())
    
    if not search_query:
        return 0
    
    url = f"https://www.youtube.com/results?search_query={search_query}"

    async with aiohttp.ClientSession() as session:
        page_text = await error_handling(session, url)
        if page_text is None or 'var ytInitialData = ' not in page_text:
            return 0
        
        #Extract the json data from the page
        try:
            data_str = page_text.split('var ytInitialData = ', 1)[1].split(';</script>', 1)[0]
            data = json.loads(data_str)
        except (json.JSONDecodeError, IndexError):
            return 0
                # Parse for the first video view count
        try:
            results_data = data['contents']['twoColumnSearchResultsRenderer']['primaryContents'][
                'sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        except KeyError:
            return 0

        for item in results_data:
            if 'videoRenderer' in item:
                video_info = item['videoRenderer']
                view_count_text = video_info.get('viewCountText', {}).get('simpleText', '0')
                return convert_view_count(view_count_text)

    # If no video found
    return 0

def get_youtube_view_count(title: str, artist: str = "") -> int:
    """
    Get the view count of the first YouTube video matching the given title and optional artist.

    Parameters:
        title (str): The title of the song/video.
        artist (str, optional): The artist of the song. Defaults to "".

    Returns:
        int: The integer view count of the first matching YouTube video. Returns 0 if not found.
    """
    return asyncio.run(_fetch_view_count(title, artist))