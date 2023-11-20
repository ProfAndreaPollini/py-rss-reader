import argparse
import re

import requests

from rich.console import Console
from rich.progress import Progress,track
from rich.prompt import Prompt
from rich.markdown import Markdown

console = Console()

COMMANDS = ["list_sources"]

parser = argparse.ArgumentParser()
commands = parser.add_subparsers(dest="command")
list_sources_command = commands.add_parser("list_sources", 
                    help="command to execute")
list_sources_command.add_argument("-u","--url",  type=str,help="url to add")
list_sources_command.add_argument("-c","--category",  type=str,help="feed source category", default="general")
show_source_items_command = commands.add_parser("show_items", help="show items from source")



args = parser.parse_args()

command = args.command

def show_source_items():
    r = requests.get("http://localhost:8080/sources")
    sources = r.json()['sources']
    # for source in sources:
    #     print(f"{source['name']}: ({source['url']}) [{source['category']}]")
    source_name = Prompt.ask("Which source?", choices=[source['name'] for source in sources])
    #get source id
    source_id = sources[[source['name'] for source in sources].index(source_name)]['id']

    r = requests.get(f"http://localhost:8080/items/{source_id}")
    data = r.json()
    
    items = data['items']
    for item in items:
        # print(f"{item['title']}: ({item['url']}) [{item['published']}]")
        markdown = f"""# {item['title']}

## {item['published']}

{item['content']}
"""
        md = Markdown(markdown)
        console.print(md)

def list_sources():
    r = requests.get("http://localhost:8080/sources")
    sources = r.json()['sources']
    for source in sources:
        print(f"{source['name']}: ({source['url']}) [{source['category']}]")

match command:
    case "list_sources": list_sources()
    case "show_items": show_source_items()