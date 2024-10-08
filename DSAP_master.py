import turtle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, colorchooser, simpledialog
import customtkinter as ctk
import time
import random
import uuid
import firebase_admin
from firebase_admin import credentials, db
from ttkthemes import ThemedTk
import webbrowser
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

cred = credentials.Certificate("nails-36418-firebase-adminsdk-cmi75-307c4a5b03.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://nails-36418-default-rtdb.firebaseio.com/"}
)

settings = {"resolution": "1024x768", "background": "#359e56", "audio": True}
nail_options = {"nail_color": "black", "nail_size": 10}
string_options = {"string_color": "white", "string_thickness": 3}
nails = []
current_nail = 0
num_nails = 0
user_id = str(uuid.uuid4())
user_name = "Player"
selected_user_id = None
drawing_started_at = None
is_editing = False
pen = None
screen = None
game_root_single = None
game_root_multi = None
waiting_screen = None
chat_window = None
hints_window = None
game_ended = False


def splash_screen():
    root = ctk.CTk()
    root.title("DTAP v1.0 | By: Yair K.")
    window_width = 500
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    title_label = ctk.CTkLabel(
        frame, text="Digital String Art Platform", font=("Monaco", 26, "bold")
    )
    title_label.pack(pady=30)

    def singleplayer_mode():
        singleplayer_window = ctk.CTkToplevel()
        singleplayer_window.title("Single Player Mode")
        singleplayer_window.geometry("400x200")
        ctk.CTkLabel(
            singleplayer_window, text="Choose Mode:", font=("Monaco", 16)
        ).pack(pady=10)

        def free_draw_mode():
            singleplayer_window.destroy()
            open_free_draw_mode()

        def vs_ai_mode():
            singleplayer_window.destroy()
            open_vs_ai_mode()

        free_draw_button = ctk.CTkButton(
            singleplayer_window, text="Free Draw", command=free_draw_mode
        )
        free_draw_button.pack(pady=10)
        vs_ai_button = ctk.CTkButton(
            singleplayer_window, text="Vs AI", command=vs_ai_mode
        )
        vs_ai_button.pack(pady=10)

        def on_close():
            singleplayer_window.destroy()
            splash_screen()

        singleplayer_window.protocol("WM_DELETE_WINDOW", on_close)

    singleplayer_button = ctk.CTkButton(
        frame,
        text="Single Player Game",
        font=("Monaco", 18),
        command=lambda: [root.destroy(), singleplayer_mode()],
    )
    singleplayer_button.pack(pady=10)
    multiplayer_button = ctk.CTkButton(
        frame,
        text="Multiplayer Game",
        font=("Monaco", 18),
        command=lambda: [root.destroy(), start_multiplayer()],
    )
    multiplayer_button.pack(pady=10)
    settings_button = ctk.CTkButton(
        frame, text="Settings", font=("Monaco", 18), command=open_settings
    )
    settings_button.pack(pady=10)
    info_button = ctk.CTkButton(
        frame, text="Info", font=("Monaco", 18), command=open_info
    )
    info_button.pack(pady=10)
    clean_up_old_users()
    root.mainloop()


def send_to_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Based on this description of a string art drawing: '{prompt}', what do you think the player is drawing?",
                }
            ],
        )
        messagebox.showinfo(
            "AI's Guess", response.choices[0].message["content"].strip()
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def open_vs_ai_mode():
    global pen, screen, nails, current_nail, num_nails, game_root_single, prompt
    reset_game_variables_single()

    prompt = get_random_prompt()
    messagebox.showinfo("Your Drawing Prompt", f"Draw the following: {prompt}")

    ask_for_nails_free_draw()

    if not screen or not screen._root:
        screen = turtle.Screen()
    else:
        try:
            screen.reset()
        except turtle.Terminator:
            screen = turtle.Screen()
    screen.setup(
        width=int(settings["resolution"].split("x")[0]),
        height=int(settings["resolution"].split("x")[1]),
    )
    screen.bgcolor(settings["background"])
    screen.title("Digital String Art - Vs AI Mode")
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    game_root_single = ctk.CTk()
    game_root_single.title("Digital String Art - Vs AI Mode")
    window_width, window_height = map(int, settings["resolution"].split("x"))
    game_root_single.geometry(f"{window_width}x200")

    taskbar_frame = ctk.CTkFrame(game_root_single, corner_radius=10)
    taskbar_frame.pack(fill="both", padx=20, pady=10)

    ctk.CTkLabel(taskbar_frame, text="Nail Size:", font=("Monaco", 12)).grid(
        row=0, column=0, padx=5, pady=5
    )
    nail_size_var = tk.IntVar(value=nail_options["nail_size"])
    nail_size_entry = ctk.CTkEntry(taskbar_frame, textvariable=nail_size_var, width=50)
    nail_size_entry.grid(row=0, column=1, padx=5, pady=5)

    def choose_nail_color():
        color_code = colorchooser.askcolor(title="Choose Nail Color")
        if color_code:
            nail_options["nail_color"] = color_code[1]

    nail_color_button = ctk.CTkButton(
        taskbar_frame, text="Nail Color", command=choose_nail_color
    )
    nail_color_button.grid(row=0, column=2, padx=5, pady=5)

    def choose_string_color():
        color_code = colorchooser.askcolor(title="Choose String Color")
        if color_code:
            string_options["string_color"] = color_code[1]

    string_color_button = ctk.CTkButton(
        taskbar_frame, text="String Color", command=choose_string_color
    )
    string_color_button.grid(row=1, column=2, padx=5, pady=5)

    cost_label = ctk.CTkLabel(taskbar_frame, text="Total Cost: $0.00")
    cost_label.grid(row=1, column=0, padx=5, pady=5)

    def reset_canvas_free_draw():
        if screen:
            screen.clear()
        cost_label.configure(text="Total Cost: $0.00")

    reset_button = ctk.CTkButton(
        taskbar_frame, text="Clear Canvas", command=reset_canvas_free_draw
    )
    reset_button.grid(row=0, column=3, padx=5, pady=5)

    send_ai_button = ctk.CTkButton(
        taskbar_frame, text="Send to AI", command=lambda: send_to_ai(prompt)
    )
    send_ai_button.grid(row=1, column=3, padx=5, pady=5)

    exit_button = ctk.CTkButton(
        taskbar_frame,
        text="Back to Main Menu",
        command=lambda: [reset_game_variables_single(), splash_screen()],
    )
    exit_button.grid(row=0, column=5, rowspan=2, padx=10, pady=5)

    def update_options():
        try:
            nail_options["nail_size"] = int(nail_size_var.get())
        except ValueError:
            nail_options["nail_size"] = 10
        game_root_single.after(500, update_options)

    update_options()
    screen.onscreenclick(lambda x, y: place_nail_free_draw(x, y, cost_label))
    game_root_single.mainloop()


def get_ai_guess(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Based on this description of a string art drawing: '{prompt}', what do you think the player is drawing?",
                }
            ],
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"


def get_user_info():
    global user_id, user_name
    user_id = str(uuid.uuid4())
    user_name_input = ctk.CTkInputDialog(
        text="Enter your name:", title="User Name"
    ).get_input()
    if user_name_input:
        user_name = user_name_input
    else:
        user_name = "Player"


