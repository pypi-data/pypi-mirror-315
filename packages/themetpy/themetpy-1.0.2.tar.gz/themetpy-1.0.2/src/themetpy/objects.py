# themetpy/objects.py
# returns a record for an object, containing all open access data about that object, 
# including its image (if the image is available under Open Access)

import requests
import logging
from .utils import handle_missing_data

logger = logging.getLogger(__name__)

def get_all_object_ids(metadataDate=None, departmentIds=None):
    """
    Retrieve a list of all valid Object IDs from The Met's collection.

    Parameters:
    -----------
        metadataDate (str, optional): Return objects with updated data after this date (YYYY-MM-DD).
        departmentIds (list or int, optional): List of department IDs or a single department ID.

    Returns:
    --------
        list: A list of Object IDs.

    Examples:
    ---------
    >>> from themetpy.objects import get_all_object_ids
    >>> # Retrieve all object IDs
    >>> all_object_ids = get_all_object_ids()
    >>> print(all_object_ids[:5])  # Display first 5 Object IDs
    [1, 2, 3, 4, 5]

    >>> # Retrieve object IDs updated after January 1, 2023
    >>> recent_object_ids = get_all_object_ids(metadataDate="2023-01-01")
    >>> print(recent_object_ids[:5])
    [947, 949, 951, 952, 953]

    >>> # Retrieve object IDs from departments 1, 3, and 6
    >>> department_object_ids = get_all_object_ids(departmentIds=[1, 3, 6])
    >>> print(department_object_ids[:5])
    [1, 2, 3, 4, 5]
    
    """
    
    base_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
    params = {}
    # if the metadataDate and the departmentIds parameters are passed with values, add them to the API call
    # By default, they are none
    if metadataDate:
        params['metadataDate'] = metadataDate
    if departmentIds:
        if isinstance(departmentIds, list):
            params['departmentIds'] = '|'.join(map(str, departmentIds))
        else:
            params['departmentIds'] = str(departmentIds)
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        object_ids = data.get('objectIDs', [])
        return object_ids
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching object IDs: {e}")
        raise

def get_object(objectID, handle_missing='log', replace_value='Unknown', verbose=False, raw=False):
    """
    Retrieve detailed information for a specific object from The Met's API.

    Parameters:
    -----------
        objectID (int): The Object ID of the artwork.
        handle_missing (str): How to handle missing data ('log', 'filter', 'replace').
        replace_value (str): Value to replace missing fields with when handle_missing='replace'.
        verbose (bool): If True, prints warnings about missing data fields.
        raw (bool): If True, returns the raw JSON data without processing.

    Returns:
    --------
        dict or pd.DataFrame: The object's data as a dictionary or DataFrame, or raw JSON if raw=True.
    
    Raises:
    ------
        ValueError: If the Object ID does not exist (HTTP 404).
        requests.exceptions.HTTPError: For other HTTP-related errors.

    Example:
    --------
    >>> from themetpy.objects import get_object
    >>> # Retrieve object data with missing fields replaced by 'Unknown'
    >>> object_data = get_object(
    ...     objectID=45734,
    ...     handle_missing='replace',
    ...     replace_value='Unknown',
    ...     verbose=True
    ... )
    >>> print(object_data)
    {
        'objectID': 45734,
        'title': 'Quail and Millet',
        'artistDisplayName': 'Kiyohara Yukinobu',
        'primaryImage': 'https://images.metmuseum.org/CRDImages/as/original/DP251139.jpg',
        'objectDate': 'late 17th century',
        'medium': 'Hanging scroll; ink and color on silk',
        'dimensions': '46 5/8 x 18 3/4 in. (118.4 x 47.6 cm)',
        'department': 'Asian Art',
        'culture': 'Japan'
    }

    >>> # Attempt to retrieve a non-existent object
    >>> get_object(999999999)
    Traceback (most recent call last):
        ...
    ValueError: Object ID 999999999 does not exist.
    
    """
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}"
    
    try:
        response = requests.get(url)
        if response.status_code == 404:
            raise ValueError(f"Object ID {objectID} does not exist.")
        response.raise_for_status()
        data = response.json()
        
        if raw:
            return data
        
        # Define required fields
        required_fields = [
            'title', 'artistDisplayName', 'primaryImage', 'objectDate',
            'medium', 'dimensions', 'department', 'culture'
        ]
        
        # Handle missing data
        data = handle_missing_data(data, required_fields, handle_missing, replace_value, verbose)
        
        if data is None:
            # Record is filtered out due to missing data
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching object {objectID}: {e}")
        raise