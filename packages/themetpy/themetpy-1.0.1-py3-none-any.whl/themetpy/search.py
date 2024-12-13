# themetpy/search.py
# returns a listing of all Object IDs for objects that contain the search query within the object’s data

import requests
import logging

logger = logging.getLogger(__name__)

def search(query, isHighlight=None, title=None, tags=None, departmentId=None, 
           isOnView=None, artistOrCulture=None, medium=None, hasImages=None, 
           geoLocation=None, dateBegin=None, dateEnd=None):
    """
    Perform a search across The Met's collection.

    Parameters:
    -----------
        query (str): Search term.
        isHighlight (bool, optional): Filter by highlighted artworks.
        title (bool, optional): Search within titles.
        tags (bool, optional): Search within subject keyword tags.
        departmentId (int, optional): Filter by department ID.
        isOnView (bool, optional): Filter by objects currently on view.
        artistOrCulture (bool, optional): Search within artist name or culture fields.
        medium (str, optional): Filter by medium or object type (multiple values separated by '|').
        hasImages (bool, optional): Filter by objects that have images.
        geoLocation (str, optional): Filter by geographic location (multiple values separated by '|').
        dateBegin (int, optional): Start year for date range.
        dateEnd (int, optional): End year for date range.

    Returns:
    --------
        list: A list of Object IDs matching the search criteria.
    
    Examples:
    ---------
    >>> from themetpy.search import search
    >>> # Perform a basic search for 'sunflowers'
    >>> results = search(query="sunflowers")
    >>> print(results[:5])  # Display first 5 Object IDs
    [436524, 484935, 437112, 210191, 431264]

    >>> # Perform an advanced search with multiple filters
    >>> advanced_results = search(
    ...     query="sunflowers",
    ...     isHighlight=True,
    ...     medium="Paintings",
    ...     hasImages=True,
    ...     dateBegin=1850,
    ...     dateEnd=1900
    ... )
    >>> print(f"Found {len(advanced_results)} objects matching the search criteria.")
    >>> print(advanced_results)
    Found 2 objects matching the search criteria.
    [436535, 436121]

    >>> # Search within specific departments
    >>> department_search = search(
    ...     query="cat",
    ...     departmentId=6  # Asian Art
    ... )
    >>> print(department_search[:5])
    [49698, 49470, 36221, 53222, 60873]

    """
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {}
    
    # if the parameters are passed with values, add them to the API call
    # By default, only query is passed with values
    if isHighlight is not None:
        params['isHighlight'] = str(isHighlight).lower()
    if title is not None:
        params['title'] = str(title).lower()
    if tags is not None:
        params['tags'] = str(tags).lower()
    if departmentId is not None:
        params['departmentId'] = departmentId
    if isOnView is not None:
        params['isOnView'] = str(isOnView).lower()
    if artistOrCulture is not None:
        params['artistOrCulture'] = str(artistOrCulture).lower()
    if medium is not None:
        params['medium'] = medium
    if hasImages is not None:
        params['hasImages'] = str(hasImages).lower()
    if geoLocation is not None:
        params['geoLocation'] = geoLocation
    if dateBegin is not None and dateEnd is not None:
        params['dateBegin'] = dateBegin
        params['dateEnd'] = dateEnd

    params['q'] = query

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        object_ids = data.get('objectIDs', [])
        if object_ids is None:
            return []
        return object_ids
    except requests.exceptions.RequestException as e:
        logger.error(f"Error performing search: {e}")
        raise