-- categories(pk: id, name)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
-- sources(pk:id,name,url,fk:category_id)
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
-- items(pk:id,title,content,url,fk:source_id)
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT NOT NULL,
    node TEXT NOT NULL,
    date DATE NULL,
    readed BOOLEAN NOT NULL DEFAULT 0,
    source_id INTEGER NOT NULL,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);
-- mapping(pk:id, config,fk:source_id)
CREATE TABLE IF NOT EXISTS mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);
