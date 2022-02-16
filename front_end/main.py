#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import math
import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox

host = 'localhost'
db_name = 'tm'


class App(tk.Tk):
    """
    The Controller for the application.

    Controls current page and holds database connection.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        style = ttk.Style()
        style.theme_use('default')

        self.title('Tournament Manager')
        self.geometry('900x600')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # The parent frame for all pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container

        # The starting frame
        frame = LoginPage(parent=container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frame = frame
        self.last_frame = None

        self.cnx = None

        self.to_id = None
        self.d_id = None
        self.te_id = None
        self.p_id = None
        self.s_id = None
        self.m_id = None

    def next_frame(self, frame_type):
        self.last_frame = self.frame.__class__
        frame = frame_type(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frame.destroy()
        self.frame = frame

    def refresh(self):
        self.next_frame(self.frame.__class__)


class LoginPage(ttk.Frame):
    """
    Represents the login page of the application.

    Takes user login input and validates login to SQL Database.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Form Grouping
        form = ttk.Frame(self)

        # username label and text entry box
        username_label = ttk.Label(form, text="Username:")
        username_label.pack()
        self.username = tk.StringVar()
        username_entry = ttk.Entry(form, textvariable=self.username)
        username_entry.pack(pady=5)

        # password label and password entry box
        password_label = ttk.Label(form, text="Password:")
        password_label.pack()
        self.password = tk.StringVar()
        password_entry = ttk.Entry(form, textvariable=self.password, show='*')
        password_entry.pack(pady=5)

        login_button = ttk.Button(form, text="Login", command=self.attempt_login)
        login_button.pack(padx=5, pady=5)

        form.place(relx=0.5, rely=0.4, anchor="center")

    def attempt_login(self):
        try:
            cnx = pymysql.connect(host=host, user=self.username.get(),
                                  password=self.password.get(),
                                  db=db_name, charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
            self.controller.cnx = cnx
            self.controller.next_frame(Homepage)
        except pymysql.err.OperationalError:
            messagebox.showerror("Error", "Incorrect login info, please try again.")


class Homepage(ttk.Frame):
    """
    Represents the application homepage.

    Presents tournament, player, and school access.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Homepage", font=controller.title_font)
        label.pack(side="top", fill="x", padx=10, pady=10)

        # Button Grouping
        group = ttk.Frame(self)

        button1 = ttk.Button(group, text="Go to Tournaments",
                             command=lambda: controller.next_frame(Tournaments))
        button1.pack(pady=5)
        button2 = ttk.Button(group, text="Go to Players",
                             command=lambda: controller.next_frame(Players))
        button2.pack(pady=5)
        button3 = ttk.Button(group, text="Go to Schools",
                             command=lambda: controller.next_frame(Schools))
        button3.pack(pady=5)

        group.place(relx=0.5, rely=0.4, anchor="center")


class Header(ttk.Frame):
    """
    Represents a page header.

    Titles the page and offers back and homepage buttons.
    """

    def __init__(self, parent, controller, title):
        ttk.Frame.__init__(self, parent)

        title = ttk.Label(self, text=title, font=controller.title_font)
        title.pack(side="left")
        button = ttk.Button(self, text="Go to the homepage",
                            command=lambda: controller.next_frame(Homepage))
        button.pack(side="right")
        button = ttk.Button(self, text="Go back",
                            command=lambda: controller.next_frame(controller.last_frame))
        button.pack(side="right", padx=5)


def valid_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def valid_time(time):
    try:
        datetime.datetime.strptime(time, '%H:%M:%S')
        return True
    except ValueError:
        return False


class Form(ttk.Frame):
    """
    Represents a form.

    Offers user input to all columns associated with a table.
    """

    def __init__(self, parent, controller, table_name):
        ttk.Frame.__init__(self, parent)

        cur = controller.cnx.cursor()
        cur.callproc("get_columns_from_table", (table_name, db_name,))
        self.column_data = cur.fetchall()
        cur.close()

        entries = {}
        for row in self.column_data:
            section = ttk.Frame(self)
            if row["COLUMN_KEY"] != "PRI":
                field = row["COLUMN_NAME"]
                data_type = row["DATA_TYPE"]
                is_nullable = row["IS_NULLABLE"] == 'YES'
                input_info = data_type
                if not is_nullable:
                    input_info += '*'
                label = ttk.Label(section, width=22, anchor='w',
                                  text=f"{field} ({input_info}): ")
                entry = ttk.Entry(section)
                section.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                label.pack(side=tk.LEFT)
                entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                entries[field] = entry
        self.entries = entries

    def valid_entries(self):
        for row in self.column_data:

            field = row["COLUMN_NAME"]
            if field in self.entries:

                data_type = row["DATA_TYPE"]
                is_nullable = row["IS_NULLABLE"] == 'YES'
                value = self.entries[field].get()

                input_requirement = ''
                if value == '':
                    if not is_nullable:
                        input_requirement = "is not nullable"
                elif data_type == 'int':
                    is_int = value.isdigit()
                    if not is_int:
                        input_requirement = "requires integer input"
                elif data_type == 'date':
                    is_date = valid_date(value)
                    if not is_date:
                        input_requirement = "requires date input (YYYY-MM-DD)"
                elif data_type == 'time':
                    is_time = valid_time(value)
                    if not is_time:
                        input_requirement = "requires time input (HH:MM:SS)"

                if input_requirement != '':
                    messagebox.showerror("Error", f"{field} {input_requirement}, please edit and try again.")
                    return False

        return True


class CreateForm(ttk.Frame):
    """
    Represents a create form.

    On create validates user input and submits input to database.
    """

    def __init__(self, parent, controller, table_name):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.table_name = table_name

        self.form = Form(parent=self, controller=controller, table_name=table_name)
        self.form.pack()

        button = ttk.Button(self, text=f"Create {table_name}",
                            command=lambda: self.create())
        button.pack(pady=5)

    def create(self):

        if self.form.valid_entries():
            columns = []
            values = []
            for field, entry in self.form.entries.items():
                columns.append(field)
                values.append(f"'{entry.get()}'")

            sql = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"

            try:
                cur = self.controller.cnx.cursor()
                cur.execute(sql)
                self.controller.cnx.commit()
                self.controller.refresh()
            except Exception as e:
                messagebox.showerror("Error", f"{e.args[0]}: {e.args[1]}")


class UpdateForm(ttk.Frame):
    """
    Represents an update form.

    On update validates user input and submits input to database.
    On delete submits delete request to database.
    """

    def __init__(self, parent, controller, table_name, entity_id):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.table_name = table_name
        self.entity_id = entity_id

        sql = f"SELECT * FROM {self.table_name} WHERE id={self.entity_id}"

        cur = self.controller.cnx.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        entity = rows[0]
        cur.close()

        self.form = Form(parent=self, controller=controller, table_name=table_name)
        self.form.pack()

        for field, entry in self.form.entries.items():
            text = ''
            if entity[field]:
                text = entity[field]
            entry.insert(0, text)

        button1 = ttk.Button(self, text=f"Update {table_name}",
                             command=lambda: self.update())
        button1.pack(pady=5)
        button2 = ttk.Button(self, text=f"Delete {table_name}",
                             command=lambda: self.delete())
        button2.pack()

    def update(self):

        if self.form.valid_entries():
            col_val_pairings = []
            for field, entry in self.form.entries.items():

                if entry.get() == '':
                    col_val_pairings.append(f"{field} = NULL")
                else:
                    col_val_pairings.append(f"{field} = '{entry.get()}'")

            sql = f"UPDATE {self.table_name} SET {', '.join(col_val_pairings)} WHERE id={self.entity_id}"

            try:
                cur = self.controller.cnx.cursor()
                cur.execute(sql)
                self.controller.cnx.commit()
                cur.close()
                self.controller.refresh()
            except Exception as e:
                messagebox.showerror("Error", f"{e.args[0]}: {e.args[1]}")

    def delete(self):

        sql = f"DELETE FROM {self.table_name} WHERE id={self.entity_id}"

        try:
            cur = self.controller.cnx.cursor()
            cur.execute(sql)
            self.controller.cnx.commit()
            cur.close()
            self.controller.next_frame(self.controller.last_frame)
        except Exception as e:
            messagebox.showerror("Error", f"{e.args[0]}: {e.args[1]}")


class Tournaments(ttk.Frame):
    """
    Represents the tournaments view.

    Offers tournament creation and specific tournament selection.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        header = Header(parent=self, controller=controller, title="Tournaments")
        header.pack(fill="x", pady=10, padx=10)

        # Setup new tournament form
        create_tournament = CreateForm(parent=self, controller=controller, table_name="tournament")
        create_tournament.pack(fill="x", pady=10, padx=10)

        # Request all tournament information
        cur = controller.cnx.cursor()
        cur.callproc("view_all_tournaments")
        tournaments = cur.fetchall()
        cur.close()

        # Setup Tournament Grid
        tournament_grid = ttk.Frame(self)
        tournament_grid.grid_columnconfigure(0, weight=1)
        tournament_grid.grid_columnconfigure(1, weight=1)
        tournament_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(tournaments) / 3)):
            tournament_grid.grid_rowconfigure(y, weight=1)

        # Add tournaments to grid
        count = 0
        for tournament in tournaments:
            name = tournament["name"]
            date = tournament["date"]
            address = tournament["address"]
            button_text = f"{name}\n" \
                          f"{date}\n" \
                          f"{address}"
            button = ttk.Button(tournament_grid, text=button_text,
                                command=lambda to_id=tournament["id"]: self.select_tournament(to_id))
            button.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1

        tournament_grid.pack(fill="both", expand=True, pady=10, padx=10)

    def select_tournament(self, to_id):
        self.controller.to_id = to_id
        self.controller.next_frame(Tournament)


