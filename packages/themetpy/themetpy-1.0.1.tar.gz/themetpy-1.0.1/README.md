# themetpy

The Python Package for The MET Museum. 
**TheMetPy** is designed to provide a user-friendly interface to The Metropolitan Museum of Art’s Open Access API. By abstracting the complexities of API interactions, TheMetPy enables developers, researchers, and enthusiasts to effortlessly retrieve and analyze data from The Met's vast collection. Whether you're building data visualizations, conducting research, or developing applications, TheMetPy streamlines the process of accessing museum data.

## Installation

You can install **TheMetPy** via [PyPI](https://pypi.org/project/themetpy/) using `pip`:

```bash
$ pip install themetpy
```

## Usage

**TheMetPy** offers a simple and intuitive interface to interact with The Met’s Open Access API. Below are examples demonstrating how to utilize its core functionalities.

**Quick Start** 

After installation, you can start using **TheMetPy** to interact with The Met’s Open Access API.

```
from themetpy import get_all_object_ids, get_object, get_departments, search

# 1. List all Object IDs in Department 6 (Asian Art)
object_ids = get_all_object_ids(departmentIds=6)
print(f"Total Object IDs in Department 6: {len(object_ids)}")

# 2. Retrieve details of a specific object (objectID: 45734)
object_data = get_object(45734, handle_missing='replace', replace_value='Unknown', verbose=True)
print(object_data)

# 3. List all departments
departments = get_departments()
for dept in departments:
    print(f"ID: {dept['departmentId']}, Name: {dept['displayName']}")

# 4. Perform an advanced search
search_results = search(
    query="sunflowers",
    isHighlight=True,
    medium="Paintings",
    hasImages=True,
    dateBegin=1800,
    dateEnd=1900
)
print(f"Found {len(search_results)} objects matching the search criteria.")
```

**Detailed Usage**

- **Listing All Valid Object IDs**

Fetch a list of all valid Object IDs from The Met’s collection. You can optionally filter by metadataDate and departmentIds.

* Parameters:
	* metadataDate (str, optional): Return objects with updated data after this date (format: YYYY-MM-DD).
	* departmentIds (list or int, optional): Filter by department ID(s).

* Returns:
	* list: A list of Object IDs.

```
from themetpy import get_all_object_ids

# Retrieve all object IDs
all_object_ids = get_all_object_ids()
print(all_object_ids)

# Retrieve object IDs updated after a specific date
recent_object_ids = get_all_object_ids(metadataDate="2021-01-01")
print(recent_object_ids)

# Retrieve object IDs from specific departments (using department's ID)
department_object_ids = get_all_object_ids(departmentIds=[1, 3, 6])
print(department_object_ids)
```

- **Retrieving Object Records**

Fetch detailed information about a specific artwork using its Object ID. You can specify how to handle missing data.

* Parameters:
	* objectID (int): The Object ID of the artwork.
	* handle_missing (str): Strategy for handling missing data. Options:
	* 'log': Log a warning for missing fields.
	* 'filter': Exclude records with missing data.
	* 'replace': Replace missing fields with a specified value.
	* replace_value (str): Value to replace missing fields with (used when handle_missing='replace').
	* verbose (bool): If True, prints warnings about missing data fields.
	* raw (bool): If True, returns the raw JSON data without processing.

* Returns:
	* dict or None: Return the object’s data as a dictionary, or None if filtered out.

```
from themetpy import get_object

# Retrieve object data with missing fields replaced by 'Unknown'
object_data = get_object(
    objectID=45734,
    handle_missing='replace',
    replace_value='Unknown',
    verbose=True
)
print(object_data)
```

- **Listing All Departments**

Fetch a list of all departments within The Met, including their IDs and display names.

* Parameters: None

* Returns:
	* list: A list of dictionaries containing departmentId and displayName.

```
from themetpy import get_departments

# List all departments
departments = get_departments()
for dept in departments:
    print(f"ID: {dept['departmentId']}, Name: {dept['displayName']}")
```

- **Advanced Search**

Perform complex searches across The Met’s collection using various parameters to filter results.

* Parameters:
	* query (str): Search term.
	* isHighlight (bool, optional): Filter by highlighted artworks.
	* title (bool, optional): Search within titles.
	* tags (bool, optional): Search within subject keyword tags.
	* departmentId (int, optional): Filter by department ID.
	* isOnView (bool, optional): Filter by objects currently on view.
	* artistOrCulture (bool, optional): Search within artist name or culture fields.
	* medium (str, optional): Filter by medium or object type (multiple values separated by |).
	* hasImages (bool, optional): Filter by objects that have images.
	* geoLocation (str, optional): Filter by geographic location (multiple values separated by |).
	* dateBegin (int, optional): Start year for date range.
	* dateEnd (int, optional): End year for date range.

* Returns:
	* list: A list of Object IDs matching the search criteria.

```
from themetpy import search

# Perform an advanced search
# Example
search_results = search(
    query="impressionism",
    isHighlight=True,
    medium="Paintings",
    hasImages=True,
    dateBegin=1850,
    dateEnd=1900
)
print(f"Found {len(search_results)} objects matching the search criteria.")
```

## Dependencies

TheMetPy currently relies on the following Python packages:
- requests: For making HTTP requests to The Met’s API.

*These dependencies are automatically installed when you install TheMetPy via pip.*

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms. Contributions are welcome in various forms, including bug reports, feature requests, and pull requests.

## License

`themetpy` was created by Yuxi Sun. It is licensed under the terms of the MIT license.

## Credits

`themetpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
