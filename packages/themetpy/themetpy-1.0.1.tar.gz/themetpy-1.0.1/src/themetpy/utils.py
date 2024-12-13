# themetpy/utils.py

import logging

logger = logging.getLogger(__name__)

def handle_missing_data(data, required_fields, handle_missing='log', replace_value='Unknown', verbose=False):
    """
    Handle missing data based on user preference.

    Parameters:
    -----------
        data (dict): The data dictionary to check.
        required_fields (list): List of fields to verify.
        handle_missing (str): Strategy for handling missing data ('log', 'filter', 'replace').
        replace_value (str): Value to replace missing fields with when handle_missing='replace'.
        verbose (bool): If True, prints warnings about missing data fields.

    Returns:
    --------
        dict or None: Modified data dictionary or None if filtered out.
    
    Examples:
    ---------
    >>> from themetpy.utils import handle_missing_data
    >>> # Example data with missing 'artistDisplayName'
    >>> # Assume the data has no field called 'artistDisplayName'
    >>> data = {
    ...     'title': 'Wheat Field with Cypresses',
    ...     'primaryImage': 'https://images.metmuseum.org/CRDImages/ep/original/DT1567.jpg',
    ...     'objectDate': '1889',
    ...     'medium': 'Oil on canvas',
    ...     'dimensions': '28 7/8 × 36 3/4 in. (73.2 × 93.4 cm)',
    ...     'department': 'European Paintings'
    ... }
    >>> required_fields = ['title', 'artistDisplayName']
    
    >>> # Handling missing data by logging
    >>> handled_data = handle_missing_data(data, required_fields, handle_missing='log', verbose=True)
    Warning: Missing fields: artistDisplayName
    >>> print(handled_data)
    {
        'title': 'Wheat Field with Cypresses',
        'primaryImage': 'https://images.metmuseum.org/CRDImages/ep/original/DT1567.jpg',
        'objectDate': '1889',
        'medium': 'Oil on canvas',
        'dimensions': '28 7/8 × 36 3/4 in. (73.2 × 93.4 cm)',
        'department': 'European Paintings',
        'artistDisplayName': None
    }

    >>> # Handling missing data by replacing with 'Unknown'
    >>> handled_data_replace = handle_missing_data(data, required_fields, handle_missing='replace', replace_value='Unknown', verbose=True)
    Warning: Missing fields: artistDisplayName. Replaced with 'Unknown'.
    >>> print(handled_data_replace)
    {
        'title': 'Wheat Field with Cypresses',
        'primaryImage': 'https://images.metmuseum.org/CRDImages/ep/original/DT1567.jpg',
        'objectDate': '1889',
        'medium': 'Oil on canvas',
        'dimensions': '28 7/8 × 36 3/4 in. (73.2 × 93.4 cm)',
        'department': 'European Paintings',
        'artistDisplayName': 'Unknown'
    }

    >>> # Handling missing data by filtering out the record
    >>> handled_data_filter = handle_missing_data(data, required_fields, handle_missing='filter')
    >>> print(handled_data_filter)
    None

    """
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        message = f"Missing fields: {', '.join(missing_fields)}"
        if handle_missing == 'log':
            logger.warning(message)
            for field in missing_fields:
                data[field] = None
        elif handle_missing == 'filter':
            return None
        elif handle_missing == 'replace':
            for field in missing_fields:
                data[field] = replace_value
            if verbose:
                print(f"Warning: {message}. Replaced with '{replace_value}'.")
        else:
            logger.warning(message)
    
    return data