def start_multiplayer():
    get_user_info()
    start_multiplayer_lobby()


def start_multiplayer_lobby():
    global user_id, user_name, selected_user_id
    user_data = {
        "name": user_name,
        "status": "online",
        "invitation": None,
        "game_session": None,
        "timestamp": time.time(),
    }
    users_ref = db.reference("lobby/users")
    users_ref.child(user_id).set(user_data)
    lobby_root = ctk.CTk()
    lobby_root.title("Multiplayer Lobby")
    window_width = 500
    window_height = 450
    screen_width = lobby_root.winfo_screenwidth()
    screen_height = lobby_root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    lobby_root.geometry(
        f"{window_width}x{window_height}+{position_right}+{position_top}"
    )
    connected_frame = ctk.CTkFrame(lobby_root, corner_radius=10)
    connected_frame.pack(expand=True, fill="both", padx=20, pady=20)
    ctk.CTkLabel(connected_frame, text="Connected Players", font=("Monaco", 20)).pack(
        pady=10
    )
    player_listbox = tk.Listbox(connected_frame, height=5, font=("Monaco", 14))
    player_listbox.pack(pady=10)
    selected_user_id = tk.StringVar()
    status_label = ctk.CTkLabel(connected_frame, text="", font=("Monaco", 14))
    status_label.pack(pady=10)

    def refresh_players():
        player_listbox.delete(0, tk.END)
        all_users = users_ref.get()
        if all_users:
            for uid, user in all_users.items():
                if uid != user_id and user.get("status") == "online":
                    player_listbox.insert(tk.END, f"{user['name']} ({uid})")
        else:
            player_listbox.insert(tk.END, "No other players online")

    refresh_button = ctk.CTkButton(
        connected_frame, text="Refresh", command=refresh_players
    )
    refresh_button.pack(pady=10)

    def send_invitation():
        selection = player_listbox.curselection()
        if selection:
            selected_text = player_listbox.get(selection[0])
            selected_uid = selected_text.split("(")[-1].strip(")")
            selected_user_id.set(selected_uid)
            users_ref.child(selected_uid).child("invitation").set(
                {"from": user_id, "status": "pending"}
            )
            status_label.configure(text="Invitation sent. Waiting for response...")
            check_invitation_status()
        else:
            messagebox.showwarning("No Selection", "Please select a player to invite.")

    invite_button = ctk.CTkButton(
        connected_frame, text="Send Invitation", command=send_invitation
    )
    invite_button.pack(pady=10)

    def check_invitation_status():
        invitation_ref = users_ref.child(user_id).child("invitation")
        invitation = invitation_ref.get()
        if invitation:
            if invitation.get("status") == "accepted":
                game_session_id = invitation.get("game_session")
                lobby_root.after(
                    0,
                    lambda: [
                        lobby_root.destroy(),
                        start_multiplayer_game(game_session_id),
                    ],
                )
            elif invitation.get("status") == "declined":
                messagebox.showinfo(
                    "Invitation Declined", "The player declined your invitation."
                )
                invitation_ref.delete()
                status_label.configure(text="")
            else:
                lobby_root.after(1000, check_invitation_status)
        else:
            lobby_root.after(1000, check_invitation_status)

    def check_for_invitations():
        invitation_ref = users_ref.child(user_id).child("invitation")
        invitation = invitation_ref.get()
        if invitation and invitation.get("status") == "pending":
            inviter_id = invitation.get("from")
            inviter_name = users_ref.child(inviter_id).child("name").get()

            def handle_invitation():
                response = messagebox.askyesno(
                    "Game Invitation",
                    f"{inviter_name} has invited you to play. Accept?",
                )
                if response:
                    game_session_id = str(uuid.uuid4())
                    players = [inviter_id, user_id]
                    random.shuffle(players)
                    drawer_id = players[0]
                    guesser_id = players[1]
                    game_session_ref = db.reference(f"games/{game_session_id}")
                    game_data = {
                        "drawer": drawer_id,
                        "guesser": guesser_id,
                        "state": "waiting_for_prompt",
                        "prompt": None,
                        "drawing": None,
                        "guess": None,
                        "game_result": None,
                        "drawing_started_at": None,
                        "hint_level": 0,
                        "current_hint": "",
                        "guess_attempts": 0,
                        "guesses": {},
                        "hints": {},
                    }
                    game_session_ref.set(game_data)
                    users_ref.child(user_id).update(
                        {"game_session": game_session_id, "status": "in-game"}
                    )
                    users_ref.child(inviter_id).update(
                        {"game_session": game_session_id, "status": "in-game"}
                    )
                    invitation_ref.update(
                        {"status": "accepted", "game_session": game_session_id}
                    )
                    users_ref.child(inviter_id).child("invitation").update(
                        {"status": "accepted", "game_session": game_session_id}
                    )
                    lobby_root.after(
                        0,
                        lambda: [
                            lobby_root.destroy(),
                            start_multiplayer_game(game_session_id),
                        ],
                    )
                else:
                    invitation_ref.update({"status": "declined"})
                    users_ref.child(inviter_id).child("invitation").update(
                        {"status": "declined"}
                    )

            lobby_root.after(0, handle_invitation)
        else:
            lobby_root.after(1000, check_for_invitations)

    check_for_invitations()

    def on_lobby_close():
        users_ref.child(user_id).delete()
        lobby_root.destroy()

    lobby_root.protocol("WM_DELETE_WINDOW", on_lobby_close)
    clean_up_old_users()
    refresh_players()
    lobby_root.mainloop()


def clean_up_old_users():
    users_ref = db.reference("lobby/users")
    all_users = users_ref.get()
    current_time = time.time()
    if all_users:
        for uid, user in all_users.items():
            last_active = user.get("timestamp", 0)
            if current_time - last_active > 300:
                users_ref.child(uid).delete()


def start_multiplayer_game(game_session_id):
    global user_id, user_name
    game_session_ref = db.reference(f"games/{game_session_id}")
    game_data = game_session_ref.get()
    if not game_data:
        messagebox.showerror("Error", "Game session not found.")
        return
    if user_id == game_data["drawer"]:
        player_role = "drawer"
    elif user_id == game_data["guesser"]:
        player_role = "guesser"
    else:
        messagebox.showerror("Error", "You are not part of this game.")
        return
    instruction_text = f"You are the {player_role}.\n"
    if player_role == "drawer":
        instruction_text += "You will receive a prompt to draw. Place the nails and create your string art.\n\nOnce you are ready, click 'Send Drawing' to send it to the guesser.\n"
    else:
        instruction_text += "Wait for the drawer to create their string art.\n\nOnce the drawing is ready, you can start guessing.\n"
    instruction_window = ctk.CTk()
    instruction_window.title("Game Instructions")
    instruction_window.geometry("400x300")
    ctk.CTkLabel(
        instruction_window, text=instruction_text, font=("Monaco", 14), wraplength=380
    ).pack(pady=20)

    def proceed_to_game():
        instruction_window.destroy()
        game_loop(game_session_id, player_role)

    proceed_button = ctk.CTkButton(
        instruction_window, text="Continue", command=proceed_to_game
    )
    proceed_button.pack(pady=10)
    instruction_window.mainloop()


