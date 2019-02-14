import sqlite3
import json

db_name = 'employees.db'
table_name = 'employees'


def create_connection():
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print('Could not create connection... {}'.format(e))
    return None


def create_table():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name +
            ' (id INTEGER PRIMARY KEY, name text, sales integer, amount integer)')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print('Could not create table... {}'.format(e))
    finally:
        conn.close()


def is_employee_in_db(name):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name + ' WHERE name=?', (name,))
        row = cur.fetchall()
        if name in [i[1] for i in row]:
            conn.close()
            return True
        else:
            conn.close()
            return False
    except sqlite3.Error as e:
        print('Error when fetching employee from table... {}'.format(e))
    finally:
        conn.close()


def insert(name, sales, amount):
    conn = create_connection()
    try:
        cur = conn.cursor()
        # NULL will be replaced by id
        cur.execute('INSERT INTO ' + table_name + ' VALUES (NULL,?,?,?)', (name, sales, amount))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print('Error when inserting employee into table... {}'.format(e))
    finally:
        conn.close()


def update(name, sales, amount):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('UPDATE ' + table_name + ' SET amount=?, sales=? WHERE name=?', (amount, sales, name))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print('Error when updating employee record... {}'.format(e))
    finally:
        conn.close()


def view_db_records():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name)
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        # print('Error when viewing employee records... {}'.format(e))
        pass
        # log exception
    finally:
        conn.close()


def is_table_empty():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name)
        rows = cur.fetchall()
        if not rows:
            print('There are no sales records. Ask your salespeople to sell something...\n')
            return True
    except sqlite3.Error:
        pass
        # log exception
    finally:
        conn.close()
    return False


def export_as_json():
    conn = create_connection()
    cur = conn.cursor()
    result = cur.execute('SELECT * FROM ' + table_name)
    items = [dict(zip([key[0] for key in cur.description], row)) for row in result]
    print(json.dumps({table_name: items}))


def export_as_xml(file_name):
    with open(file_name, "w") as f:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name)
        rows = cur.fetchall()
        f.write('<?xml version="1.0" ?>\n')
        f.write('<employees>\n')
        for row in rows:
            f.write('  <row>\n')
            f.write('    <id>%s</id>\n' % row[0])
            f.write('    <name>%s</name>\n' % row[1])
            f.write('    <sales>%s</sales>\n' % row[2])
            f.write('    <amount>%s</amount>\n' % row[3])
            f.write('  </row>\n')
        f.write('</employees>\n')
        conn.close()