class Tournament(ttk.Frame):
    """
    Represents a specific tournament view.

    Presents tournament data, offers tournament deletion/editing, and division selection.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        header = Header(parent=self, controller=controller, title=f"Tournament {controller.to_id}")
        header.pack(fill="x", pady=10, padx=10)

        # Setup new tournament form
        update_tournament = \
            UpdateForm(parent=self, controller=controller, table_name="tournament", entity_id=controller.to_id)
        update_tournament.pack(fill="x", pady=10, padx=10)

        # Request tournament's divisions
        cur = controller.cnx.cursor()
        cur.callproc("view_all_tournament_divisions", (controller.to_id,))
        divisions = cur.fetchall()
        cur.close()

        division_grid = ttk.Frame(self)
        division_grid.grid_columnconfigure(0, weight=1)
        division_grid.grid_columnconfigure(1, weight=1)
        division_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(divisions) / 3)):
            division_grid.grid_rowconfigure(y, weight=1)

        count = 0
        for division in divisions:
            name = division["name"]
            button_text = f"{name}\n"
            button = ttk.Button(division_grid, text=button_text,
                                command=lambda d_id=division["id"]: self.select_division(d_id))
            button.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1
        division_grid.pack(fill="both", expand=True, pady=10, padx=10)

        # Setup new division form
        create_division = CreateForm(parent=self, controller=controller, table_name="division")
        create_division.pack(fill="x", pady=10, padx=10)
        create_division.form.entries["tournament_id_FK"].insert(0, controller.to_id)
        create_division.form.entries["tournament_id_FK"].config(state="disabled")

    def select_division(self, d_id):
        self.controller.d_id = d_id
        self.controller.next_frame(Division)


class Division(ttk.Frame):
    """
    Represents a specific division view.

    Presents division data and the division's teams and matches.
    Offers division deletion/editing and division team/match creation.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        header = Header(parent=self, controller=controller, title=f"Division {controller.d_id}")
        header.pack(fill="x", pady=10, padx=10)

        # Setup new tournament form
        update_division = \
            UpdateForm(parent=self, controller=controller, table_name="division", entity_id=controller.d_id)
        update_division.pack(fill="x", pady=10, padx=10)

        # Setup tabbing
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Teams tab
        teams_tab = DivisionTeams(parent=notebook, controller=controller)
        teams_tab.pack(fill='both', expand=True)

        # Matches tab
        matches_tab = DivisionMatches(parent=notebook, controller=controller)
        matches_tab.pack(fill='both', expand=True)

        notebook.add(teams_tab, text='Teams')
        notebook.add(matches_tab, text='Matches')


