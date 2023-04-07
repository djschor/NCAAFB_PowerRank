import os
from dotenv import load_dotenv

def get_base_path():
    """
    Gets the base path of the project located at the base NCAAFB_POWER_RANK directory, two parents above the current path. 

    Returns:
        str: The base path of the project.
    """
    current_path = os.path.abspath(__file__)
    parent_path = os.path.dirname(current_path)
    grandparent_path = os.path.dirname(parent_path)
    base_path = os.path.dirname(grandparent_path)
    return base_path

def read_api_key():
    """
    Reads the CFB_API_KEY from the .env file.

    Returns:
        str: The CFB_API_KEY.
    """
    # Load the environment variables from the .env file
    base_path = get_base_path()
    dotenv_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path)

    # Read the CFB_API_KEY from the environment variables
    api_key = os.getenv('CFB_API_KEY')

    return api_key