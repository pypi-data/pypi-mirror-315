import os
import json
from json import JSONDecodeError
from functools import wraps
from typing import Callable, Union, Any, Optional
from time import perf_counter
from requests import ConnectionError
from ..constants import console, SUPERHEROES_JSON_FILE_PATH, SUPERHEROES_IDS_NAMES_TABLE
import plotext as plt

# For testing purposes
def measure_function_execution_time(func: Callable[..., Any]) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        console.print(f"\"{func.__name__}\" Function done within {end - start: .2f} s.")
        return result
    return wrapper

def requests_error_handler(func: Callable[..., Any]) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            console.print("[red]No internet connection! Please check your network and try again.[/red]")
            return None
        except Exception as error:
            console.print(f"[red]An error has occured:[/red]\n{error}")
            return None
    return wrapper

def cli_errors_handler(func: Callable[..., Any]) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except (EOFError, KeyboardInterrupt):
            print("Exiting...")
            exit("Have a good day!")
    return wrapper

def meters_to_freedom_units(meters : Union[int, float]) -> str:
    total_feet = meters * 3.28084  
    feet = int(total_feet)         
    inches = (total_feet - feet) * 12  
    return f"{feet}'{round(inches)}\""

def verify_superhero (superhero_id_or_name : str):
    try:
        with open(SUPERHEROES_JSON_FILE_PATH, "r") as superheroes_json_file:
            ref : Dict = json.load(superheroes_json_file)
        try:
            id = int(superhero_id_or_name)
            if  1 <= id <= 731:
                return True,id
            else:
                return False,None 
        except ValueError:
            id = [int(ids) for ids in ref if ref[ids]==superhero_id_or_name.title()]
            if not id:
                return False,None
            elif len(id) == 1:
                return True,id[0]      
            return True,id
    except JSONDecodeError as err:
        console.print(f"[red]Broken or invalid JSON file:\"{SUPERHEROES_JSON_FILE_PATH}\"\n{err}")
        return None, False

def clear_screen() -> None:
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def create_powerstats_barplot(combat : int, intelligence: int, power: int, speed: int, strength: int, sup_name : str) -> None:
    powerstats = ["Combat", "Intelligence", "Power", "Speed", "Strength"]
    powerstats_percentages = [combat, intelligence, power, speed, strength]
    plt.simple_bar(powerstats, powerstats_percentages, width = 50,color="green", title = plt.colorize(f'{sup_name} Powerstats Chart', "magenta"))
    plt.show()

def display_superheroes_table() -> None:
    console.print(SUPERHEROES_IDS_NAMES_TABLE)