class DivisionMatches(ttk.Frame):
    """
    Represents the matches view for a division.

    Presents match data and offers match creation.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        cur = controller.cnx.cursor()
        cur.callproc("view_all_division_teams", (controller.d_id,))
        teams = cur.fetchall()
        cur.close()

        team_id_to_name = {}

        for team in teams:
            team_id = team["id"]
            name = team["name"]
            team_id_to_name[team_id] = name

        cur = controller.cnx.cursor()
        cur.callproc("view_all_division_matches", (controller.d_id,))
        matches = cur.fetchall()
        cur.close()

        match_grid = ttk.Frame(self)
        match_grid.grid_columnconfigure(0, weight=1)
        match_grid.grid_columnconfigure(1, weight=1)
        match_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(matches) / 3)):
            match_grid.grid_rowconfigure(y, weight=1)

        count = 0
        for match in matches:
            team1_id = match["team1_id_FK"]
            team2_id = match["team2_id_FK"]
            button_text = f"{team_id_to_name[team1_id]} vs. {team_id_to_name[team2_id]}"
            button = ttk.Button(match_grid, text=button_text, command=lambda m_id=match["id"]: self.select_match(m_id))
            button.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1
        match_grid.pack(fill="both", expand=True, pady=10, padx=10)

        create_team = CreateForm(parent=self, controller=controller, table_name="match_data")
        create_team.pack(fill="x", pady=10, padx=10)
        create_team.form.entries["division_id_FK"].insert(0, controller.d_id)
        create_team.form.entries["division_id_FK"].config(state="disabled")

    def select_match(self, m_id):
        self.controller.m_id = m_id
        self.controller.next_frame(Match)


class Match(ttk.Frame):
    """
    Represents the match view.

    Offers game info updating.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        header = Header(parent=self, controller=controller, title=f"Match {controller.m_id}")
        header.pack(fill="x", pady=10, padx=10)

        # Setup update player form
        update_match = \
            UpdateForm(parent=self, controller=controller, table_name="match_data", entity_id=controller.m_id)
        update_match.pack(fill="x", pady=10, padx=10)

        # Request all game information for a match
        cur = controller.cnx.cursor()
        cur.callproc("view_all_match_games", (controller.m_id,))
        games = cur.fetchall()
        cur.close()

        # Setup Game Grid
        game_grid = ttk.Frame(self)
        game_grid.grid_columnconfigure(0, weight=1)
        game_grid.grid_columnconfigure(1, weight=1)
        game_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(games) / 3)):
            game_grid.grid_rowconfigure(y, weight=1)

        # Add players to grid
        count = 0
        for game in games:
            game_frame = ttk.Frame(game_grid)
            game_frame['borderwidth'] = 5
            game_frame['relief'] = 'sunken'
            header = ttk.Label(game_frame, text=f"Game {count + 1}", font=controller.title_font)
            header.pack(padx=5, pady=5)

            team1_label = ttk.Label(game_frame, text="Team 1 Score:")
            team1_label.pack()
            team1_entry = ttk.Entry(game_frame)
            team1_entry.pack()

            team2_label = ttk.Label(game_frame, text="Team 2 Score:")
            team2_label.pack()
            team2_entry = ttk.Entry(game_frame)
            team2_entry.pack()

            button = ttk.Button(game_frame, text="Update Score",
                                command=lambda g_id=game["id"], t1_score=team1_entry.get(), t2_score=team2_entry.get():
                                self.update_game(g_id, t1_score, t2_score))
            button.pack(padx=5, pady=5)

            game_frame.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1

        game_grid.pack(fill="both", expand=True, pady=10, padx=10)

    def update_game(self, g_id, t1_score, t2_score):
        sql = f"UPDATE game_data SET team1_score = {t1_score}, team2_score = {t2_score} WHERE id={g_id}"

        try:
            cur = self.controller.cnx.cursor()
            cur.execute(sql)
            self.controller.cnx.commit()
            cur.close()
            self.controller.refresh()
        except Exception as e:
            messagebox.showerror("Error", f"{e.args[0]}: {e.args[1]}")


