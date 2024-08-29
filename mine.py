import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from deep_translator import GoogleTranslator
from threading import Thread

def translate_text(text):
    """Перевод текста с английского на русский."""
    if text is None or not text.strip():
        return text
    
    try:
        translated = GoogleTranslator(source='en', target='ru').translate(text)
        return translated
    except Exception as e:
        print(f"Ошибка при переводе текста '{text}': {e}")
        return text

def translate_mod_file(file_path, output_folder, status_callback):
    """Перевод файла мода."""
    if not os.path.exists(file_path):
        status_callback("Файл не найден.")
        return
    
    status_callback("Чтение файла...")
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            mod_data = json.load(file)
        except json.JSONDecodeError as e:
            status_callback(f"Ошибка чтения JSON файла: {e}")
            return
    
    translated_mod_data = {}
    total_items = sum(1 for _ in mod_data.values() if isinstance(_, str))
    current_item = 0
    status_callback("Начало перевода...")
    for key, value in mod_data.items():
        if isinstance(value, str):
            translated_mod_data[key] = translate_text(value)
            current_item += 1
            status_callback(f"Переведено {current_item}/{total_items} строк.")
        elif isinstance(value, dict):
            translated_mod_data[key] = {k: translate_text(v) if isinstance(v, str) else v for k, v in value.items()}
        else:
            translated_mod_data[key] = value
    
    translated_file_path = os.path.join(output_folder, 'ru_ru.json')
    with open(translated_file_path, 'w', encoding='utf-8') as file:
        json.dump(translated_mod_data, file, ensure_ascii=False, indent=4)
    
    status_callback(f"Перевод завершен. Файл сохранен как {translated_file_path}")

class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Translator")
        self.geometry("600x400")
        self._configure_style()

        self.create_widgets()
        self.output_folder = ""

    def _configure_style(self):
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Модульный переводчик", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        self.file_path_entry = ctk.CTkEntry(self, width=450, placeholder_text="Выберите файл JSON...")
        self.file_path_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.browse_button = ctk.CTkButton(self, text="Выбрать файл", command=self.browse_file, width=120, height=30)
        self.browse_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.output_folder_entry = ctk.CTkEntry(self, width=450, placeholder_text="Выберите папку для сохранения...")
        self.output_folder_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.browse_output_folder_button = ctk.CTkButton(self, text="Выбрать папку", command=self.browse_output_folder, width=120, height=30)
        self.browse_output_folder_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.translate_button = ctk.CTkButton(self, text="Перевести", command=self.start_translation, width=120, height=30)
        self.translate_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.clear_button = ctk.CTkButton(self, text="Очистить", command=self.clear_all, width=120, height=30)
        self.clear_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.status_text = ctk.CTkTextbox(self, width=500, height=100, state=tk.DISABLED)
        self.status_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(4, weight=1)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, folder_path)
            self.output_folder = folder_path

    def start_translation(self):
        file_path = self.file_path_entry.get()
        output_folder = self.output_folder_entry.get()
        if not file_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл для перевода.")
            return
        if not output_folder:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите папку для сохранения.")
            return

        self.update_status("Запуск перевода...")
        translation_thread = Thread(target=self.perform_translation, args=(file_path, output_folder))
        translation_thread.start()

    def perform_translation(self, file_path, output_folder):
        def status_callback(message):
            self.update_status(message)

        translate_mod_file(file_path, output_folder, status_callback)

    def update_status(self, message):
        self.status_text.configure(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END) 
        self.status_text.configure(state=tk.DISABLED)

    def clear_all(self):
        """Очистка всех полей и статус текста"""
        self.file_path_entry.delete(0, tk.END)
        self.output_folder_entry.delete(0, tk.END)
        self.status_text.configure(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.configure(state=tk.DISABLED)

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
