import sqlite3 as sql


class Database():
    def __init__(self):
        self.connection = sql.connect('database.db')
        self.cur = self.connection.cursor()

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def execute(self, new_data):
        """execute a row of data to current cursor"""
        self.cur.execute(new_data)

    def fetchone(self):
        row = self.cur.fetchone()
        return row

    def commit(self):
        """commit changes to database"""
        self.connection.commit()


def reset_database():
    conn = Database()
    conn.execute('DROP TABLE IF EXISTS speed_table')
    conn.execute('DROP TABLE IF EXISTS line_table')
    conn.execute('DROP TABLE IF EXISTS distance_table')
    conn.execute('DROP TABLE IF EXISTS commands_table')
    conn.execute('DROP TABLE IF EXISTS start_robot')
    conn.execute('DROP TABLE IF EXISTS checkpoint')

    conn.execute('CREATE TABLE IF NOT EXISTS speed_table (data TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS line_table (data TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS distance_table (data TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS commands_table (data TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS start_robot (data TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS checkpoint (data TEXT)')

    conn.execute('INSERT INTO speed_table(data) VALUES(0)')
    conn.execute('INSERT INTO line_table(data) VALUES(0)')
    conn.execute('INSERT INTO distance_table(data) VALUES(0)')
    conn.execute('INSERT INTO commands_table(data) VALUES(0)')
    conn.execute('INSERT INTO start_robot(data) VALUES(0)')
    conn.execute('INSERT INTO checkpoint(data) VALUES(0)')

    conn.commit()
    print('database reset')
    conn.close()


def update_data(speed,line,distance,start_robot,checkpoint):
    conn = Database()
    if speed is not None:
        query = 'UPDATE speed_table SET data=?' + speed + ' WHERE rowid=1'
        conn.execute(query)
    if line is not None:
        query = 'UPDATE line_table SET data=?' + line + ' WHERE rowid=1'
        conn.execute(query)
    if distance is not None:
        query = 'UPDATE distance_table SET data=?' + distance + ' WHERE rowid=1'
        conn.execute(query)
    if start_robot is not None:
        query = 'UPDATE start_robot SET data=?' + start_robot + ' WHERE rowid=1'
        conn.execute(query)
    if checkpoint is not None:
        query = 'UPDATE checkpoint SET data=?' + checkpoint + ' WHERE rowid=1'
        conn.execute(query)
    conn.commit()
    conn.close()


def get_speed():
    conn = Database()
    conn.execute("select * from speed_table")
    row = conn.fetchone()
    speed = row[0]
    conn.commit()
    conn.close()
    return speed


def get_line():
    conn = Database()
    conn.execute("select * from line_table")
    row = conn.fetchone()
    line = row[0]
    conn.commit()
    conn.close()
    return line


def get_distance():
    conn = Database()
    conn.execute("select * from distance_table")
    row = conn.fetchone()
    distance = row[0]
    conn.commit()
    conn.close()
    return distance


def get_start():
    conn = Database()
    conn.execute("select * from start_robot")
    row = conn.fetchone()
    start_robot = row[0]
    conn.commit()
    conn.close()
    return start_robot


def get_checkpoint():
    conn = Database()
    conn.execute("select * from checkpoint")
    row = conn.fetchone()
    checkpoint = row[0]
    conn.commit()
    conn.close()
    return checkpoint


def get_commands():
    conn = Database()
    conn.execute("select * from commands_table")
    row = conn.fetchone()
    command = "[" + row[0] + "]"
    conn.close()
    return command


def update_commands(commands):
    conn = Database()
    query = "UPDATE commands_table SET data=" + commands + " WHERE rowid=1"
    conn.execute(query)
    conn.commit()
    conn.close()

