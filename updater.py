from os import name
import sqlite3 as sq
from turtle import up
import feedparser as fp
import argparse
import json

from rich.console import Console
from rich.progress import Progress,track
from rich.prompt import Prompt


console = Console()

COMMANDS= ["update", "add", "remove"]

parser = argparse.ArgumentParser()
commands_parser = parser.add_subparsers(dest="command", 
                    help="command to execute")
add_command = commands_parser.add_parser("add", help="add new rss feed")
add_command.add_argument("-u","--url",  type=str,help="url to add")
add_command.add_argument("-c","--category",  type=str,help="feed source category", default="general")

update_command = commands_parser.add_parser("update", help="update rss feeds")
# update_command.add_argument("-s","--source",  type=str,help="source to update")

remove_command = commands_parser.add_parser("remove", help="remove rss feed")


args = parser.parse_args()

command = args.command

# connect to rss.db database
conn = sq.connect('rss.db')

def update_single_source(url):
    c = conn.cursor()
    # console.print(f"Updating {name} ({url})", style="bold green")

    # load and parse rss feed
    data = fp.parse(url)
    entries = data.entries

    for entry in entries:
        node = json.dumps(entry,indent=2)
        title = entry.title
        link = entry.link
        description = entry.description
        published = entry.published

        # check if item exists
        c.execute("SELECT COUNT(id) FROM items WHERE url = ?", (link,))
        count = c.fetchone()[0]

        if count > 0:
            # item exists, skip
            # console.log(f"Item {title} ({link}) already exists.")
            continue

        # add new item
        c.execute("INSERT INTO items (title, url, content, date,node,source_id) VALUES (?, ?, ?, ?,?,?)", (title, link, description, published,node,id))
    conn.commit()

def update_sources():
    console.print("Hello", "World!", style="bold red")
    c = conn.cursor()
    c.execute("SELECT id,name,url FROM sources")
    sources = c.fetchall()

    source_names = [source[1] for source in sources]
    source_names.append("all")

    name = Prompt.ask("Enter the source to update", choices=source_names, default="all")

    
    if name == "all":
        for source in track(sources):
               url = source[2]
               update_single_source(url)
    else:
        url = sources[source_names.index(name)][2]
        update_single_source(url)   
    conn.commit()

def remove_source():
    #get sources
    c = conn.cursor()
    c.execute("SELECT id,name,url FROM sources")
    sources = c.fetchall()

    source_names = [source[1] for source in sources]
    source_names.append("all")

    name = Prompt.ask("Enter the source to remove", choices=source_names, default="all")

    if name == "all":
        for source in track(sources):
            id = source[0]
            c.execute("DELETE FROM items WHERE source_id = ?", (id,))
            c.execute("DELETE FROM sources WHERE id = ?", (id,))
    else:
        id = sources[source_names.index(name)][0]
        c.execute("DELETE FROM items WHERE source_id = ?", (id,))
        c.execute("DELETE FROM sources WHERE id = ?", (id,))

    conn.commit()


match command:
    case "remove":
        remove_source()
    case "update":
        update_sources()
    case "add":
        url = args.url
        category = args.category
        # add new rss feed
        d = fp.parse(url)
        name = d.feed.title
        print(f"Adding {name} ({url}) [{len(d.entries)} entries]")
    
    

        # check if category name exists
        c = conn.cursor()
        c.execute("SELECT COUNT(id) FROM categories WHERE name = ?", (category,))
        count = c.fetchone()[0]

        if count == 0:
            # create category
            c.execute("INSERT INTO categories (name) VALUES (?)", (category,))
            # conn.commit()

            print(f"Created category {category}.")
        
        # get category id
        c.execute("SELECT id FROM categories WHERE name = ?", (category,))
        category_id = c.fetchone()[0]

        # check if source exists
        c.execute("SELECT COUNT(id) FROM sources WHERE url = ?", (url,))
        count = c.fetchone()[0]

        if count > 0:
            print(f"Source {name} ({url}) already exists.")
            # conn.rollback()
            conn.close()
            exit()

        # c = conn.cursor()
        c.execute("INSERT INTO sources (url, name,category_id) VALUES (?, ?,?)", (url, name,category_id))
        conn.commit()

        print(f"Added {name} ({url}) to {category}.")

        ## add new rss feed

        source_id = c.lastrowid

        entries = d.entries
        try:
            for entry in entries:
                title = entry.title
                link = entry.link
                description = entry.description
                published = entry.published
                node = json.dumps(entry,indent=2)

                # c = conn.cursor()
                c.execute("INSERT INTO items (title, url, content, date,node,source_id) VALUES (?, ?, ?, ?,?,?)", (title, link, description, published,node,source_id))
                # conn.commit()

                print(f"Added {title} ({link}) to entries.")
            
            # c = conn.cursor()
            # c.execute("INSERT INTO rss (url, name) VALUES (?, ?)", (url, name))
            # conn.commit()
            # c.close()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
            exit()
        conn.commit()

