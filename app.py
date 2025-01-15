import streamlit as st
import sqlite3

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('esports.db')
    conn.row_factory = sqlite3.Row  # Enables fetching rows as dictionaries
    return conn

# Function to get all teams
def get_teams():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM teams')
    teams = cursor.fetchall()
    conn.close()
    return teams

# Function to get players by team
def get_players_by_team(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT p.first_name, p.last_name, p.username, t.name as team_name
    FROM players p
    JOIN teams t ON p.team_id = t.team_id
    WHERE t.team_id = ?;
    ''', (team_id,))
    players = cursor.fetchall()
    conn.close()
    return players

# Function to get brawlers
def get_brawlers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT b.name, b.type, s.played_games, s.pickrate, s.wins, s.win_rate, s.bans, s.ban_rate
    FROM brawlers b
    JOIN brawler_stats s ON b.brawler_id = s.brawler_id;
    ''')
    brawlers = cursor.fetchall()
    conn.close()
    return brawlers

# Streamlit app layout
st.title("Esports Team Database")

# Show teams
st.header("Teams")
teams = get_teams()
team_names = [team['name'] for team in teams]
selected_team = st.selectbox("Select a Team", team_names)

# Show players from selected team
if selected_team:
    st.header(f"Players in {selected_team}")
    team_id = [team['team_id'] for team in teams if team['name'] == selected_team][0]
    players = get_players_by_team(team_id)
    for player in players:
        st.write(f"**{player['first_name']} {player['last_name']}** (Username: {player['username']})")

# Show brawlers
st.header("Brawlers and Stats")
brawlers = get_brawlers()
for brawler in brawlers:
    st.write(f"**{brawler['name']}** (Type: {brawler['type']})")
    st.write(f"Played Games: {brawler['played_games']}, Pickrate: {brawler['pickrate']}%, Wins: {brawler['wins']}, Win Rate: {brawler['win_rate']}%")
    st.write(f"Bans: {brawler['bans']}, Ban Rate: {brawler['ban_rate']}%")
    st.write("---")
