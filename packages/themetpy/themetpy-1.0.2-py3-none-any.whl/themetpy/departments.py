# themetpy/departments.py
# returns a listing of all departments

import requests
import logging

logger = logging.getLogger(__name__)

def get_departments():
    """
    Retrieve a list of all departments in The Met.

    Returns:
    --------
        list: A list of dictionaries containing departmentId and displayName.
    
    Examples:
    ---------
    >>> from themetpy.departments import get_departments
    >>> departments = get_departments()
    >>> for dept in departments:
    ...     print(f"ID: {dept['departmentId']}, Name: {dept['displayName']}")
    ...
    ID: 1, Name: American Decorative Arts
    ID: 3, Name: Ancient Near Eastern Art
    ID: 4, Name: Arms and Armor
    ID: 5, Name: Arts of Africa, Oceania, and the Americas
    ID: 6, Name: Asian Art
    
    """
    url = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        departments = data.get('departments', [])
        return departments
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching departments: {e}")
        raise