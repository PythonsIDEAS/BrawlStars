import streamlit as st
import sqlite3
import plotly.graph_objects as go

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

# Function to create a pie chart for win rate
def plot_win_rate_chart(win_rate):
    # Pie chart for win rate
    fig = go.Figure(data=[go.Pie(labels=['Wins', 'Losses'], values=[win_rate, 100 - win_rate])])
    fig.update_layout(title="Win Rate Distribution")
    return fig

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

# Show brawlers and stats
st.header("Brawlers and Stats")
brawlers = get_brawlers()
for brawler in brawlers:
    st.write(f"**{brawler['name']}** (Type: {brawler['type']})")
    st.write(f"Played Games: {brawler['played_games']}, Pickrate: {brawler['pickrate']}%, Wins: {brawler['wins']}, Win Rate: {brawler['win_rate']}%")
    st.write(f"Bans: {brawler['bans']}, Ban Rate: {brawler['ban_rate']}%")
    
    # Plot the win rate pie chart
    win_rate = brawler['win_rate']
    win_rate_chart = plot_win_rate_chart(win_rate)
    st.plotly_chart(win_rate_chart)
    
    st.write("---")