class DivisionTeams(ttk.Frame):
    """
    Represents the teams view for a division.

    Presents team data and offers team creation.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        cur = controller.cnx.cursor()
        cur.callproc("view_all_division_teams", (controller.d_id,))
        teams = cur.fetchall()
        cur.close()

        team_grid = ttk.Frame(self)
        team_grid.grid_columnconfigure(0, weight=1)
        team_grid.grid_columnconfigure(1, weight=1)
        team_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(teams) / 3)):
            team_grid.grid_rowconfigure(y, weight=1)

        count = 0
        for team in teams:
            team_id = team["id"]
            name = team["name"]
            button_text = f"{name}"
            button = ttk.Button(team_grid, text=button_text, command=lambda te_id=team_id: self.select_team(te_id))
            button.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1
        team_grid.pack(fill="both", expand=True, pady=10, padx=10)

        create_team = CreateForm(parent=self, controller=controller, table_name="team")
        create_team.pack(fill="x", pady=10, padx=10)
        create_team.form.entries["division_id_FK"].insert(0, controller.d_id)
        create_team.form.entries["division_id_FK"].config(state="disabled")

    def select_team(self, te_id):
        self.controller.te_id = te_id
        self.controller.next_frame(Team)


class Team(ttk.Frame):
    """
    Represents a specific team view.

    Presents team data and offers team deletion/editing.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        header = Header(parent=self, controller=controller, title=f"Team {controller.te_id}")
        header.pack(fill="x", pady=10, padx=10)

        # Setup new tournament form
        update_team = \
            UpdateForm(parent=self, controller=controller, table_name="team", entity_id=controller.te_id)
        update_team.pack(fill="x", pady=10, padx=10)

        # Request tournament's divisions
        cur = controller.cnx.cursor()
        cur.callproc("view_all_team_players", (controller.te_id,))
        players = cur.fetchall()
        cur.close()

        player_grid = ttk.Frame(self)
        player_grid.grid_columnconfigure(0, weight=1)
        player_grid.grid_columnconfigure(1, weight=1)
        player_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(players) / 3)):
            player_grid.grid_rowconfigure(y, weight=1)

        count = 0
        for player in players:
            name = player["name"]
            button_text = f"{name}\n"
            button = ttk.Button(player_grid, text=button_text,
                                command=lambda p_id=player["id"]: self.select_player(p_id))
            button.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1
        player_grid.pack(fill="both", expand=True, pady=10, padx=10)

    def select_player(self, p_id):
        self.controller.p_id = p_id
        self.controller.next_frame(Player)