def game_loop(game_session_id, player_role):
    global user_id
    game_session_ref = db.reference(f"games/{game_session_id}")
    if player_role == "drawer":
        prompt = get_random_prompt()
        game_session_ref.update(
            {
                "prompt": prompt,
                "state": "drawing",
                "drawing_started_at": time.time(),
                "hint_level": 0,
                "current_hint": "",
                "hints": {},
            }
        )
        start_drawing(game_session_id, prompt)
    elif player_role == "guesser":
        wait_for_drawing_ready(game_session_id)


def get_random_prompt():
    prompts = [
        "House",
        "Tree",
        "Car",
        "Cat",
        "Dog",
        "Sun",
        "Flower",
        "Boat",
        "Bird",
        "Fish",
        "Bicycle",
        "Ice Cream",
        "Apple",
        "Star",
        "Cloud",
        "Moon",
        "Pencil",
        "Cake",
        "Hat",
        "Balloon",
        "Guitar",
        "Robot",
        "Cupcake",
        "Elephant",
        "Lion",
        "Train",
        "Heart",
        "Spider",
        "Kite",
        "Castle",
        "Snowman",
        "Pumpkin",
        "Turtle",
        "Rainbow",
        "Shark",
        "Octopus",
        "Ladybug",
        "Scissors",
        "Key",
        "Musical Note",
        "Drum",
        "Coffee Cup",
        "Book",
        "Sunglasses",
        "Telephone",
        "Candle",
        "Worm",
        "Teddy Bear",
        "Fire",
        "Grass",
        "Butterfly",
        "Mushroom",
        "Cactus",
        "Anchor",
        "Ice Cube",
        "Sailboat",
        "Laptop",
        "Camera",
        "Soccer Ball",
        "Baseball Bat",
        "Skateboard",
        "Glasses",
        "Map",
        "Treasure Chest",
        "Crab",
        "Pineapple",
        "Snowflake",
        "Candy",
        "Zebra",
        "Penguin",
        "Dolphin",
        "Frog",
        "Rocket",
        "Alien",
        "Grapes",
        "Corn",
        "Donut",
        "Hot Air Balloon",
        "Yacht",
        "Whale",
    ]
    return random.choice(prompts)


def start_drawing(game_session_id, prompt):
    global user_id, num_nails, drawing_started_at
    prompt_window = ctk.CTk()
    prompt_window.title("Your Drawing Prompt")
    prompt_window.geometry("300x150")
    ctk.CTkLabel(
        prompt_window, text=f"Your prompt is: {prompt}", font=("Monaco", 16)
    ).pack(pady=20)

    def proceed_to_draw():
        prompt_window.destroy()
        ask_for_nails()
        start_turtle_program(
            is_multiplayer=True, is_drawing=True, game_session_id=game_session_id
        )
        drawing_started_at = time.time()

    proceed_button = ctk.CTkButton(
        prompt_window, text="Continue", command=proceed_to_draw
    )
    proceed_button.pack(pady=10)
    prompt_window.mainloop()


def wait_for_drawing_ready(game_session_id):
    global waiting_screen
    game_session_ref = db.reference(f"games/{game_session_id}")
    waiting_screen = ctk.CTk()
    waiting_screen.title("Waiting for Drawing")
    waiting_screen.geometry("400x200")
    waiting_label = ctk.CTkLabel(
        waiting_screen, text="Player is drawing...", font=("Monaco", 16)
    )
    waiting_label.pack(pady=50)

    def check_drawing_ready():
        if not waiting_screen.winfo_exists():
            return
        game_data = game_session_ref.get()
        if game_data.get("state") == "guessing":
            waiting_screen.destroy()
            start_turtle_program(
                is_multiplayer=True, is_drawing=False, game_session_id=game_session_id
            )
        elif game_data.get("state") == "ended":
            waiting_screen.destroy()
            messagebox.showinfo("Game Ended", "The drawer has left the game.")
            return_to_lobby()
        else:
            if waiting_screen.winfo_exists():
                waiting_screen.after(1000, check_drawing_ready)

    waiting_screen.after(0, check_drawing_ready)
    waiting_screen.mainloop()


