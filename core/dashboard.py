<<<<<<< HEAD
from dash import Dash, dcc, html
=======
import dash
from dash import dcc, html
>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import requests
import pandas as pd

# Initialiser l'application Dash
<<<<<<< HEAD
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
=======
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a

# Fonction pour récupérer les données de Django
def fetch_data():
    response = requests.get("http://127.0.0.1:8000/api/auth/dashboard/")
    if response.status_code == 200:
        return response.json()
    return {}

<<<<<<< HEAD
# Layout du tableau de bord
app.layout = dbc.Container([
    html.H1("Tableau de Bord ITSM", className="text-center mt-4"),
=======

# Layout du tableau de bord
app.layout = dbc.Container([
    html.H1("Tableau de Bord IT", className="text-center mt-4"),
>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Utilisateurs en ligne"),
            dbc.CardBody(html.H3(id="users-online", className="text-center"))
        ], color="success", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Utilisateurs"),
            dbc.CardBody(html.H3(id="total-users", className="text-center"))
        ], color="primary", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Tickets"),
            dbc.CardBody(html.H3(id="total-tickets", className="text-center"))
        ], color="danger", inverse=True), width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="equipment-chart"), width=6),
        dbc.Col(dcc.Graph(id="ticket-chart"), width=6),
    ]),

<<<<<<< HEAD
    dbc.Row([
        dbc.Col(dcc.Graph(id="priority-chart"), width=12),  # Nouveau graphique pour les priorités
    ]),

    dcc.Interval(id="interval-update", interval=5000, n_intervals=0)
])

=======
    dcc.Interval(id="interval-update", interval=5000, n_intervals=0)
])


>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a
# Callback pour mettre à jour les données
@app.callback(
    [Output("users-online", "children"),
     Output("total-users", "children"),
     Output("total-tickets", "children"),
     Output("equipment-chart", "figure"),
<<<<<<< HEAD
     Output("ticket-chart", "figure"),
     Output("priority-chart", "figure")],  # Ajout du nouvel output
=======
     Output("ticket-chart", "figure")],
>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a
    Input("interval-update", "n_intervals")
)
def update_dashboard(n):
    data = fetch_data()

    # Mettre à jour les valeurs des cartes
    users_online = data.get("users_online", 0)
    total_users = data.get("total_users", 0)
    total_tickets = data.get("total_tickets", 0)

    # Graphique des équipements
    equipment_statuses = data.get("equipment_statuses", {})
    df_equipments = pd.DataFrame(list(equipment_statuses.items()), columns=["Statut", "Nombre"])
    fig_equipments = px.pie(df_equipments, names="Statut", values="Nombre", title="Répartition des Équipements")

<<<<<<< HEAD
    # Graphique des tickets par statut
=======
    # Graphique des tickets
>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a
    tickets_by_status = data.get("tickets_by_status", {})
    df_tickets = pd.DataFrame(list(tickets_by_status.items()), columns=["Statut", "Nombre"])
    fig_tickets = px.bar(df_tickets, x="Statut", y="Nombre", title="Statut des Tickets", color="Statut")

<<<<<<< HEAD
    # Graphique des tickets par priorité
    tickets_by_priority = data.get("tickets_by_priority", {})
    df_priority = pd.DataFrame(list(tickets_by_priority.items()), columns=["Priorité", "Nombre"])
    fig_priority = px.bar(df_priority, x="Priorité", y="Nombre", title="Priorité des Tickets", color="Priorité")

    return users_online, total_users, total_tickets, fig_equipments, fig_tickets, fig_priority

# Exécuter l'application Dash
if __name__ == "__main__":
    app.run_server(debug=True)
=======
    return users_online, total_users, total_tickets, fig_equipments, fig_tickets


# Exécuter l'application Dash
if __name__ == "__main__":
    app.run_server(debug=True)
>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a
