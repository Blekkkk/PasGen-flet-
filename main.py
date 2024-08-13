import flet as ft
import random
import string
import json
import os

# Файл для хранения настроек
settings_file = "settings.json"

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            return json.load(file)
    return {"password_length": 16}  # Значение по умолчанию

def save_settings(settings):
    with open(settings_file, "w") as file:
        json.dump(settings, file)

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def main(page: ft.Page):
    page.title = "Password Generator"
    page.window_width = 400
    page.window_height = 400

    # Загрузка настроек
    settings = load_settings()
    initial_length = settings["password_length"]

    # Create a container for centering elements
    container = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    # Create a text label to display the selected password length
    length_label = ft.Text(value=f"Password Length: {initial_length}", size=20)

    # Set the initial value of the slider to the loaded length
    password_length = ft.Slider(min=16, max=64, value=initial_length, label="Password Length", on_change=lambda e: update_password())
    password_field = ft.TextField(label="Generated Password", read_only=True, width=300)

    def update_password():
        length = int(password_length.value)
        password = generate_password(length)
        password_field.value = password
        length_label.value = f"Password Length: {length}"  # Update the label with the current length
        page.update()

        # Сохранение настроек при изменении длины пароля
        settings["password_length"] = length
        save_settings(settings)

    def copy_to_clipboard(e):
        page.set_clipboard(password_field.value)
        page.snack_bar = ft.SnackBar(ft.Text("Password copied to clipboard!"))
        page.snack_bar.open = True
        page.update()

    generate_button = ft.ElevatedButton("Generate Password", on_click=lambda e: update_password())
    copy_button = ft.ElevatedButton("Copy to Clipboard", on_click=copy_to_clipboard)

    # Add elements to the container
    container.controls.extend([length_label, password_length, password_field, generate_button, copy_button])

    # Add the container to the page
    page.add(container)

    # Generate the initial password on startup
    update_password()

ft.app(target=main)
