import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import os

FAV_FILE = 'favorites.json'

def load_favorites():
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, 'r') as f:
            return json.load(f)
    return []

def save_favorites(favorites):
    with open(FAV_FILE, 'w') as f:
        json.dump(favorites, f, indent=4)

# Основное окно
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("700x500")

favorites = load_favorites()

# Поле для ввода
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Введите имя пользователя GitHub:").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(search_frame, width=30)
entry_search.pack(side=tk.LEFT, padx=5)

# Результаты поиска
results_frame = tk.Frame(root)
results_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(results_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(results_frame, yscrollcommand=scrollbar.set)
listbox.pack(fill=tk.BOTH, expand=True)

scrollbar.config(command=listbox.yview)

def search_user():
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Внимание", "Поле поиска не должно быть пустым.")
        return
    url = f"https://api.github.com/users/{username}"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 404:
                messagebox.showerror("Не найдено", "Пользователь не найден.")
                return
            data_bytes = response.read()
            data_str = data_bytes.decode('utf-8')
            data = json.loads(data_str)
            display_results([data])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            messagebox.showerror("Не найдено", "Пользователь не найден.")
        else:
            messagebox.showerror("Ошибка", f"Ошибка HTTP: {e.code}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def display_results(users):
    listbox.delete(0, tk.END)
    for user in users:
        listbox.insert(tk.END, user['login'])

def add_to_favorites():
    selection = listbox.curselection()
    if not selection:
        messagebox.showinfo("Внимание", "Выберите пользователя.")
        return
    username = listbox.get(selection)
    if username in favorites:
        messagebox.showinfo("Информация", "Пользователь уже в избранных.")
        return
    favorites.append(username)
    save_favorites(favorites)
    messagebox.showinfo("Готово", f"{username} добавлен в избранное.")

def show_favorites():
    if not favorites:
        messagebox.showinfo("Избранное", "Нет избранных пользователей.")
    else:
        messagebox.showinfo("Избранное", "\n".join(favorites))

btn_search = tk.Button(search_frame, text="Поиск", command=search_user)
btn_search.pack(side=tk.LEFT, padx=5)

btn_add = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_add.pack(pady=5)

btn_show = tk.Button(root, text="Показать избранное", command=show_favorites)
btn_show.pack(pady=5)

root.mainloop()