def start_turtle_program(is_multiplayer, is_drawing, game_session_id=None):
    global pen, screen, nails, current_nail, num_nails, drawing_started_at
    global is_editing, game_root_single, game_root_multi, game_ended
    nails = []
    current_nail = 0
    is_editing = False
    game_ended = False
    if not screen or not screen._root:
        screen = turtle.Screen()
    else:
        try:
            screen.reset()
        except turtle.Terminator:
            screen = turtle.Screen()
    screen.setup(
        width=int(settings["resolution"].split("x")[0]),
        height=int(settings["resolution"].split("x")[1]),
    )
    screen.bgcolor(settings["background"])
    screen.title("Digital String Art")
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    if is_multiplayer and (is_drawing or not is_drawing):
        if not game_root_multi or not game_root_multi.winfo_exists():
            game_root_multi = ctk.CTk()
            game_root_multi.title("Digital String Art - In-Game Taskbar")
        window_width, window_height = map(int, settings["resolution"].split("x"))
        game_root_multi.geometry(f"{window_width}x150")
        current_game_root = game_root_multi
    else:
        if not game_root_single or not game_root_single.winfo_exists():
            game_root_single = ctk.CTk()
            game_root_single.title("Digital String Art - In-Game Taskbar")
        window_width, window_height = map(int, settings["resolution"].split("x"))
        game_root_single.geometry(f"{window_width}x150")
        current_game_root = game_root_single
    for widget in current_game_root.winfo_children():
        widget.destroy()
    taskbar_frame = ctk.CTkFrame(current_game_root, corner_radius=10)
    taskbar_frame.pack(fill="both", padx=20, pady=10)
    timer_label = ctk.CTkLabel(taskbar_frame, text="Time: 120", font=("Monaco", 16))
    timer_label.pack(side="left", padx=10)
    if is_multiplayer and is_drawing:

        game_session_ref = db.reference(f"games/{game_session_id}")
        game_data = game_session_ref.get()
        prompt = game_data.get("prompt", "")
        prompt_label = ctk.CTkLabel(
            taskbar_frame, text=f"Prompt: {prompt}", font=("Monaco", 16)
        )
        prompt_label.pack(side="left", padx=10)
        reset_button = ctk.CTkButton(
            taskbar_frame,
            text="Reset Canvas",
            font=("Monaco", 16),
            command=lambda: reset_canvas(is_multiplayer, is_drawing, game_session_id),
        )
        reset_button.pack(side="left", padx=10)
        send_button = ctk.CTkButton(
            taskbar_frame,
            text="Send Drawing",
            font=("Monaco", 16),
            command=lambda: send_drawing(is_multiplayer, is_drawing, game_session_id),
        )
        send_button.pack(side="left", padx=10)
        edit_button = ctk.CTkButton(
            taskbar_frame,
            text="Edit Drawing",
            font=("Monaco", 16),
            command=lambda: edit_drawing(is_multiplayer, is_drawing, game_session_id),
        )
        edit_button.pack(side="left", padx=10)
    exit_button = ctk.CTkButton(
        taskbar_frame,
        text="Exit Game",
        font=("Monaco", 16),
        command=lambda: exit_game(game_session_id, is_multiplayer),
    )
    exit_button.pack(side="right", padx=10)

    timer_running = {"running": True}

    def update_timer():
        if not timer_running["running"]:
            return
        global game_ended
        if game_ended:
            return
        if is_multiplayer:
            game_session_ref = db.reference(f"games/{game_session_id}")
            game_data = game_session_ref.get()
            if not game_data:
                return
            elapsed_time = int(
                time.time() - game_data.get("drawing_started_at", time.time())
            )
            time_left = max(0, 120 - elapsed_time)
            timer_label.configure(text=f"Time: {time_left} sec")
            if game_data.get("state") == "ended":
                timer_running["running"] = False
                current_game_root.after(
                    0,
                    lambda: show_stats_and_exit(
                        game_session_id, "drawer" if is_drawing else "guesser"
                    ),
                )
                return
            if game_data.get("state") == "guessing":
                if is_drawing:
                    pass
                else:
                    if elapsed_time >= 45 and game_data.get("hint_level") == 0:
                        prompt = game_data.get("prompt", "")
                        hint_message = f"The word has {len(prompt)} letters."
                        game_session_ref.update({"hint_level": 1})

                        hints_ref = game_session_ref.child("hints")
                        hints_ref.push({"message": hint_message})
                    elif elapsed_time >= 90 and game_data.get("hint_level") == 1:
                        prompt = game_data.get("prompt", "")
                        hint_message = f"The word starts with '{prompt[0]}' and ends with '{prompt[-1]}'."
                        game_session_ref.update({"hint_level": 2})

                        hints_ref = game_session_ref.child("hints")
                        hints_ref.push({"message": hint_message})
                    elif elapsed_time >= 120 and game_data.get("state") != "ended":
                        game_session_ref.update(
                            {
                                "state": "ended",
                                "game_result": "Time Up",
                                "guess_time": time.time(),
                            }
                        )
                        timer_running["running"] = False
                        current_game_root.after(
                            0, lambda: show_stats_and_exit(game_session_id, "guesser")
                        )
                        return
            current_game_root.after(1000, update_timer)
        else:
            pass

    update_timer()
    if is_multiplayer and is_drawing:
        screen.onscreenclick(
            lambda x, y: place_nail(x, y, is_multiplayer, is_drawing, game_session_id)
        )

        def check_game_state_drawer():
            if not timer_running["running"]:
                return
            global game_ended
            if game_ended:
                return
            game_session_ref = db.reference(f"games/{game_session_id}")
            game_data = game_session_ref.get()
            if not game_data:
                return
            if game_data.get("state") == "ended":
                timer_running["running"] = False
                current_game_root.after(
                    0, lambda: show_stats_and_exit(game_session_id, "drawer")
                )
            elif game_data.get("state") == "guessing":

                if not hasattr(start_turtle_program, "chat_window_opened"):
                    open_chat_window_drawer(game_session_id)
                    start_turtle_program.chat_window_opened = True
                else:
                    pass
            else:
                current_game_root.after(1000, check_game_state_drawer)

        check_game_state_drawer()
        current_game_root.mainloop()
    elif is_multiplayer and not is_drawing:

        def fetch_and_draw():
            game_session_ref = db.reference(f"games/{game_session_id}")
            game_data = game_session_ref.get()
            if not game_data:
                messagebox.showerror("Error", "Game session data not found.")
                return_to_lobby()
                return
            nails_data = game_session_ref.child("drawing/nails").get()
            if nails_data:
                nails_list = []
                for key in sorted(nails_data.keys()):
                    nail = nails_data[key]
                    x = nail["x"]
                    y = nail["y"]
                    nails_list.append((x, y))
                draw_string_art_custom(nails_list)
            else:
                messagebox.showerror("Error", "No drawing data found.")
                return_to_lobby()
                return

        fetch_and_draw()

        def check_game_state_guesser():
            if not timer_running["running"]:
                return
            global game_ended
            if game_ended:
                return
            game_session_ref = db.reference(f"games/{game_session_id}")
            game_data = game_session_ref.get()
            if not game_data:
                return
            if game_data.get("state") == "ended":
                timer_running["running"] = False
                current_game_root.after(
                    0, lambda: show_stats_and_exit(game_session_id, "guesser")
                )
            elif game_data.get("state") == "drawing":
                messagebox.showinfo(
                    "Drawing Updated", "The drawer is updating the drawing."
                )
                try:
                    screen.clear()
                except turtle.Terminator:
                    screen = turtle.Screen()
                    screen.setup(
                        width=int(settings["resolution"].split("x")[0]),
                        height=int(settings["resolution"].split("x")[1]),
                    )
                    screen.bgcolor(settings["background"])
                    screen.title("Digital String Art")
                    pen = turtle.Turtle()
                    pen.speed(0)
                    pen.hideturtle()
                wait_for_drawing_ready(game_session_id)
                return
            else:
                current_game_root.after(1000, check_game_state_guesser)

        check_game_state_guesser()
        open_chat_window(game_session_id, current_game_root, timer_label)
    else:
        screen.onscreenclick(lambda x, y: place_nail_singleplayer(x, y))
        if not game_root_single or not game_root_single.winfo_exists():
            game_root_single = ctk.CTk()
            game_root_single.title("Digital String Art - In-Game Taskbar")
            window_width, window_height = map(int, settings["resolution"].split("x"))
            game_root_single.geometry(f"{window_width}x150")
            for widget in game_root_single.winfo_children():
                widget.destroy()
            taskbar_frame_single = ctk.CTkFrame(game_root_single, corner_radius=10)
            taskbar_frame_single.pack(fill="both", padx=20, pady=10)
            timer_label_single = ctk.CTkLabel(
                taskbar_frame_single, text="Time: 0", font=("Monaco", 16)
            )
            timer_label_single.pack(side="left", padx=10)
            exit_button_single = ctk.CTkButton(
                taskbar_frame_single,
                text="Exit to Main Menu",
                font=("Monaco", 16),
                command=lambda: [reset_game_variables_single(), splash_screen()],
            )
            exit_button_single.pack(side="right", padx=10)

            def update_timer_single():
                global game_ended
                if game_ended:
                    return
                elapsed_time = (
                    int(time.time() - drawing_started_at) if drawing_started_at else 0
                )
                timer_label_single.configure(text=f"Time: {elapsed_time} sec")
                game_root_single.after(1000, update_timer_single)

            update_timer_single()
            game_root_single.mainloop()


def reset_canvas(is_multiplayer, is_drawing, game_session_id=None):
    global pen, nails, current_nail, screen
    pen.clear()
    nails = []
    current_nail = 0
    if is_multiplayer and is_drawing:
        drawing_ref = db.reference(f"games/{game_session_id}/drawing")
        drawing_ref.delete()
        game_session_ref = db.reference(f"games/{game_session_id}")
        game_session_ref.update({"state": "drawing"})
        messagebox.showinfo("Canvas Reset", "Your canvas has been reset.")
        try:
            screen.reset()
        except turtle.Terminator:
            screen = turtle.Screen()
            screen.setup(
                width=int(settings["resolution"].split("x")[0]),
                height=int(settings["resolution"].split("x")[1]),
            )
            screen.bgcolor(settings["background"])
            screen.title("Digital String Art")
            pen = turtle.Turtle()
            pen.speed(0)
            pen.hideturtle()
        pen = turtle.Turtle()
        pen.speed(0)
        pen.hideturtle()
        screen.onscreenclick(
            lambda x, y: place_nail(x, y, is_multiplayer, is_drawing, game_session_id)
        )


