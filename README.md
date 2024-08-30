# Модульный переводчик JSON-файлов

[Присоединяйтесь к нашему сообществу в Telegram](https://t.me/transcend_space)

Это приложение на Python с графическим интерфейсом пользователя (GUI), созданное с использованием библиотек `tkinter` и `customtkinter`. Приложение предназначено для перевода текстовых данных из JSON-файлов с английского на русский и другие языки, используя API Google Translate.

## Оглавление
- [Модульный переводчик JSON-файлов](#модульный-переводчик-json-файлов)
  - [Оглавление](#оглавление)
  - [Установка](#установка)
  - [Использование](#использование)
  - [Зависимости](#зависимости)
  - [Архитектура кода](#архитектура-кода)
    - [Основные функции](#основные-функции)
    - [GUI приложение](#gui-приложение)
    - [Описание работы потоков](#описание-работы-потоков)
  - [Примеры](#примеры)

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/akkasis/minecraft-mod-translator.git
   cd minecraft-mod-translator
   ```

2. **Установите все необходимые зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

   **Зависимости**:
   - `tkinter` — стандартный модуль для создания GUI в Python.
   - `customtkinter` — модуль для улучшения внешнего вида стандартного `tkinter`.
   - `deep_translator` — библиотека для взаимодействия с API Google Translate.
   - `threading` — стандартный модуль для работы с потоками в Python.
   - `CTkToolTip` — модуль для добавления всплывающих подсказок в элементы интерфейса.

## Использование

1. Запустите приложение:
   ```bash
   python translator_app.py
   ```
2. В появившемся окне выберите JSON-файл, который вы хотите перевести.
3. Укажите папку, в которой будет сохранен переведенный файл.
4. Выберите язык перевода из доступных опций.
5. Нажмите кнопку "Перевести". После завершения перевода файл будет сохранен в выбранной папке с именем, соответствующим выбранному языку, например, `ru_RU.json`.

## Зависимости

Проект требует наличия следующих библиотек и модулей:

- `os` — работа с файловой системой.
- `json` — работа с JSON-файлами.
- `tkinter` — создание графических пользовательских интерфейсов.
- `customtkinter` — улучшение функциональности и стиля `tkinter`.
- `deep_translator` — перевод текста через API Google Translate.
- `threading` — реализация многопоточности.
- `CTkToolTip` — добавление всплывающих подсказок в элементы интерфейса.

Все необходимые зависимости указаны в `requirements.txt`.

## Архитектура кода

### Основные функции

- `translate_text(text, target_lang="ru")` — Переводит строку текста на указанный язык (по умолчанию — русский).
- `translate_mod_file(file_path, output_folder, status_callback, update_progress, target_lang="ru")` — Читает JSON-файл, переводит его содержимое и сохраняет переведенный файл в указанную папку, обновляя статус и прогресс.

### GUI приложение

- `TranslatorApp(ctk.CTk)` — Основной класс приложения, управляющий графическим интерфейсом и обработкой операций по переводу.

### Описание работы потоков

Перевод выполняется в отдельном потоке, чтобы избежать зависания интерфейса и обеспечить отзывчивость программы. В случае прерывания перевода можно сохранить прогресс и продолжить позже.

## Примеры

Исходный JSON-файл:
```json
{
    "name": "Sword",
    "description": "A sharp blade used in combat."
}
```

Переведенный файл:
```json
{
    "name": "Меч",
    "description": "Острый клинок, используемый в бою."
}
```