class Players(ttk.Frame):
    """
    Represents the players view.

    Offers player creation and specific player selection.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        header = Header(parent=self, controller=controller, title="Players")
        header.pack(fill="x", pady=10, padx=10)

        # Setup new player form
        create_player = CreateForm(parent=self, controller=controller, table_name="player")
        create_player.pack(fill="x", pady=10, padx=10)

        # Request all player information
        cur = controller.cnx.cursor()
        cur.callproc("view_all_players")
        players = cur.fetchall()
        cur.close()

        # Setup Player Grid
        player_grid = ttk.Frame(self)
        player_grid.grid_columnconfigure(0, weight=1)
        player_grid.grid_columnconfigure(1, weight=1)
        player_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(players) / 3)):
            player_grid.grid_rowconfigure(y, weight=1)

        # Add players to grid
        count = 0
        for player in players:
            name = player["name"]
            date = player["dob"]
            phone = player["phone_number"]
            button_text = f"{name}\n" \
                          f"{date}\n" \
                          f"{phone}"
            button = ttk.Button(player_grid, text=button_text,
                                command=lambda p_id=player["id"]: self.select_player(p_id))
            button.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1

        player_grid.pack(fill="both", expand=True, pady=10, padx=10)

    def select_player(self, p_id):
        self.controller.p_id = p_id
        self.controller.next_frame(Player)


class Player(ttk.Frame):
    """
    Represents a specific player view.

    Presents player data and offers player deletion/editing.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        header = Header(parent=self, controller=controller, title=f"Player {controller.p_id}")
        header.pack(fill="x", pady=10, padx=10)

        # Setup update player form
        update_player = \
            UpdateForm(parent=self, controller=controller, table_name="player", entity_id=controller.p_id)
        update_player.pack(fill="x", pady=10, padx=10)


