"""
Simple Data Access Layer (DAL) for projects only.
This file manages a single SQLite database `projects.db` and a single table `projects`
with columns: Title, Description, ImageFileName.

Functions:
- get_connection(db_path=None)
- init_projects_db(db_path=None)
- insert_project(data, db_path=None)
- get_projects(limit=100, db_path=None)
- get_project_by_id(project_id, db_path=None)

Notes:
- `data` passed to insert_project may use keys 'title'/'Title', 'description'/'Description',
  'image_filename'/'ImageFileName'. The function will accept either and map appropriately.
- Images should be placed manually in `app/static/images/` and only the filename should be stored in the DB.
"""

import sqlite3
from sqlite3 import Connection
from typing import Optional, List, Dict, Any
import datetime
import os

PROJECTS_DB = os.path.join(os.path.dirname(__file__), "projects.db")


def get_connection(db_path: Optional[str] = None) -> Connection:
    """Return a sqlite3 connection for the projects database."""
    path = db_path or PROJECTS_DB
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn


def init_projects_db(db_path: Optional[str] = None) -> None:
    """Create the projects database and the `projects` table if they do not exist.

    The table schema uses the exact column names: Title, Description, ImageFileName.
    """
    path = db_path or PROJECTS_DB
    conn = get_connection(path)
    with conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Description TEXT,
                ImageFileName TEXT,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
    conn.close()


def insert_project(data: Dict[str, Any], db_path: Optional[str] = None) -> int:
    """Insert a project record and return the new row id.

    Accepts keys: 'title' or 'Title', 'description' or 'Description',
    'image_filename' or 'ImageFileName'.
    """
    path = db_path or PROJECTS_DB
    # map possible keys to the DB column names
    title = data.get('Title') or data.get('title') or ''
    description = data.get('Description') or data.get('description') or ''
    image_filename = data.get('ImageFileName') or data.get('image_filename') or data.get('image') or ''

    conn = get_connection(path)
    with conn:
        cur = conn.execute(
            """
            INSERT INTO projects (Title, Description, ImageFileName, CreatedAt)
            VALUES (:Title, :Description, :ImageFileName, :CreatedAt)
            """,
            {
                'Title': title,
                'Description': description,
                'ImageFileName': image_filename,
                'CreatedAt': data.get('CreatedAt', datetime.datetime.utcnow()),
            },
        )
        rowid = cur.lastrowid
    conn.close()
    return rowid


def get_projects(limit: int = 100, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    path = db_path or PROJECTS_DB
    conn = get_connection(path)
    cur = conn.execute("SELECT id, Title, Description, ImageFileName, CreatedAt FROM projects ORDER BY CreatedAt DESC LIMIT :limit", {"limit": limit})
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_project_by_id(project_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    path = db_path or PROJECTS_DB
    conn = get_connection(path)
    cur = conn.execute("SELECT id, Title, Description, ImageFileName, CreatedAt FROM projects WHERE id = :id", {"id": project_id})
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None
