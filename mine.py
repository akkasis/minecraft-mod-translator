import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from deep_translator import GoogleTranslator
from threading import Thread
import logging
from CTkToolTip import CTkToolTip

# Настройка логирования
handler = logging.FileHandler('translator_log.txt', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levellevel)s - %(message)s')
handler.setFormatter(formatter)

logging.basicConfig(handlers=[handler], level=logging.INFO)

def translate_text(text, target_lang="ru"):
    """Перевод текста с английского на указанный язык."""
    if text is None or not text.strip():
        return text

    try:
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        return translated
    except Exception as e:
        logging.error(f"Ошибка при переводе текста '{text}': {e}")
        return text

def translate_mod_file(file_path, output_folder, status_callback, update_progress, target_lang="ru"):
    """Перевод файла мода."""
    if not os.path.exists(file_path):
        status_callback("Файл не найден.")
        return

    status_callback("Чтение файла...")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            mod_data = json.load(file)
    except json.JSONDecodeError as e:
        status_callback(f"Ошибка чтения JSON файла: {e}")
        return

    translated_mod_data = {}
    saved_progress = 0
    progress_file = os.path.join(output_folder, 'progress.json')

    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            translated_mod_data = json.load(f)
            saved_progress = len(translated_mod_data)

    total_items = sum(1 for _ in mod_data.values() if isinstance(_, str))
    current_item = saved_progress
    status_callback("Начало перевода...")

    for key, value in list(mod_data.items())[saved_progress:]:
        if isinstance(value, str):
            translated_mod_data[key] = translate_text(value, target_lang)
            current_item += 1
            update_progress(current_item, total_items)
        elif isinstance(value, dict):
            translated_mod_data[key] = {k: translate_text(v, target_lang) if isinstance(v, str) else v for k, v in value.items()}
        elif isinstance(value, list):
            translated_mod_data[key] = [translate_text(v, target_lang) if isinstance(v, str) else v for v in value]
        else:
            translated_mod_data[key] = value

        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(translated_mod_data, f, ensure_ascii=False, indent=4)

    translated_file_path = os.path.join(output_folder, f'{target_lang}_{target_lang.upper()}.json')
    with open(translated_file_path, 'w', encoding='utf-8') as file:
        json.dump(translated_mod_data, file, ensure_ascii=False, indent=4)

    os.remove(progress_file)
    status_callback(f"Перевод завершен. Файл сохранен как {translated_file_path}")

class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Translator")
        self.geometry("650x500")
        self._configure_style()

        self.create_widgets()
        self.output_folder = ""
        self._cancel = False

    def _configure_style(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Модульный переводчик", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        self.file_path_entry = ctk.CTkEntry(self, width=400, placeholder_text="Выберите файл JSON...")
        self.file_path_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Добавление подсказки
        CTkToolTip(self.file_path_entry, message="Нажмите 'Выбрать файл', чтобы выбрать JSON файл для перевода.")

        self.browse_button = ctk.CTkButton(self, text="Выбрать файл", command=self.browse_file, width=120, height=30)
        self.browse_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        CTkToolTip(self.browse_button, message="Выберите JSON файл для перевода.")

        self.output_folder_entry = ctk.CTkEntry(self, width=400, placeholder_text="Выберите папку для сохранения...")
        self.output_folder_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        CTkToolTip(self.output_folder_entry, message="Нажмите 'Выбрать папку', чтобы выбрать место для сохранения переведенного файла.")

        self.browse_output_folder_button = ctk.CTkButton(self, text="Выбрать папку", command=self.browse_output_folder, width=120, height=30)
        self.browse_output_folder_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        CTkToolTip(self.browse_output_folder_button, message="Выберите папку для сохранения переведенного файла.")

        self.language_label = ctk.CTkLabel(self, text="Язык перевода:")
        self.language_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.language_option = ctk.CTkComboBox(self, values=["Русский", "Немецкий", "Французский", "Испанский"], width=200)
        self.language_option.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.language_option.set("Русский")
        self.language_option.bind("<<ComboboxSelected>>", self.update_output_file_name)
        CTkToolTip(self.language_option, message="Выберите язык, на который нужно перевести JSON файл.")

        self.translate_button = ctk.CTkButton(self, text="Перевести", command=self.start_translation, width=120, height=30)
        self.translate_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        CTkToolTip(self.translate_button, message="Запустить процесс перевода.")

        self.clear_button = ctk.CTkButton(self, text="Очистить", command=self.clear_all, width=120, height=30)
        self.clear_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        CTkToolTip(self.clear_button, message="Очистить все поля и сбросить настройки.")

        self.cancel_button = ctk.CTkButton(self, text="Отменить", command=self.cancel_translation, width=120, height=30)
        self.cancel_button.grid(row=4, column=2, padx=10, pady=10, sticky="ew")
        CTkToolTip(self.cancel_button, message="Отменить текущий процесс перевода.")

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        self.status_text = ctk.CTkTextbox(self, width=550, height=100, state=tk.DISABLED, wrap=tk.WORD)
        self.status_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(6, weight=1)

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

    def update_output_file_name(self, event=None):
        target_lang = self.get_target_language()
        self.update_status(f"Выходной файл будет сохранен как {target_lang}_{target_lang.upper()}.json")

    def start_translation(self):
        file_path = self.file_path_entry.get()
        output_folder = self.output_folder_entry.get()
        target_lang = self.get_target_language()

        if not file_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл для перевода.")
            return
        if not output_folder:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите папку для сохранения.")
            return

        self.update_status("Запуск перевода...")
        self.progress_bar.set(0)

        translation_thread = Thread(target=self.perform_translation, args=(file_path, output_folder, target_lang))
        translation_thread.start()

    def perform_translation(self, file_path, output_folder, target_lang):
        try:
            translate_mod_file(file_path, output_folder, self.update_status, self.update_progress, target_lang)
        except Exception as e:
            self.update_status(f"Ошибка: {e}")
        finally:
            self._cancel = False

    def update_status(self, message):
        self.status_text.configure(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.configure(state=tk.DISABLED)
        logging.info(message)

    def update_progress(self, current, total):
        self.progress_bar.set(current / total)
        self.update_status(f"Прогресс: {current}/{total}")

    def clear_all(self):
        self.file_path_entry.delete(0, tk.END)
        self.output_folder_entry.delete(0, tk.END)
        self.language_option.set("Русский")
        self.progress_bar.set(0)
        self.status_text.configure(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.configure(state=tk.DISABLED)

    def cancel_translation(self):
        """Устанавливает флаг отмены."""
        self._cancel = True

    def get_target_language(self):
        lang = self.language_option.get()
        if lang == "Русский":
            return "ru"
        elif lang == "Немецкий":
            return "de"
        elif lang == "Французский":
            return "fr"
        elif lang == "Испанский":
            return "es"
        else:
            return "ru"

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