class Schools(ttk.Frame):
    """
    Represents the schools view.

    Offers school creation and specific school selection.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        header = Header(parent=self, controller=controller, title="Schools")
        header.pack(fill="x", pady=10, padx=10)

        # Setup new tournament form
        create_tournament = CreateForm(parent=self, controller=controller, table_name="school")
        create_tournament.pack(fill="x", pady=10, padx=10)

        # Request all tournament information
        cur = controller.cnx.cursor()
        cur.callproc("view_all_schools")
        schools = cur.fetchall()
        cur.close()

        # Setup Tournament Grid
        school_grid = ttk.Frame(self)
        school_grid.grid_columnconfigure(0, weight=1)
        school_grid.grid_columnconfigure(1, weight=1)
        school_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(schools) / 3)):
            school_grid.grid_rowconfigure(y, weight=1)

        # Add tournaments to grid
        count = 0
        for school in schools:
            name = school["name"]
            address = school["address"]
            button_text = f"{name}\n" \
                          f"{address}"
            button = ttk.Button(school_grid, text=button_text,
                                command=lambda s_id=school["id"]: self.select_school(s_id))
            button.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1

        school_grid.pack(fill="both", expand=True, pady=10, padx=10)

    def select_school(self, s_id):

        self.controller.s_id = s_id
        self.controller.next_frame(School)


class School(ttk.Frame):
    """
    Represents a specific school view.

    Presents school data and offers school deletion/editing.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        header = Header(parent=self, controller=controller, title=f"School {controller.s_id}")
        header.pack(fill="x", pady=10, padx=10)

        # Setup new tournament form
        update_school = \
            UpdateForm(parent=self, controller=controller, table_name="school", entity_id=controller.s_id)
        update_school.pack(fill="x", pady=10, padx=10)

        # Request tournament's divisions
        cur = controller.cnx.cursor()
        cur.callproc("get_players_from_school", (controller.s_id,))
        players = cur.fetchall()
        cur.close()

        player_grid = ttk.Frame(self)
        player_grid.grid_columnconfigure(0, weight=1)
        player_grid.grid_columnconfigure(1, weight=1)
        player_grid.grid_columnconfigure(2, weight=1)
        for y in range(math.ceil(len(players) / 3)):
            player_grid.grid_rowconfigure(y, weight=1)

        count = 0
        for player in players:
            name = player["name"]
            button_text = f"{name}\n"
            button = ttk.Button(player_grid, text=button_text,
                                command=lambda p_id=player["id"]: self.select_player(p_id))
            button.grid(row=math.trunc(count / 3), column=count % 3, sticky="nsew")
            count += 1
        player_grid.pack(fill="both", expand=True, pady=10, padx=10)

    def select_player(self, p_id):
        self.controller.p_id = p_id
        self.controller.next_frame(Player)


if __name__ == "__main__":
    app = App()
    app.mainloop()
