import sqlite3

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('esports.db')
    conn.row_factory = sqlite3.Row  # Enables fetching rows as dictionaries
    return conn

# Initialize the database and create tables
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Teams Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    ''')

    # Create Players Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT,
        username TEXT NOT NULL,
        team_id INTEGER,
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
    );
    ''')

    # Create Brawlers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS brawlers (
        brawler_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL
    );
    ''')

    # Create Brawler Stats Table (for storing brawler performance data)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS brawler_stats (
        stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        brawler_id INTEGER,
        played_games INTEGER,
        pickrate REAL,
        wins INTEGER,
        win_rate REAL,
        bans INTEGER,
        ban_rate REAL,
        FOREIGN KEY (brawler_id) REFERENCES brawlers(brawler_id)
    );
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Add a team to the database
def add_team(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO teams (name) 
    VALUES (?);
    ''', (name,))
    conn.commit()
    conn.close()

# Add a player to the database
def add_player(first_name, last_name, username, team_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO players (first_name, last_name, username, team_id) 
    VALUES (?, ?, ?, ?);
    ''', (first_name, last_name, username, team_id))
    conn.commit()
    conn.close()

# Add brawler stats
def add_brawler_stats(brawler_id, played_games, pickrate, wins, win_rate, bans, ban_rate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO brawler_stats (brawler_id, played_games, pickrate, wins, win_rate, bans, ban_rate) 
    VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', (brawler_id, played_games, pickrate, wins, win_rate, bans, ban_rate))
    conn.commit()
    conn.close()

# Add brawler to the database
def add_brawler(name, brawler_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO brawlers (name, type) 
    VALUES (?, ?);
    ''', (name, brawler_type))
    conn.commit()
    conn.close()

# Function to view all players with their team names
def get_players_with_teams():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT p.first_name, p.last_name, p.username, t.name as team_name
    FROM players p
    JOIN teams t ON p.team_id = t.team_id;
    ''')
    players = cursor.fetchall()
    conn.close()
    for player in players:
        print(f"Player: {player['first_name']} {player['last_name']} (Username: {player['username']}) - Team: {player['team_name']}")

# Function to view all brawlers with their stats
def get_brawlers_with_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT b.name, b.type, s.played_games, s.pickrate, s.wins, s.win_rate, s.bans, s.ban_rate
    FROM brawlers b
    JOIN brawler_stats s ON b.brawler_id = s.brawler_id;
    ''')
    brawlers = cursor.fetchall()
    conn.close()
    for brawler in brawlers:
        print(f"Brawler: {brawler['name']}, Type: {brawler['type']}, Played Games: {brawler['played_games']}, Pickrate: {brawler['pickrate']}%, Wins: {brawler['wins']}, Win Rate: {brawler['win_rate']}%, Bans: {brawler['bans']}, Ban Rate: {brawler['ban_rate']}%")

# Initialize the database if this script is run directly
if __name__ == "__main__":
    initialize_db()

    # Add teams
    add_team('Crazy Raccoon')
    add_team('HMBLE')
    add_team('Totem')

    # Add players with associated teams (Team ID)
    add_player('SITETAMPO', '', 'SITETAMPO', 1)
    add_player('MOYA', '', 'MOYA', 1)
    add_player('TENSAI', '', 'TENSAI', 1)

    add_player('Symantec', '', 'Symantec', 2)
    add_player('BosS', '', 'BosS', 2)
    add_player('Lukii', '', 'Lukii', 2)

    add_player('Maru', '', 'Maru', 3)
    add_player('Maury', '', 'Maury', 3)
    add_player('iKaoss', '', 'iKaoss', 3)

    # Add brawlers
    add_brawler('Meg', 'Tank')
    add_brawler('Frank', 'Tank')
    add_brawler('Chester', 'Assassin')
    add_brawler('Gale', 'Support')
    add_brawler('Barley', 'Support')
    add_brawler('Gene', 'Support')
    add_brawler('Buster', 'Tank')
    add_brawler('Max', 'Assassin')
    add_brawler('Larry & Lawrie', 'Support')
    add_brawler('R-T', 'Tank')
    add_brawler('Stu', 'Assassin')
    add_brawler('Angelo', 'Tank')
    add_brawler('Belle', 'Assassin')
    add_brawler('Berry', 'Tank')

    # Add stats for brawlers
    add_brawler_stats(1, 29, 67.4, 17, 58.6, 14, 16.3)  # Meg
    add_brawler_stats(2, 14, 32.6, 8, 57.1, 16, 18.6)  # Frank
    add_brawler_stats(3, 13, 30.2, 8, 61.5, 6, 7.0)   # Chester
    add_brawler_stats(4, 12, 27.9, 6, 50.0, 16, 18.6)   # Gale
    add_brawler_stats(5, 10, 23.3, 5, 50.0, 5, 5.8)    # Barley
    add_brawler_stats(6, 9, 20.9, 4, 44.4, 13, 15.1)   # Gene
    add_brawler_stats(7, 8, 18.6, 6, 75.0, 8, 9.3)    # Buster
    add_brawler_stats(8, 8, 18.6, 5, 62.5, 9, 10.5)   # Max
    add_brawler_stats(9, 7, 16.3, 2, 28.6, 18, 20.9)   # Larry & Lawrie
    add_brawler_stats(10, 7, 16.3, 3, 42.9, 0, 0.0)   # R-T
    add_brawler_stats(11, 7, 16.3, 4, 57.1, 0, 0.0)   # Stu
    add_brawler_stats(12, 6, 14.0, 2, 33.3, 11, 12.8)  # Angelo
    add_brawler_stats(13, 6, 14.0, 2, 33.3, 2, 2.3)   # Belle
    add_brawler_stats(14, 6, 14.0, 1, 16.7, 4, 4.7)   # Berry

    # View all players and their team names
    print("Players with Teams:")
    get_players_with_teams()

    # View all brawlers and their stats
    print("Brawlers with Stats:")
    get_brawlers_with_stats()