def send_drawing(is_multiplayer, is_drawing, game_session_id=None):
    global nails, is_editing, screen
    if is_multiplayer and is_drawing:
        if len(nails) < 2:
            messagebox.showwarning(
                "Not Enough Nails",
                "Please place at least 2 nails before sending the drawing.",
            )
            return
        drawing_ref = db.reference(f"games/{game_session_id}/drawing/nails")
        drawing_ref.delete()
        for nail in nails:
            drawing_ref.push({"x": nail[0], "y": nail[1]})
        game_session_ref = db.reference(f"games/{game_session_id}")
        game_session_ref.update({"state": "guessing"})
        messagebox.showinfo(
            "Drawing Sent", "Your drawing has been sent to the guesser."
        )
        is_editing = False

        if not hasattr(send_drawing, "chat_window_opened"):
            open_chat_window_drawer(game_session_id)
            send_drawing.chat_window_opened = True


def edit_drawing(is_multiplayer, is_drawing, game_session_id=None):
    global is_editing, screen
    if is_multiplayer and is_drawing:
        is_editing = True
        messagebox.showinfo("Edit Mode", "You can now add more nails to your drawing.")
        game_session_ref = db.reference(f"games/{game_session_id}")
        game_session_ref.update({"state": "drawing"})
        try:
            screen.reset()
        except turtle.Terminator:
            screen = turtle.Screen()
            screen.setup(
                width=int(settings["resolution"].split("x")[0]),
                height=int(settings["resolution"].split("x")[1]),
            )
            screen.bgcolor(settings["background"])
            screen.title("Digital String Art")
            pen = turtle.Turtle()
            pen.speed(0)
            pen.hideturtle()
        draw_string_art()
        screen.onscreenclick(
            lambda x, y: place_nail(x, y, is_multiplayer, is_drawing, game_session_id)
        )


def place_nail(x, y, is_multiplayer, is_drawing, game_session_id=None):
    global nails, current_nail, num_nails, is_editing
    if current_nail < num_nails or is_editing:
        nail_color = nail_options["nail_color"]
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.dot(nail_options["nail_size"], nail_color)
        nails.append((x, y))
        current_nail += 1
        if current_nail >= num_nails and not is_editing:
            draw_string_art()
        else:
            pass
    else:
        messagebox.showinfo("Limit Reached", "You have placed all nails.")


def place_nail_singleplayer(x, y):
    global nails, current_nail, num_nails, pen
    if current_nail < num_nails:
        nail_color = nail_options["nail_color"]
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.dot(nail_options["nail_size"], nail_color)
        if nails:
            pen.color(string_options["string_color"])
            pen.pensize(string_options["string_thickness"])
            pen.penup()
            pen.goto(nails[-1])
            pen.pendown()
            pen.goto(x, y)
            pen.penup()
            pen.color(nail_color)
        nails.append((x, y))
        current_nail += 1
        if current_nail == num_nails:
            pen.color(string_options["string_color"])
            pen.pensize(string_options["string_thickness"])
            pen.penup()
            pen.goto(nails[-1])
            pen.pendown()
            pen.goto(nails[0])
            pen.penup()
            pen.color(nail_color)
    else:
        messagebox.showinfo("Limit Reached", "You have placed all nails.")


def open_chat_window(game_session_id, game_root, timer_label):
    global chat_window
    chat_window = ctk.CTkToplevel()
    chat_window.title("Guess the Drawing")
    chat_window.geometry("400x400")

    chat_frame = ctk.CTkFrame(chat_window)
    chat_frame.pack(expand=True, fill="both", padx=10, pady=10)

    timer_hint_frame = ctk.CTkFrame(chat_frame)
    timer_hint_frame.pack(fill="x", padx=5, pady=5)

    chat_timer_label = ctk.CTkLabel(
        timer_hint_frame, text="Time left: 120", font=("Monaco", 14)
    )
    chat_timer_label.pack(side="left", padx=5)

    messages_text = tk.Text(chat_frame, state="disabled", wrap="word", height=10)
    messages_text.pack(expand=True, fill="both")

    input_frame = ctk.CTkFrame(chat_window)
    input_frame.pack(fill="x", padx=10, pady=5)

    guess_var = tk.StringVar()
    guess_entry = ctk.CTkEntry(input_frame, textvariable=guess_var)
    guess_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    send_button = ctk.CTkButton(
        input_frame, text="Send to AI", command=lambda: send_to_ai(prompt)
    )

    send_button.pack(side="left", padx=10)

    def send_guess(guess):
        guess = guess.strip()
        if guess:
            game_session_ref = db.reference(f"games/{game_session_id}")
            game_data = game_session_ref.get()
            prompt = game_data.get("prompt", "").lower()
            correct = guess.lower() == prompt.lower()
            guess_attempts = game_data.get("guess_attempts", 0) + 1

            guesses_ref = game_session_ref.child("guesses")
            new_guess = {"guess": guess, "correct": correct}
            guesses_ref.push(new_guess)

            if correct:
                game_session_ref.update(
                    {
                        "state": "ended",
                        "game_result": "Guesser Won",
                        "guess_time": time.time(),
                        "guess_attempts": guess_attempts,
                    }
                )
                messages_text.config(state="normal")
                messages_text.insert("end", f"You: {guess}\n")
                messages_text.insert("end", "Correct! You've guessed the drawing.\n")
                messages_text.config(state="disabled")

                close_all_windows()
                chat_window.after(
                    0, lambda: show_stats_and_exit(game_session_id, "guesser")
                )
            else:
                game_session_ref.update({"guess_attempts": guess_attempts})
                messages_text.config(state="normal")
                messages_text.insert("end", f"You: {guess}\n")
                messages_text.insert("end", "Incorrect guess. Try again.\n")
                messages_text.config(state="disabled")
                guess_var.set("")

    def update_chat():
        global last_hint_index
        game_session_ref = db.reference(f"games/{game_session_id}")
        game_data = game_session_ref.get()
        if not game_data:
            return

        elapsed_time = int(
            time.time() - game_data.get("drawing_started_at", time.time())
        )
        time_left = max(0, 120 - elapsed_time)
        chat_timer_label.configure(text=f"Time left: {time_left}s")

        if game_data.get("state") == "ended":

            close_all_windows()
            chat_window.after(
                0, lambda: show_stats_and_exit(game_session_id, "guesser")
            )
            return
        else:
            chat_window.after(1000, update_chat)

    update_chat()
    open_hints_window(game_session_id)


