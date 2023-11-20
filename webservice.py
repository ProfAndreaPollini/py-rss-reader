from bottle import route, run, template, request, static_file,get
import json
import sqlite3 as sq

@route('/')
def index():
    return static_file('index.html', root='public')

@get("/items/<source_id:int>")
def source_items(source_id:int):
    # get source items
    conn = sq.connect('rss.db')
    c = conn.cursor()
    c.execute("""SELECT sources.name,items.title,items.url,items.content,items.date FROM sources,items WHERE sources.id = items.source_id AND sources.id = ?""", (source_id,))
    source_name = c.fetchone()[0][0]
    items = c.fetchall()

    
    ret = {
        "source": source_name,
        "items": []
    }

    for item in items:
        title = item[1]
        url = item[2]
        content = item[3]
        published = item[4]
        

        item_data = {
            "title": title,
            "url": url,
            "content": content,
            "published": published,
        }

        ret['items'].append(item_data)

    c.close()
    conn.close()
    return json.dumps(ret, indent=2)
    

@get("/sources")
def get_sources():
    conn = sq.connect('rss.db')
    c = conn.cursor()
    c.execute("SELECT id,name,url,category_id FROM sources")
    sources = c.fetchall()

    ret = {
        "sources": []
    }
    # get category name
    for i, source in enumerate(sources):
        print(f"{source=}")
        name = source[1]
        url = source[2]
        id = source[0]
        category_id = source[3]
        c.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
        category = c.fetchone()[0]

        source_data = {
            "id": id,
            "name": name,
            "url": url,
            "category": category
        }

        
        ret['sources'].append(source_data)
    c.close()
    conn.close()
    
    return json.dumps(ret, indent=2)


run(host='localhost', port=8080, debug=True,reloader=True)