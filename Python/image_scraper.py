# Brodie Davis
# Written on Dec 2016 for Python 3
# Image Scraper - Download images from bing search based on a search term. Bing API key required.
# SEE https://azure.microsoft.com/en-us/free/ for a Bing API key
# Designed to download new, random wallpapers :)
#
import http.client
from urllib import parse, request, error
from json import loads

# Change query here if running this script directly
# Should change to accepting CLI args
SEARCH = {
    'search_term': "Cat Desktop Backgrounds",  # Terms to search Bing search engine for
    'count': 50,      # Number of pics to return from search
    'offset': 0,      # Number of search results to skip before returning results
    'min_width': 0,   # Minimum width  of pic, in pixels
    'min_height': 0,  # Minimum height of pic, in pixels
    'safe_search': 'Moderate',  # Strict, Moderate, Off
    'subscription_key': ''  # Subscription key for Bing API
}
TARGET_DIR = ''  # Optional directory to save images to. Relative or absolute, no trailing slash, ex. /tmp/images
SPACE_CHAR = '_'       # Choose what to replace spaces in the filename with. Make this a space to not replace them
VERBOSITY = 'warn'     # Can be 'Error', 'Warn', or 'Info' (In order of increasing Verbosity)


def search_bing_images(query, subscription_key, count=35, offset=0, mkt='en-US', safe_search='Moderate'):
    #
    # SEE https://azure.microsoft.com/en-us/free/ for an API key
    #
    # https://dev.cognitive.microsoft.com/docs/services/56b43f0ccf5ff8098cef3808/operations/56b4433fcf5ff8098cef380c
    # q string
    # The user's search query string
    #
    # count (optional) number
    # The number of image results to return in the response. The actual number delivered may be less than requested.
    #
    # offset (optional) number
    # The zero-based offset that indicates the number of image results to skip before returning results.
    #
    # mkt (optional) string
    # The market where the results come from. Typically, this is the country where the user is making the request from;
    # however, it could be a different country if the user is not located in a country where Bing delivers results.
    # The market must be in the form -. For example, en-US.
    #
    # Full list of supported markets:
    # es-AR,en-AU,de-AT,nl-BE,fr-BE,pt-BR,en-CA,fr-CA,es-CL,da-DK,fi-FI,fr-FR,de-DE,zh-HK,en-IN,en-ID,en-IE,it-IT,ja-JP,
    # ko-KR,en-MY,es-MX,nl-NL,en-NZ,no-NO,zh-CN,pl-PL,pt-PT,en-PH,ru-RU,ar-SA,en-ZA,es-ES,sv-SE,fr-CH,de-CH,zh-TW,tr-TR,
    # en-GB,en-US,es-US
    #
    # safeSearch (optional) string
    # A filter used to filter results for adult content.
    #
    # RETURNS: A python dictionary of the data

    # Error Handling :/
    if not subscription_key:
        raise ValueError("Must provide a Bing search API subscription key!")
    if safe_search.lower() not in ['moderate', 'strict', 'off']:
        raise ValueError("SafeSearch value of \"{}\" is not valid!".format(safe_search))
    if not count > 0:
        raise ValueError("count must be greater than 0")
    if offset < 0:
        raise ValueError("offset must be not be negative")
    headers = {
        # Request headers
        'Content-Type': 'multipart/form-data',
        'Ocp-Apim-Subscription-Key': '{sub_key}'.format(sub_key=subscription_key)
    }
    params = parse.urlencode({
        'q': query,
        'count': count,
        'offset': offset,
        'mkt': mkt,
        'safeSearch': safe_search
    })

    conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
    conn.request("POST", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    pydata = loads(data.decode())  # parse the JSON with json.loads
    return pydata

def normalize(s):
    # Necessary to dispose of undesirable chars like '|' in file-names
    from string import ascii_letters, digits
    output = ''
    isSpace = False
    for char in s.strip():
        if char in ascii_letters or char in digits:
            isSpace = False
            output += char
        elif char == ' ' and not isSpace:
            isSpace = True  # eliminate multiple space chars in a row
            output += SPACE_CHAR
    return output.strip('_')  # we strip here incase we removed a character at the end of a string


def download_image(url, name, file_format, target_directory=None):
    file_format = 'jpg' if file_format == 'jpeg' else file_format
    try:
        if target_directory:  # save to a target directory if defined
            from os import path
            if not path.isdir(target_directory):  # Check of target dir exists first
                raise FileNotFoundError('Target directory not found: "{}"'.format(target_directory))
            request.urlretrieve(url, "{dir}/{name}.{format}".format(dir=target_directory,
                                                                    name=name, format=file_format))
        else:
            request.urlretrieve(url, "{name}.{format}".format(name=name, format=file_format))
    except error.HTTPError:
        print('Permission Denied! Continuing...')


if __name__ == "__main__":

    search_data = search_bing_images(SEARCH['search_term'], SEARCH['subscription_key'], count=SEARCH['count'],
                                     offset=SEARCH['offset'], safe_search=SEARCH['safe_search'])

    if search_data is None:
        print("Search failed! Exiting...")
        exit(1)

    results = search_data['value']  # Get search results from JSON data
    LIMIT = SEARCH['count'] if SEARCH['count'] < len(results) else len(results)  # max num of pics to download

    for i in range(0, LIMIT):
        # Get metadata for the current image 'i'
        img_name = normalize(results[i]['name'])
        img_size = results[i]['contentSize']
        img_format = results[i]['encodingFormat']
        img_height = results[i]['height']
        img_width = results[i]['width']
        img_url = results[i]['contentUrl']
        if VERBOSITY.lower() == 'info':
            # Verbose mode: Print metadata for each image to the screen
            # This could be better done with python logging
            print('\n\nNAME:"{name}"\n\tSIZE: {size}\n\tFORMAT: {format}\n\t'
                  'HEIGHT: {height}\n\tWIDTH: {width}'.format(
                    name=img_name,
                    size=img_size,
                    format=img_format,
                    height=img_height,
                    width=img_width
                    ))
        if img_height < SEARCH['min_height'] or img_width < SEARCH['min_width']:
            if VERBOSITY.lower() == 'warn' or VERBOSITY.lower() == 'info':  # Yup, definitely better with python logging
                print("Image is {img_x}x{img_y}, but min is {min_x}x{min_y}, skipping..." .format(
                    img_x=img_width,
                    img_y=img_height,
                    min_x=SEARCH['min_width'],
                    min_y=SEARCH['min_height']
                ))
            continue
        download_image(url=img_url, name=img_name, file_format=img_format, target_directory=TARGET_DIR)

    print("Received {} results from an estimated {}".format(len(results), search_data['totalEstimatedMatches']))