def open_hints_window(game_session_id):
    global hints_window
    hints_window = ctk.CTkToplevel()
    hints_window.title("Hints")
    hints_window.geometry("300x200")
    hints_frame = ctk.CTkFrame(hints_window)
    hints_frame.pack(expand=True, fill="both", padx=10, pady=10)
    hints_text = tk.Text(hints_frame, state="disabled", wrap="word", height=10)
    hints_text.pack(expand=True, fill="both")
    last_hint_index = None

    def update_hints():
        nonlocal last_hint_index
        game_session_ref = db.reference(f"games/{game_session_id}")
        hints = game_session_ref.child("hints").get()
        if hints:
            hints_list = sorted(hints.items(), key=lambda x: x[0])
            for index, hint_data in enumerate(hints_list):
                if last_hint_index is None or index > last_hint_index:
                    hint_message = hint_data[1]["message"]
                    hints_text.config(state="normal")
                    hints_text.insert("end", f"{hint_message}\n")
                    hints_text.config(state="disabled")
                    last_hint_index = index
        game_data = game_session_ref.get()
        if game_data.get("state") == "ended":
            hints_window.destroy()
        else:
            hints_window.after(1000, update_hints)

    update_hints()


def open_chat_window_drawer(game_session_id):
    global chat_window
    chat_window = ctk.CTkToplevel()
    chat_window.title("Guesser's Attempts")
    chat_window.geometry("400x300")
    chat_frame = ctk.CTkFrame(chat_window)
    chat_frame.pack(expand=True, fill="both", padx=10, pady=10)
    messages_text = tk.Text(chat_frame, state="disabled", wrap="word")
    messages_text.pack(expand=True, fill="both")
    last_displayed_guess = None

    def receive_guesses():
        nonlocal last_displayed_guess
        game_session_ref = db.reference(f"games/{game_session_id}")
        game_data = game_session_ref.get()
        guesses = game_data.get("guesses", {})
        sorted_guesses = sorted(guesses.items(), key=lambda item: item[0])
        for key, guess_data in sorted_guesses:
            if last_displayed_guess is None or key > last_displayed_guess:
                guess_text = guess_data["guess"]
                correct = guess_data["correct"]
                messages_text.config(state="normal")
                messages_text.insert("end", f"Guesser guessed: {guess_text}\n")
                messages_text.config(state="disabled")
                last_displayed_guess = key
        if game_data.get("state") == "ended":

            close_all_windows()
            chat_window.after(0, lambda: show_stats_and_exit(game_session_id, "drawer"))
        else:
            chat_window.after(1000, receive_guesses)

    receive_guesses()


def ask_for_nails():
    global num_nails
    while True:
        try:
            num_nails_input = ctk.CTkInputDialog(
                text="How many nails do you want to use?", title="Nail Count"
            ).get_input()
            num_nails = int(num_nails_input)
            if num_nails > 0:
                break
            else:
                messagebox.showerror(
                    "Invalid Input", "Please enter a positive integer."
                )
        except (ValueError, TypeError):
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
    return num_nails


def draw_string_art():
    global pen, nails
    pen.color(string_options["string_color"])
    for x, y in nails:
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.dot(nail_options["nail_size"], nail_options["nail_color"])
    for i in range(len(nails)):
        x1, y1 = nails[i]
        x2, y2 = nails[(i + 1) % len(nails)]
        pen.penup()
        pen.goto(x1, y1)
        pen.pendown()
        pen.pensize(string_options["string_thickness"])
        pen.goto(x2, y2)
    global current_nail
    current_nail = 0


def draw_string_art_custom(nails_list):
    pen.clear()
    pen.color(string_options["string_color"])
    for x, y in nails_list:
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.dot(nail_options["nail_size"], nail_options["nail_color"])
    for i in range(len(nails_list)):
        x1, y1 = nails_list[i]
        x2, y2 = nails_list[(i + 1) % len(nails_list)]
        pen.penup()
        pen.goto(x1, y1)
        pen.pendown()
        pen.pensize(string_options["string_thickness"])
        pen.goto(x2, y2)


def open_free_draw_mode():
    global pen, screen, nails, current_nail, num_nails, game_root_single
    reset_game_variables_single()
    if not screen or not screen._root:
        screen = turtle.Screen()
    else:
        try:
            screen.reset()
        except turtle.Terminator:
            screen = turtle.Screen()
    screen.setup(
        width=int(settings["resolution"].split("x")[0]),
        height=int(settings["resolution"].split("x")[1]),
    )
    screen.bgcolor(settings["background"])
    screen.title("Digital String Art - Free Draw Mode")
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    game_root_single = ctk.CTk()
    game_root_single.title("Digital String Art - Free Draw Mode")
    window_width, window_height = map(int, settings["resolution"].split("x"))
    game_root_single.geometry(f"{window_width}x200")
    taskbar_frame = ctk.CTkFrame(game_root_single, corner_radius=10)
    taskbar_frame.pack(fill="both", padx=20, pady=10)
    ctk.CTkLabel(taskbar_frame, text="Nail Size:", font=("Monaco", 12)).grid(
        row=0, column=0, padx=5, pady=5
    )
    nail_size_var = tk.IntVar(value=nail_options["nail_size"])
    nail_size_entry = ctk.CTkEntry(taskbar_frame, textvariable=nail_size_var, width=50)
    nail_size_entry.grid(row=0, column=1, padx=5, pady=5)

    def choose_nail_color():
        color_code = colorchooser.askcolor(title="Choose Nail Color")
        if color_code:
            nail_options["nail_color"] = color_code[1]

    nail_color_button = ctk.CTkButton(
        taskbar_frame, text="Nail Color", command=choose_nail_color
    )
    nail_color_button.grid(row=0, column=2, padx=5, pady=5)
    ctk.CTkLabel(taskbar_frame, text="String Thickness:", font=("Monaco", 12)).grid(
        row=1, column=0, padx=5, pady=5
    )
    string_thickness_var = tk.IntVar(value=string_options["string_thickness"])
    string_thickness_entry = ctk.CTkEntry(
        taskbar_frame, textvariable=string_thickness_var, width=50
    )
    string_thickness_entry.grid(row=1, column=1, padx=5, pady=5)

    def choose_string_color():
        color_code = colorchooser.askcolor(title="Choose String Color")
        if color_code:
            string_options["string_color"] = color_code[1]

    string_color_button = ctk.CTkButton(
        taskbar_frame, text="String Color", command=choose_string_color
    )
    string_color_button.grid(row=1, column=2, padx=5, pady=5)
    reset_button = ctk.CTkButton(
        taskbar_frame,
        text="Reset Canvas",
        command=lambda: reset_canvas_free_draw(cost_label),
    )
    reset_button.grid(row=0, column=3, padx=5, pady=5)

    def export_canvas():
        canvas = screen.getcanvas()
        canvas.postscript(file="string_art.eps")
        messagebox.showinfo(
            "Export Successful", "Your art has been exported as 'string_art.eps'."
        )

    export_button = ctk.CTkButton(
        taskbar_frame, text="Export Canvas", command=export_canvas
    )
    export_button.grid(row=1, column=3, padx=5, pady=5)

    cost_label = ctk.CTkLabel(
        taskbar_frame, text="Total Cost: $0.00", font=("Monaco", 14)
    )
    cost_label.grid(row=0, column=4, rowspan=2, padx=10, pady=5)

    reset_button = ctk.CTkButton(
        taskbar_frame,
        text="Clear Canvas",
        command=lambda: reset_canvas_free_draw(cost_label),
    )
    reset_button.grid(row=0, column=3, padx=5, pady=5)
    exit_button = ctk.CTkButton(
        taskbar_frame,
        text="Exit to Main Menu",
        command=lambda: [reset_game_variables_single(), splash_screen()],
    )
    exit_button.grid(row=0, column=5, rowspan=2, padx=10, pady=5)
    ask_for_nails_free_draw()

    def update_options():
        try:
            nail_options["nail_size"] = int(nail_size_var.get())
        except ValueError:
            nail_options["nail_size"] = 10
        try:
            string_options["string_thickness"] = int(string_thickness_var.get())
        except ValueError:
            string_options["string_thickness"] = 2
        game_root_single.after(500, update_options)

    update_options()
    screen.onscreenclick(lambda x, y: place_nail_free_draw(x, y, cost_label))
    game_root_single.mainloop()


def ask_for_nails_free_draw():
    global num_nails
    while True:
        try:
            num_nails_input = ctk.CTkInputDialog(
                text="How many nails do you want to use?", title="Nail Count"
            ).get_input()
            num_nails = int(num_nails_input)
            if num_nails > 0:
                break
            else:
                messagebox.showerror(
                    "Invalid Input", "Please enter a positive integer."
                )
        except (ValueError, TypeError):
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
    return num_nails


def place_nail_free_draw(x, y, cost_label):
    global nails, current_nail, num_nails, pen
    if current_nail < num_nails:
        nail_color = nail_options["nail_color"]
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.dot(nail_options["nail_size"], nail_color)
        if nails:
            pen.color(string_options["string_color"])
            pen.pensize(string_options["string_thickness"])
            pen.penup()
            pen.goto(nails[-1])
            pen.pendown()
            pen.goto(x, y)
            pen.penup()
            pen.color(nail_color)
        nails.append((x, y))
        current_nail += 1
        if current_nail == num_nails:
            pen.color(string_options["string_color"])
            pen.pensize(string_options["string_thickness"])
            pen.penup()
            pen.goto(nails[-1])
            pen.pendown()
            pen.goto(nails[0])
            pen.penup()
            pen.color(nail_color)
            if cost_label:
                total_cost = calculate_cost()
                cost_label.configure(text=f"Total Cost: ${total_cost:.2f}")
    else:
        messagebox.showinfo("Limit Reached", "You have placed all nails.")


def calculate_cost():
    global nails
    board_cost = 5.00
    nails_cost = len(nails) * 0.12
    total_length = 0
    for i in range(len(nails)):
        x1, y1 = nails[i]
        x2, y2 = nails[(i + 1) % len(nails)]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        total_length += distance
    string_cost = (total_length / 32) * 0.07
    total_cost = board_cost + nails_cost + string_cost
    return total_cost


def reset_canvas_free_draw(cost_label):
    global pen, nails, current_nail, screen
    pen.clear()
    nails = []
    current_nail = 0
    if cost_label:
        cost_label.configure(text="Total Cost: $0.00")
    ask_for_nails_free_draw()


def open_settings():
    settings_window = ctk.CTkToplevel()
    settings_window.title("Settings")
    resolution_var = tk.StringVar(value=settings["resolution"])
    ctk.CTkLabel(settings_window, text="Resolution:", font=("Monaco", 12)).pack(pady=5)
    resolution_options = [
        "800x600",
        "1024x768",
        "1280x720",
        "1366x768",
        "1600x900",
        "1920x1080",
    ]
    ctk.CTkOptionMenu(
        settings_window, variable=resolution_var, values=resolution_options
    ).pack(pady=5)
    ctk.CTkLabel(settings_window, text="Background Color:", font=("Monaco", 12)).pack(
        pady=5
    )

    def choose_bg_color():
        color_code = colorchooser.askcolor(title="Choose Background Color")
        if color_code:
            settings["background"] = color_code[1]

    bg_color_button = ctk.CTkButton(
        settings_window, text="Choose Color", command=choose_bg_color
    )
    bg_color_button.pack(pady=5)
    audio_var = tk.BooleanVar(value=settings["audio"])
    ctk.CTkLabel(settings_window, text="Enable Audio", font=("Monaco", 12)).pack(pady=5)
    ctk.CTkSwitch(settings_window, text="Audio", variable=audio_var).pack(pady=5)

    def save_settings():
        settings["resolution"] = resolution_var.get()
        settings["audio"] = audio_var.get()
        settings_window.destroy()
        messagebox.showinfo("Settings Saved", "Your settings have been updated.")

    ctk.CTkButton(settings_window, text="Save", command=save_settings).pack(pady=10)


def open_info():

    info_window = ThemedTk(theme="radiance")
    info_window.title("Digital String Art Platform - Info")
    info_window.geometry("600x725")

    main_frame = ttk.Frame(info_window, padding=10)
    main_frame.pack(fill="both", expand=True)

    title_label = ttk.Label(
        main_frame,
        text="Digital String Art Platform v1.0",
        font=("Helvetica", 22, "bold"),
        foreground="#007BFF",
    )
    title_label.pack(pady=10)

    about_label = ttk.Label(
        main_frame,
        text=(
            "Welcome to Digital String Art Platform v1.0, the place where art meets technology! "
            "This app allows you to create interactive string art using customizable tools "
            "and play with friends in different game modes. Developed by Yair K., "
            "this app is designed to be fun, competitive, and collaborative."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    about_label.pack(pady=5)

    game_modes_title = ttk.Label(
        main_frame,
        text="Game Modes",
        font=("Helvetica", 16, "bold"),
        foreground="#FF6347",
    )
    game_modes_title.pack(pady=10)

    game_modes_label = ttk.Label(
        main_frame,
        text=(
            "- Free Draw Mode: Unleash your creativity with a freeform drawing experience.\n"
            "- Multiplayer Mode: Compete with friends online in a guessing game.\n"
            "- Vs AI Mode: Play against our AI to test your skills."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    game_modes_label.pack(pady=5)

    features_title = ttk.Label(
        main_frame,
        text="Features",
        font=("Helvetica", 16, "bold"),
        foreground="#28A745",
    )
    features_title.pack(pady=10)

    features_label = ttk.Label(
        main_frame,
        text=(
            "- Customizable nail and string settings (color, size, thickness).\n"
            "- Export your creations as high-quality images.\n"
            "- Real-time multiplayer with chat and synchronization."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    features_label.pack(pady=5)

    tech_stack_title = ttk.Label(
        main_frame,
        text="Tech Stack",
        font=("Helvetica", 16, "bold"),
        foreground="#FFC107",
    )
    tech_stack_title.pack(pady=10)

    tech_stack_label = ttk.Label(
        main_frame,
        text=(
            "- Python for core functionality.\n"
            "- Turtle Graphics for rendering.\n"
            "- CustomTkinter for sleek UI.\n"
            "- GPT-4o for clever AI Recognition\n"
            "- Google Firebase Database for real-time multiplayer support."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    tech_stack_label.pack(pady=5)

    history_title = ttk.Label(
        main_frame,
        text="History & Development",
        font=("Helvetica", 16, "bold"),
        foreground="#6C757D",
    )
    history_title.pack(pady=10)

    history_label = ttk.Label(
        main_frame,
        text=(
            "The DSAP was created by Yair as an extention to his 1P13A Project. "
            "He got tired from being tired from studying for his midterms so he decided to make studying even harder by taking on this project."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    history_label.pack(pady=5)

    def callback(event):
        webbrowser.open_new(r"https://yair.ca")

    website_label = ttk.Label(
        main_frame,
        text="Feel free to visit my Portfolio @ https://yair.ca",
        font=("Helvetica", 14, "bold"),
        foreground="blue",
        cursor="hand2",
    )
    website_label.pack(pady=10)
    website_label.bind("<Button-1>", callback)

    close_button = ttk.Button(info_window, text="Close", command=info_window.destroy)
    close_button.pack(pady=20)

    info_window.mainloop()

    info_window = ThemedTk(theme="radiance")
    info_window.title("Digital String Art Platform - Info")
    info_window.geometry("600x700")

    main_frame = ttk.Frame(info_window, padding=10)
    main_frame.pack(fill="both", expand=True)

    title_label = ttk.Label(
        main_frame,
        text="Digital String Art Platform v1.0",
        font=("Helvetica", 22, "bold"),
        foreground="#007BFF",
    )
    title_label.pack(pady=10)

    about_label = ttk.Label(
        main_frame,
        text=(
            "Welcome to Digital String Art v1.0, the platform where art meets technology! "
            "This app allows you to create interactive string art using customizable tools "
            "and play with friends in different game modes. Developed by Yair K., "
            "this app is designed to be fun, competitive, and collaborative."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    about_label.pack(pady=5)

    game_modes_title = ttk.Label(
        main_frame,
        text="Game Modes",
        font=("Helvetica", 16, "bold"),
        foreground="#FF6347",
    )
    game_modes_title.pack(pady=10)

    game_modes_label = ttk.Label(
        main_frame,
        text=(
            "- Free Draw Mode: Unleash your creativity with a freeform drawing experience.\n"
            "- Multiplayer Mode: Compete with friends in a guessing game.\n"
            "- Vs AI Mode (Coming Soon): Play against our AI to test your skills."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    game_modes_label.pack(pady=5)

    features_title = ttk.Label(
        main_frame,
        text="Features",
        font=("Helvetica", 16, "bold"),
        foreground="#28A745",
    )
    features_title.pack(pady=10)

    features_label = ttk.Label(
        main_frame,
        text=(
            "- Customizable nail and string settings (color, size, thickness).\n"
            "- Export your creations as high-quality images.\n"
            "- Real-time multiplayer with chat and synchronization."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    features_label.pack(pady=5)

    tech_stack_title = ttk.Label(
        main_frame,
        text="Tech Stack",
        font=("Helvetica", 16, "bold"),
        foreground="#FFC107",
    )
    tech_stack_title.pack(pady=10)

    tech_stack_label = ttk.Label(
        main_frame,
        text=(
            "- Python for core functionality.\n"
            "- Turtle Graphics for rendering.\n"
            "- CustomTkinter for sleek UI.\n"
            "- Firebase for real-time multiplayer."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    tech_stack_label.pack(pady=5)

    history_title = ttk.Label(
        main_frame,
        text="History & Development",
        font=("Helvetica", 16, "bold"),
        foreground="#6C757D",
    )
    history_title.pack(pady=10)

    history_label = ttk.Label(
        main_frame,
        text=(
            "The Digital String Art Platform was created by Yair K.. "
            "It has since evolved into a more collaborative experience."
        ),
        font=("Helvetica", 12),
        wraplength=580,
        justify="left",
    )
    history_label.pack(pady=5)

    def callback(event):
        webbrowser.open_new(r"https://yair.ca")

    website_label = ttk.Label(
        main_frame,
        text="Visit my website: yair.ca",
        font=("Helvetica", 14, "bold"),
        foreground="blue",
        cursor="hand2",
    )
    website_label.pack(pady=10)
    website_label.bind("<Button-1>", callback)

    close_button = ttk.Button(info_window, text="Close", command=info_window.destroy)
    close_button.pack(pady=20)

    info_window.mainloop()


def reset_game_variables():
    global nails, current_nail, num_nails, drawing_started_at, is_editing
    global pen, screen, game_root_single, game_root_multi, waiting_screen, chat_window, hints_window, game_ended
    nails = []
    current_nail = 0
    num_nails = 0
    drawing_started_at = None
    is_editing = False
    game_ended = False
    if pen:
        try:
            pen.clear()
            pen.reset()
            pen.hideturtle()
        except (turtle.Terminator, tk.TclError):
            pass
        pen = None
    if screen:
        try:
            screen.clear()
            screen.bye()
            screen = None
        except (turtle.Terminator, tk.TclError):
            screen = None
    if game_root_single:
        try:
            if game_root_single.winfo_exists():
                game_root_single.destroy()
        except tk.TclError:
            pass
        game_root_single = None
    if game_root_multi:
        try:
            if game_root_multi.winfo_exists():
                game_root_multi.destroy()
        except tk.TclError:
            pass
        game_root_multi = None
    if waiting_screen:
        try:
            if waiting_screen.winfo_exists():
                waiting_screen.destroy()
        except tk.TclError:
            pass
        waiting_screen = None
    if chat_window:
        try:
            if chat_window.winfo_exists():
                chat_window.destroy()
        except tk.TclError:
            pass
        chat_window = None
    if hints_window:
        try:
            if hints_window.winfo_exists():
                hints_window.destroy()
        except tk.TclError:
            pass
        hints_window = None


def reset_game_variables_single():
    reset_game_variables()


def return_to_lobby():
    users_ref = db.reference("lobby/users")
    users_ref.child(user_id).delete()
    reset_game_variables()
    splash_screen()


def exit_game(game_session_id, is_multiplayer):
    if is_multiplayer:
        game_session_ref = db.reference(f"games/{game_session_id}")
        game_session_ref.update({"state": "ended"})
    reset_game_variables()
    splash_screen()


def show_stats_and_exit(game_session_id, player_role):
    global game_ended
    if game_ended:
        return
    game_ended = True
    game_session_ref = db.reference(f"games/{game_session_id}")
    game_data = game_session_ref.get()
    if not game_data:
        return_to_lobby()
        return
    result = game_data.get("game_result", "Unknown")
    guess_attempts = game_data.get("guess_attempts", 0)
    total_time = int(
        game_data.get("guess_time", time.time())
        - game_data.get("drawing_started_at", time.time())
    )

    stats_window = ctk.CTkToplevel()
    stats_window.title("Game Stats")
    stats_window.geometry("400x300")
    frame = ctk.CTkFrame(stats_window)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    if player_role == "guesser":
        message = f"Game Over!\nResult: {result}\nTotal Time: {total_time} seconds\nGuess Attempts: {guess_attempts}"
    else:
        message = f"Game Over!\nThe guesser has {result.lower()}.\nTotal Time: {total_time} seconds\nGuess Attempts: {guess_attempts}"
    ctk.CTkLabel(frame, text=message, font=("Monaco", 16), wraplength=360).pack(pady=20)
    ctk.CTkButton(
        frame,
        text="Return to Lobby",
        command=lambda: [stats_window.destroy(), return_to_lobby()],
    ).pack(pady=10)


def close_all_windows():
    global game_root_single, game_root_multi, chat_window, hints_window

    windows_to_destroy = [game_root_single, game_root_multi, chat_window, hints_window]
    for window in windows_to_destroy:
        try:
            if window and window.winfo_exists():
                window.destroy()
        except tk.TclError:
            pass

    if screen:
        try:
            screen.bye()
        except turtle.Terminator:
            pass


splash_screen()
