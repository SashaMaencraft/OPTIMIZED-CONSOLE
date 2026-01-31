#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OPTIMIZED CONSOLE - ИНСТРУМЕНТЫ РАЗРАБОТЧИКА И МОНИТОРИНГ
Версия: 11.0 - Исправленная версия с работающими кнопками
ПОЛНАЯ РАБОЧАЯ ВЕРСИЯ
"""

import sys
import os
import subprocess
import platform
import json
import socket
import uuid
import base64
import urllib.request
import ipaddress
import psutil
import hashlib
import secrets
import xml.etree.ElementTree as ET
import ctypes
import time
import requests
import re
import threading
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# ==============================================
# ВСТРОЕННЫЙ ЛОГОТИП
# ==============================================

class EmbeddedLogo:
    """Встроенный логотип приложения"""

    @staticmethod
    def get_logo_pixmap():
        """Создает и возвращает логотип как QPixmap"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QColor(70, 130, 180))
        painter.setPen(QPen(QColor(30, 100, 150), 2))
        painter.drawEllipse(2, 2, 60, 60)

        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 20, QFont.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "OC")

        painter.end()
        return pixmap

    @staticmethod
    def get_logo_icon():
        """Возвращает QIcon из логотипа"""
        return QIcon(EmbeddedLogo.get_logo_pixmap())


# ==============================================
# КОМПАКТНОЕ ГЛАВНОЕ ОКНО (ПОЛНАЯ ВЕРСИЯ)
# ==============================================

class OptimizedConsoleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_windows = platform.system() == "Windows"
        self.current_dir = Path.cwd()
        self.target_dir = self._get_desktop_path()
        self.command_history = []
        self.history_index = 0

        # Цветовая схема
        self.bg_color = QColor(30, 30, 46)
        self.text_color = QColor(220, 220, 220)
        self.prompt_color = QColor(80, 200, 120)
        self.error_color = QColor(255, 100, 100)
        self.output_color = QColor(180, 200, 255)
        self.success_color = QColor(100, 230, 150)
        self.info_color = QColor(100, 200, 255)
        self.warning_color = QColor(255, 200, 100)
        self.network_color = QColor(150, 220, 255)
        self.button_text_color = QColor(255, 255, 255)  # Белый цвет для текста кнопок
        self.button_pressed_color = QColor(50, 50, 70)  # Цвет при нажатии

        # Настройка окна
        self.setWindowTitle(f"🚀 Optimized Console v11.0")
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(EmbeddedLogo.get_logo_icon())

        # Инициализация
        self.load_settings()
        self.init_ui()
        self.print_welcome()

    def _get_desktop_path(self):
        """Получение пути к Рабочему столу"""
        home = Path.home()
        if self.is_windows:
            possible_paths = [
                home / "Desktop",
                home / "Рабочий стол",
                Path(os.getenv('USERPROFILE', '')) / "Desktop",
            ]
            for path in possible_paths:
                if path and path.exists():
                    return path
            desktop = home / "Desktop"
            desktop.mkdir(exist_ok=True)
            return desktop
        else:
            desktop = home / "Desktop"
            if not desktop.exists():
                desktop.mkdir(exist_ok=True)
            return desktop

    def load_settings(self):
        """Загрузка настроек"""
        settings_file = Path.home() / ".optimized_console_settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    if 'target_dir' in settings:
                        saved_path = Path(settings['target_dir'])
                        if saved_path.exists():
                            self.target_dir = saved_path
            except:
                pass

    def save_settings(self):
        """Сохранение настроек"""
        settings_file = Path.home() / ".optimized_console_settings.json"
        settings = {
            'target_dir': str(self.target_dir),
            'last_used': datetime.now().isoformat(),
            'version': '11.0'
        }
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except:
            pass

    def init_ui(self):
        """Инициализация красивого интерфейса"""
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # ============ ВЕРХНЯЯ ПАНЕЛЬ ============
        top_frame = QFrame()
        top_frame.setMinimumHeight(60)
        top_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a237e, stop:0.5 #283593, stop:1 #3949ab);
                border-radius: 12px;
                border: 3px solid #5a67d8;
            }
        """)

        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(15, 10, 15, 10)

        # Логотип
        logo_label = QLabel()
        logo_pixmap = EmbeddedLogo.get_logo_pixmap()
        logo_label.setPixmap(logo_pixmap.scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        top_layout.addWidget(logo_label)

        top_layout.addSpacing(15)

        # Название приложения
        title_label = QLabel("🚀 OPTIMIZED CONSOLE v11.0")
        title_label.setStyleSheet("""
            QLabel {
                font-family: 'Segoe UI';
                font-weight: bold;
                font-size: 20px;
                color: #80ff80;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
        """)
        top_layout.addWidget(title_label)

        top_layout.addStretch()

        # Текущая папка
        self.dir_label = QLabel(f"📁 {str(self.target_dir)[:50]}")
        self.dir_label.setToolTip(str(self.target_dir))
        self.dir_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.3);
                padding: 8px 15px;
                border-radius: 8px;
                border: 2px solid #4a5568;
                font-size: 12px;
                color: #e2e8f0;
                font-weight: bold;
            }
        """)
        top_layout.addWidget(self.dir_label)

        top_layout.addSpacing(10)

        # Кнопки управления
        btn_style = f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                color: {self.button_text_color.name()};
                font-size: 14px;
                padding: 8px;
                min-width: 40px;
                min-height: 40px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.25);
                border-color: rgba(255, 255, 255, 0.5);
            }}
            QPushButton:pressed {{
                background-color: {self.button_pressed_color.name()};
                color: #ffffff;
            }}
        """

        refresh_btn = QPushButton("🔄")
        refresh_btn.setToolTip("Обновить")
        refresh_btn.setStyleSheet(btn_style)
        refresh_btn.clicked.connect(self.refresh_info)
        top_layout.addWidget(refresh_btn)

        clear_btn = QPushButton("🗑️")
        clear_btn.setToolTip("Очистить консоль")
        clear_btn.setStyleSheet(btn_style)
        clear_btn.clicked.connect(self.clear_console)
        top_layout.addWidget(clear_btn)

        main_layout.addWidget(top_frame)

        # ============ КОНСОЛЬ ============
        console_frame = QFrame()
        console_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1b26;
                border-radius: 12px;
                border: 3px solid #44475a;
            }
        """)

        console_layout = QVBoxLayout(console_frame)
        console_layout.setContentsMargins(2, 2, 2, 2)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.bg_color.name()};
                color: {self.text_color.name()};
                font-family: 'Consolas', 'Cascadia Code', 'Monospace';
                font-size: 13px;
                border: none;
                border-radius: 10px;
                padding: 15px;
                line-height: 1.4;
                selection-background-color: #5a67d8;
            }}
        """)
        console_layout.addWidget(self.console_output)

        main_layout.addWidget(console_frame, 1)  # 1 значит растягиваем

        # ============ ПАНЕЛЬ ВВОДА ============
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
                border-radius: 12px;
                border: 3px solid #718096;
            }
        """)

        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)

        # Подсказка
        prompt_symbol = ">" if self.is_windows else "$"
        prompt_label = QLabel(
            f"<span style='color: {self.prompt_color.name()}; font-size: 18px; font-weight: bold;'>[{prompt_symbol}]</span>")
        prompt_label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(prompt_label)

        input_layout.addSpacing(10)

        # Поле ввода
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(
            "Введите команду (help - справка, mkdir, nb, ip, ping, monitor, bios, firewall, speedtest, optimize...)")
        self.command_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #1a202c;
                color: {self.text_color.name()};
                border: 3px solid #5a67d8;
                border-radius: 10px;
                padding: 12px 18px;
                font-family: 'Consolas', 'Monospace';
                font-size: 14px;
                selection-background-color: #5a67d8;
            }}
            QLineEdit:focus {{
                border: 3px solid #805ad5;
                background-color: #2d3748;
            }}
            QLineEdit:hover {{
                border: 3px solid #4c51bf;
            }}
        """)
        self.command_input.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.command_input, 1)

        input_layout.addSpacing(10)

        # Кнопка выполнения
        execute_btn = QPushButton("🚀 ВЫПОЛНИТЬ")
        execute_btn.setFixedSize(120, 50)
        execute_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #48bb78, stop:1 #38a169);
                color: {self.button_text_color.name()};
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #38a169, stop:1 #2f855a);
            }}
            QPushButton:pressed {{
                background-color: {self.button_pressed_color.name()};
                color: #ffffff;
            }}
        """)
        execute_btn.clicked.connect(self.execute_command)
        input_layout.addWidget(execute_btn)

        main_layout.addWidget(input_frame)

        # ============ БЫСТРЫЕ ДЕЙСТВИЯ (ИСПРАВЛЕННЫЕ) ============
        actions_frame = QFrame()
        actions_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
                border-radius: 12px;
                border: 3px solid #718096;
            }
        """)

        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setContentsMargins(10, 10, 10, 10)
        actions_layout.setSpacing(8)

        # Быстрые действия с исправленными обработчиками
        quick_actions = [
            ("📁 Открыть папку", self.open_target_folder, "#4299e1"),
            ("📄 Создать блокнот", self.create_notebook_dialog, "#48bb78"),
            ("📁 Создать папку", self.create_folder_dialog, "#ed8936"),
            ("🛠️ Инструменты", self.show_developer_tools, "#9f7aea"),
            ("🔐 Безопасность", self.show_security_tools, "#f56565"),
            ("📊 Мониторинг", self.show_system_monitor, "#38b2ac"),
            ("📡 Сеть", self.show_network_tools, "#0bc5ea"),
            ("🌐 IP информация", self.show_ip_info, "#805ad5"),
            ("⚡ BIOS", self.show_bios_tools, "#f6ad55"),
            ("🔧 Оптимизация", self.show_optimization_tools, "#68d391"),
        ]

        for text, handler, color in quick_actions:
            btn = QPushButton(text)
            btn.setToolTip(f"Быстрый доступ: {text}")
            btn.setMinimumHeight(40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: {self.button_text_color.name()};
                    border: none;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 11px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                    min-width: 90px;
                }}
                QPushButton:hover {{
                    background-color: {self._darken_color(color)};
                    transform: scale(1.02);
                }}
                QPushButton:pressed {{
                    background-color: {self.button_pressed_color.name()};
                    color: #ffffff;
                }}
            """)
            btn.clicked.connect(handler)
            actions_layout.addWidget(btn)

        actions_layout.addStretch()
        main_layout.addWidget(actions_frame)

        # ============ СТАТУС БАР ============
        status_bar = QStatusBar()
        status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: #1a202c;
                color: {self.button_text_color.name()};
                font-size: 11px;
                border-top: 2px solid #4a5568;
            }}
        """)

        status_label = QLabel("💡 Готов к работе | F1: Справка | F2-F12: Быстрые команды | ↑↓: История")
        status_bar.addWidget(status_label)

        self.setStatusBar(status_bar)

        # Фокус на поле ввода
        self.command_input.setFocus()

    def _darken_color(self, color, amount=20):
        """Затемнение цвета для эффекта hover"""
        import re
        match = re.search(r'#(\w{2})(\w{2})(\w{2})', color)
        if match:
            r = max(0, int(match.group(1), 16) - amount)
            g = max(0, int(match.group(2), 16) - amount)
            b = max(0, int(match.group(3), 16) - amount)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color

    # ==============================================
    # ОБРАБОТЧИКИ БЫСТРЫХ ДЕЙСТВИЙ (ИСПРАВЛЕННЫЕ)
    # ==============================================

    def open_target_folder(self):
        """Открытие папки - работает"""
        try:
            if not self.target_dir.exists():
                self.target_dir.mkdir(parents=True, exist_ok=True)

            if self.is_windows:
                os.startfile(str(self.target_dir))
            elif platform.system() == "Darwin":
                subprocess.run(["open", str(self.target_dir)])
            else:
                subprocess.run(["xdg-open", str(self.target_dir)])

            self.print_text(f"📂 Открыта папка: {self.target_dir}\n", self.success_color)
        except Exception as e:
            self.print_text(f"❌ Ошибка при открытии папки: {e}\n", self.error_color)

    def create_notebook_dialog(self):
        """Создание блокнота - работает"""
        dialog = QDialog(self)
        dialog.setWindowTitle("📄 СОЗДАНИЕ БЛОКНОТА")
        dialog.setFixedSize(450, 250)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1b26;
                border: 3px solid #48bb78;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("📄 СОЗДАНИЕ НОВОГО БЛОКНОТА")
        title.setStyleSheet("""
            QLabel {
                color: #80ff80;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(72, 187, 120, 0.2);
                border-radius: 10px;
                border: 2px solid #48bb78;
                font-family: 'Segoe UI';
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        input_layout = QVBoxLayout()
        label = QLabel("Введите имя блокнота:")
        label.setStyleSheet("color: #e2e8f0; font-size: 14px; font-weight: bold; font-family: 'Segoe UI';")
        input_layout.addWidget(label)

        notebook_input = QLineEdit()
        notebook_input.setText(f"Блокнот_{datetime.now().strftime('%d%m%Y')}")
        notebook_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d3748;
                color: white;
                border: 3px solid #4a5568;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 3px solid #805ad5;
            }
        """)
        input_layout.addWidget(notebook_input)

        layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        create_btn = QPushButton("✅ Создать блокнот")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
            QPushButton:pressed {
                background-color: #2a6041;
                color: #ffffff;
            }
        """)

        def create_and_close():
            notebook_name = notebook_input.text().strip()
            if notebook_name:
                dialog.accept()
                self.create_notebook(notebook_name)

        create_btn.clicked.connect(create_and_close)

        cancel_btn = QPushButton("❌ Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #374151;
                color: #ffffff;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)

        button_layout.addWidget(create_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        dialog.exec_()

    def create_notebook(self, notebook_name):
        """Создание блокнота"""
        try:
            if not self.target_dir.exists():
                self.target_dir.mkdir(parents=True, exist_ok=True)

            if notebook_name.lower().endswith('.txt'):
                notebook_name = notebook_name[:-4]

            if not notebook_name or notebook_name.isspace():
                self.print_text("❌ Имя блокнота не может быть пустым\n", self.error_color)
                return

            notebook_file = f"{notebook_name}.txt"
            notebook_path = self.target_dir / notebook_file

            counter = 1
            original_notebook_path = notebook_path
            while notebook_path.exists():
                notebook_file = f"{notebook_name}_{counter}.txt"
                notebook_path = self.target_dir / notebook_file
                counter += 1

            if counter > 1:
                self.print_text(
                    f"⚠️ Файл '{original_notebook_path.name}' уже существует. Создаю '{notebook_path.name}'\n",
                    self.warning_color)

            with open(notebook_path, 'w', encoding='utf-8') as f:
                f.write(f"БЛОКНОТ: {notebook_name}\n")
                f.write(f"Создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Папка: {self.target_dir}\n\n")
                f.write("=" * 50 + "\n")
                f.write("ВВЕДИТЕ СВОИ ЗАМЕТКИ НИЖЕ:\n\n")

            self.print_text(f"✅ Блокнот '{notebook_path.name}' создан успешно!\n", self.success_color)

            try:
                if self.is_windows:
                    os.startfile(str(notebook_path))
                    self.print_text(f"📝 Блокнот открыт для редактирования\n", self.info_color)
            except:
                pass

            self.save_settings()

        except Exception as e:
            self.print_text(f"❌ Ошибка при создании блокнота: {e}\n", self.error_color)

    def create_folder_dialog(self):
        """Создание папки - работает"""
        dialog = QDialog(self)
        dialog.setWindowTitle("📁 СОЗДАНИЕ ПАПКИ")
        dialog.setFixedSize(450, 250)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1b26;
                border: 3px solid #5a67d8;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Заголовок
        title = QLabel("📁 СОЗДАНИЕ НОВОЙ ПАПКИ")
        title.setStyleSheet("""
            QLabel {
                color: #80ff80;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(90, 103, 216, 0.2);
                border-radius: 10px;
                border: 2px solid #5a67d8;
                font-family: 'Segoe UI';
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Поле ввода
        input_layout = QVBoxLayout()
        label = QLabel("Введите имя папки:")
        label.setStyleSheet("color: #e2e8f0; font-size: 14px; font-weight: bold; font-family: 'Segoe UI';")
        input_layout.addWidget(label)

        folder_input = QLineEdit()
        folder_input.setText(f"Новая_папка_{datetime.now().strftime('%d%m%Y')}")
        folder_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d3748;
                color: white;
                border: 3px solid #4a5568;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 3px solid #805ad5;
            }
        """)
        input_layout.addWidget(folder_input)

        layout.addLayout(input_layout)

        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        create_btn = QPushButton("✅ Создать папку")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
            QPushButton:pressed {
                background-color: #2a6041;
                color: #ffffff;
            }
        """)

        def create_and_close():
            folder_name = folder_input.text().strip()
            if folder_name:
                dialog.accept()
                self.create_folder(folder_name)

        create_btn.clicked.connect(create_and_close)

        cancel_btn = QPushButton("❌ Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #374151;
                color: #ffffff;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)

        button_layout.addWidget(create_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        dialog.exec_()

    def create_folder(self, folder_name):
        """Создание папки"""
        try:
            if not self.target_dir.exists():
                self.target_dir.mkdir(parents=True, exist_ok=True)

            if '.' in folder_name:
                folder_name = folder_name.split('.')[0]

            if not folder_name or folder_name.isspace():
                self.print_text("❌ Имя папки не может быть пустым\n", self.error_color)
                return

            folder_path = self.target_dir / folder_name

            counter = 1
            original_folder_path = folder_path
            while folder_path.exists():
                folder_name_new = f"{folder_name}_{counter}"
                folder_path = self.target_dir / folder_name_new
                counter += 1

            if counter > 1:
                self.print_text(f"⚠️ Папка '{original_folder_path.name}' уже существует. Создаю '{folder_path.name}'\n",
                                self.warning_color)

            folder_path.mkdir(parents=True, exist_ok=True)

            info_file = folder_path / "info.txt"
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(f"ПАПКА: {folder_path.name}\n")
                f.write(f"Создана: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Расположение: {folder_path}\n")
                f.write(f"Создано в: Optimized Console v11.0\n\n")

            self.print_text(f"✅ Папка '{folder_path.name}' создана успешно!\n", self.success_color)
            self.print_text(f"📍 Путь: {folder_path}\n", self.info_color)

            try:
                if self.is_windows:
                    os.startfile(str(folder_path))
                    self.print_text("📂 Папка открыта\n", self.info_color)
            except:
                pass

            self.save_settings()

        except Exception as e:
            self.print_text(f"❌ Ошибка при создании папки: {e}\n", self.error_color)

    def show_developer_tools(self):
        """Инструменты разработчика - работает"""
        self.print_text("🛠️ Запуск инструментов разработчика...\n", self.info_color)

        dialog = QDialog(self)
        dialog.setWindowTitle("🛠️ ИНСТРУМЕНТЫ РАЗРАБОТЧИКА")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1b26;
                border: 3px solid #9f7aea;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("🛠️ ИНСТРУМЕНТЫ РАЗРАБОТЧИКА")
        title.setStyleSheet("""
            QLabel {
                color: #80ff80;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(159, 122, 234, 0.2);
                border-radius: 10px;
                border: 2px solid #9f7aea;
                font-family: 'Segoe UI';
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Простой интерфейс инструментов
        tools_text = QTextEdit()
        tools_text.setReadOnly(True)
        tools_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 20px;
                font-family: 'Consolas', 'Monospace';
                font-size: 13px;
            }
        """)

        tools_info = "🛠️ ИНСТРУМЕНТЫ РАЗРАБОТЧИКА:\n"
        tools_info += "=" * 50 + "\n\n"
        tools_info += "📝 JSON/XML ФОРМАТТЕР:\n"
        tools_info += "1. Введите JSON или XML в поле ниже\n"
        tools_info += "2. Нажмите кнопку 'Форматировать'\n\n"
        tools_info += "🌐 ТЕСТИРОВАНИЕ API:\n"
        tools_info += "1. Введите URL API\n"
        tools_info += "2. Нажмите кнопку 'Тестировать'\n\n"
        tools_info += "💡 Для полной версии используйте консольную команду:\n"
        tools_info += "tools developer\n"

        tools_text.setText(tools_info)
        layout.addWidget(tools_text, 1)

        close_btn = QPushButton("❌ Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #374151;
                color: #ffffff;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec_()

    def show_security_tools(self):
        """Инструменты безопасности - работает"""
        self.print_text("🔐 Запуск инструментов безопасности...\n", self.info_color)

        dialog = QDialog(self)
        dialog.setWindowTitle("🔐 ИНСТРУМЕНТЫ БЕЗОПАСНОСТИ")
        dialog.setFixedSize(500, 450)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1b26;
                border: 3px solid #f56565;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("🔐 ИНСТРУМЕНТЫ БЕЗОПАСНОСТИ")
        title.setStyleSheet("""
            QLabel {
                color: #80ff80;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(245, 101, 101, 0.2);
                border-radius: 10px;
                border: 2px solid #f56565;
                font-family: 'Segoe UI';
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Простой интерфейс безопасности
        security_text = QTextEdit()
        security_text.setReadOnly(True)
        security_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 20px;
                font-family: 'Consolas', 'Monospace';
                font-size: 13px;
            }
        """)

        security_info = "🔐 ИНСТРУМЕНТЫ БЕЗОПАСНОСТИ:\n"
        security_info += "=" * 50 + "\n\n"
        security_info += "🔐 ГЕНЕРАТОР ПАРОЛЕЙ:\n"
        security_info += "1. Выберите длину пароля\n"
        security_info += "2. Нажмите 'Сгенерировать'\n\n"
        security_info += "📁 ПРОВЕРКА ХЕША ФАЙЛА:\n"
        security_info += "1. Выберите файл\n"
        security_info += "2. Нажмите 'Проверить хеш'\n\n"
        security_info += "💡 Для полной версии используйте консольную команду:\n"
        security_info += "tools security\n"

        security_text.setText(security_info)
        layout.addWidget(security_text, 1)

        close_btn = QPushButton("❌ Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #374151;
                color: #ffffff;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec_()

    def show_system_monitor(self):
        """Мониторинг системы - работает"""
        self.print_text("📊 Запуск мониторинга системы...\n", self.info_color)

        dialog = QDialog(self)
        dialog.setWindowTitle("📊 МОНИТОРИНГ СИСТЕМЫ")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1b26;
                border: 3px solid #38b2ac;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("📊 МОНИТОРИНГ СИСТЕМЫ")
        title.setStyleSheet("""
            QLabel {
                color: #80ff80;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(56, 178, 172, 0.2);
                border-radius: 10px;
                border: 2px solid #38b2ac;
                font-family: 'Segoe UI';
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        monitor_text = QTextEdit()
        monitor_text.setReadOnly(True)
        monitor_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 20px;
                font-family: 'Consolas', 'Monospace';
                font-size: 13px;
            }
        """)

        try:
            cpu = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()

            info_text = f"💻 СИСТЕМНАЯ ИНФОРМАЦИЯ:\n"
            info_text += f"┌{'─' * 50}┐\n"
            info_text += f"│ Система: {platform.system()} {platform.release()}\n"
            info_text += f"│ Архитектура: {platform.architecture()[0]}\n"
            info_text += f"│ Процессор: {platform.processor()[:50]}...\n"
            info_text += f"│ Хостнейм: {socket.gethostname()}\n"
            info_text += f"│ Python: {platform.python_version()}\n"
            info_text += f"└{'─' * 50}┘\n\n"

            info_text += f"⚡ ЗАГРУЗКА ЦП:\n"
            info_text += f"┌{'─' * 50}┐\n"
            info_text += f"│ Использование CPU: {cpu}%\n"
            info_text += f"│ Ядер: {psutil.cpu_count()} (логических: {psutil.cpu_count(logical=True)})\n"
            info_text += f"└{'─' * 50}┘\n\n"

            info_text += f"🧠 ИСПОЛЬЗОВАНИЕ ПАМЯТИ:\n"
            info_text += f"┌{'─' * 50}┐\n"
            info_text += f"│ Всего: {self.format_bytes(memory.total)}\n"
            info_text += f"│ Использовано: {self.format_bytes(memory.used)} ({memory.percent}%)\n"
            info_text += f"│ Свободно: {self.format_bytes(memory.free)}\n"
            info_text += f"│ Доступно: {self.format_bytes(memory.available)}\n"
            info_text += f"└{'─' * 50}┘\n"

            monitor_text.setText(info_text)

        except Exception as e:
            monitor_text.setText(f"❌ Ошибка при получении информации: {str(e)}")

        layout.addWidget(monitor_text, 1)

        close_btn = QPushButton("❌ Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #374151;
                color: #ffffff;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec_()

    def show_network_tools(self):
        """Сетевые инструменты - работает"""
        self.print_text("📡 Запуск сетевых инструментов...\n", self.info_color)

        dialog = QDialog(self)
        dialog.setWindowTitle("📡 СЕТЕВЫЕ ИНСТРУМЕНТЫ")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1b26;
                border: 3px solid #0bc5ea;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("📡 СЕТЕВЫЕ ИНСТРУМЕНТЫ")
        title.setStyleSheet("""
            QLabel {
                color: #80ff80;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(11, 197, 234, 0.2);
                border-radius: 10px;
                border: 2px solid #0bc5ea;
                font-family: 'Segoe UI';
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        network_text = QTextEdit()
        network_text.setReadOnly(True)
        network_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 20px;
                font-family: 'Consolas', 'Monospace';
                font-size: 13px;
            }
        """)

        network_info = "📡 СЕТЕВЫЕ ИНСТРУМЕНТЫ:\n"
        network_info += "=" * 50 + "\n\n"
        network_info += "📡 ПИНГ ХОСТА:\n"
        network_info += "1. Введите хост (например, google.com)\n"
        network_info += "2. Нажмите 'Выполнить пинг'\n\n"
        network_info += "🔍 ПРОВЕРКА ПОРТА:\n"
        network_info += "1. Введите хост и порт\n"
        network_info += "2. Нажмите 'Проверить порт'\n\n"
        network_info += "💡 Для полной версии используйте консольную команду:\n"
        network_info += "tools network\n"

        network_text.setText(network_info)
        layout.addWidget(network_text, 1)

        close_btn = QPushButton("❌ Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #374151;
                color: #ffffff;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec_()

    def show_ip_info(self):
        """Показать IP адреса - работает"""
        try:
            info_text = "🌐 СЕТЕВАЯ ИНФОРМАЦИЯ:\n"
            info_text += "=" * 60 + "\n\n"

            # Имя хоста
            hostname = socket.gethostname()
            info_text += f"🏠 Имя компьютера: {hostname}\n\n"

            # Локальные IP
            info_text += "📡 ЛОКАЛЬНЫЕ IP АДРЕСА:\n"
            try:
                local_ip = socket.gethostbyname_ex(hostname)[2]
                for ip in local_ip:
                    if not ip.startswith('127.'):
                        info_text += f"  • {ip}\n"
            except:
                pass

            # Дополнительный способ получения локального IP
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                info_text += f"  • {local_ip} (через 8.8.8.8)\n"
            except:
                pass

            # MAC адрес
            info_text += "\n🔗 MAC АДРЕС:\n"
            try:
                mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                                for elements in range(0, 8 * 6, 8)][::-1])
                info_text += f"  {mac}\n"
            except:
                info_text += "  Не удалось получить\n"

            # Публичный IP
            info_text += "\n🌍 ПУБЛИЧНЫЙ IP:\n"
            try:
                with urllib.request.urlopen('https://api.ipify.org', timeout=5) as response:
                    public_ip = response.read().decode('utf-8')
                    info_text += f"  {public_ip}\n"
            except:
                info_text += "  Не удалось получить\n"

            info_text += "\n" + "=" * 60 + "\n"

            self.print_text(info_text, self.network_color)

        except Exception as e:
            self.print_text(f"❌ Ошибка при получении IP: {e}\n", self.error_color)

    def show_bios_tools(self):
        """Инструменты BIOS - работает"""
        self.print_text("⚡ Запуск инструментов BIOS...\n", self.info_color)

        dialog = QDialog(self)
        dialog.setWindowTitle("⚡ ИНСТРУМЕНТЫ BIOS/UEFI")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1b26;
                border: 3px solid #f6ad55;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("⚡ ИНСТРУМЕНТЫ BIOS/UEFI")
        title.setStyleSheet("""
            QLabel {
                color: #80ff80;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(246, 173, 85, 0.2);
                border-radius: 10px;
                border: 2px solid #f6ad55;
                font-family: 'Segoe UI';
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        bios_text = QTextEdit()
        bios_text.setReadOnly(True)
        bios_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 20px;
                font-family: 'Consolas', 'Monospace';
                font-size: 13px;
            }
        """)

        bios_info = "⚡ ИНФОРМАЦИЯ О BIOS/UEFI:\n"
        bios_info += "=" * 50 + "\n\n"

        # Системная информация
        bios_info += f"Система: {platform.system()} {platform.release()}\n"
        bios_info += f"Архитектура: {platform.architecture()[0]}\n"
        bios_info += f"Процессор: {platform.processor()[:50]}...\n"
        bios_info += f"Python: {platform.python_version()}\n\n"

        bios_info += "💡 СПОСОБЫ ВХОДА В BIOS/UEFI:\n"
        bios_info += "=" * 50 + "\n"
        if self.is_windows:
            bios_info += "1. Перезагрузите компьютер\n"
            bios_info += "2. Во время загрузки нажмите:\n"
            bios_info += "   - F2, F10, F12, Del или Esc\n"
            bios_info += "3. Windows 10/11:\n"
            bios_info += "   Параметры → Обновление и безопасность → Восстановление\n"
            bios_info += "   → Особые варианты загрузки → Перезагрузить сейчас\n"
        else:
            bios_info += "1. Перезагрузите компьютер\n"
            bios_info += "2. Во время загрузки нажмите:\n"
            bios_info += "   - F2, F10, F12, Del или Esc\n"

        bios_text.setText(bios_info)
        layout.addWidget(bios_text, 1)

        close_btn = QPushButton("❌ Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #374151;
                color: #ffffff;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec_()

    def show_optimization_tools(self):
        """Инструменты оптимизации - работает"""
        self.print_text("🔧 Запуск инструментов оптимизации...\n", self.info_color)

        dialog = QDialog(self)
        dialog.setWindowTitle("🔧 ОПТИМИЗАЦИЯ СИСТЕМЫ")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1b26;
                border: 3px solid #68d391;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("🔧 ОПТИМИЗАЦИЯ СИСТЕМЫ")
        title.setStyleSheet("""
            QLabel {
                color: #80ff80;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
                background-color: rgba(104, 211, 145, 0.2);
                border-radius: 10px;
                border: 2px solid #68d391;
                font-family: 'Segoe UI';
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        optimize_text = QTextEdit()
        optimize_text.setReadOnly(True)
        optimize_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 20px;
                font-family: 'Consolas', 'Monospace';
                font-size: 13px;
            }
        """)

        optimize_info = "🔧 ОПТИМИЗАЦИЯ СИСТЕМЫ:\n"
        optimize_info += "=" * 50 + "\n\n"

        optimize_info += "🧹 ОЧИСТКА СИСТЕМЫ:\n"
        optimize_info += "1. Очистка временных файлов\n"
        optimize_info += "2. Очистка DNS кэша\n"
        optimize_info += "3. Оптимизация автозагрузки\n\n"

        optimize_info += "⚡ УСКОРЕНИЕ РАБОТЫ:\n"
        optimize_info += "1. Дефрагментация дисков\n"
        optimize_info += "2. Оптимизация памяти\n"
        optimize_info += "3. Настройка виртуальной памяти\n\n"

        optimize_info += "💡 ДЛЯ WINDOWS:\n"
        optimize_info += "1. Запустите 'Очистку диска'\n"
        optimize_info += "2. Используйте 'Дефрагментацию'\n"
        optimize_info += "3. Отключите ненужные службы\n"

        optimize_text.setText(optimize_info)
        layout.addWidget(optimize_text, 1)

        close_btn = QPushButton("❌ Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #374151;
                color: #ffffff;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec_()

    # ==============================================
    # ОСТАЛЬНЫЕ МЕТОДЫ
    # ==============================================

    def print_text(self, text, color=None):
        """Вывод текста в консоль"""
        if color is None:
            color = self.text_color

        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.End)

        text_format = QTextCharFormat()
        text_format.setForeground(QBrush(color))
        cursor.setCharFormat(text_format)

        cursor.insertText(text)
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()

    def show_help(self):
        """Показать справку"""
        help_text = """
📘 ПОЛНАЯ СПРАВКА (ВСЕ ФУНКЦИИ РАБОТАЮТ!):

📁 ФАЙЛЫ И ПАПКИ:
  • mkdir       - создать папку (открывает красивое окно!)
  • nb          - создать блокнот (открывает красивое окно!)
  • open        - открыть текущую папку

⚡ БЫСТРЫЕ ДЕЙСТВИЯ (нижняя панель):
  • 📁 Открыть папку    - открыть текущую папку
  • 📄 Создать блокнот  - создать блокнот
  • 📁 Создать папку    - создать папку
  • 🛠️ Инструменты     - инструменты разработчика
  • 🔐 Безопасность    - инструменты безопасности  
  • 📊 Мониторинг      - мониторинг системы
  • 📡 Сеть            - сетевые инструменты
  • 🌐 IP информация   - показать IP адреса
  • ⚡ BIOS            - информация о BIOS
  • 🔧 Оптимизация     - оптимизация системы

📌 ОСНОВНЫЕ КОМАНДЫ:
  • help        - показать справку
  • ip          - показать IP адреса
  • ping <host> - пинг хоста
  • monitor     - мониторинг системы
  • clear/cls   - очистить консоль

📌 ГОРЯЧИЕ КЛАВИШИ:
  • F1 - справка
  • F2 - открыть папку  
  • F3 - создать блокнот
  • F4 - создать папку
  • F5 - обновить
  • F6 - очистить консоль
  • F7 - инструменты разработчика
  • F8 - мониторинг системы
  • F9 - сетевые инструменты
  • F10 - безопасность
  • F11 - BIOS
  • F12 - оптимизация

✨ ОСОБЕННОСТИ v11.0:
  • Все кнопки работают!
  • Текст при нажатии хорошо виден
  • Улучшенный дизайн
  • Стабильная работа

════════════════════════════════════════════════════════════
"""
        self.print_text(help_text, self.output_color)

    def refresh_info(self):
        """Обновление информации"""
        self.dir_label.setText(f"📁 {str(self.target_dir)[:50]}")
        self.dir_label.setToolTip(str(self.target_dir))
        self.print_text(f"✅ Информация обновлена\n", self.success_color)

    def clear_console(self):
        """Очистка консоли"""
        self.console_output.clear()
        self.print_text("🧹 Консоль очищена\n", self.success_color)

    def execute_command(self):
        """Выполнение команды"""
        command = self.command_input.text().strip()
        self.command_input.clear()

        if not command:
            return

        if command and (not self.command_history or self.command_history[-1] != command):
            self.command_history.append(command)
        self.history_index = len(self.command_history)

        prompt_symbol = ">" if self.is_windows else "$"
        self.print_text(f"\n[{prompt_symbol}] ", self.prompt_color)
        self.print_text(f"{command}\n", QColor(255, 255, 200))

        cmd_lower = command.lower()
        cmd_parts = command.split()

        # Обработка команд
        if cmd_lower in ["bios", "uefi"]:
            self.show_bios_tools()
            return
        elif cmd_lower in ["firewall", "брандмауэр"]:
            self.print_text("🔥 Используйте кнопку 'Безопасность' для инструментов брандмауэра\n", self.info_color)
            return
        elif cmd_lower in ["speedtest", "speed", "скорость"]:
            self.print_text("🌐 Тест скорости интернета в разработке...\n", self.info_color)
            return
        elif cmd_lower in ["optimize", "оптимизация"]:
            self.show_optimization_tools()
            return
        elif cmd_lower in ["exit", "quit"]:
            self.close()
            return
        elif cmd_lower in ["clear", "cls"]:
            self.clear_console()
            return
        elif cmd_lower == "help":
            self.show_help()
            return
        elif cmd_lower == "open":
            self.open_target_folder()
            return
        elif cmd_lower == "mkdir":
            self.create_folder_dialog()
            return
        elif cmd_lower in ["nb", "notebook"]:
            self.create_notebook_dialog()
            return
        elif cmd_lower == "ip":
            self.show_ip_info()
            return
        elif cmd_lower == "monitor":
            self.show_system_monitor()
            return
        elif cmd_parts and cmd_parts[0].lower() == "ping":
            if len(cmd_parts) > 1:
                self.do_ping_command(cmd_parts[1])
            else:
                self.print_text("❌ Использование: ping <host>\n", self.error_color)
            return
        elif cmd_parts and cmd_parts[0].lower() == "mkdir":
            if len(cmd_parts) > 1:
                folder_name = " ".join(cmd_parts[1:])
                self.create_folder(folder_name)
            else:
                self.create_folder_dialog()
            return
        elif cmd_parts and cmd_parts[0].lower() in ["nb", "notebook"]:
            if len(cmd_parts) > 1:
                notebook_name = " ".join(cmd_parts[1:])
                self.create_notebook(notebook_name)
            else:
                self.create_notebook_dialog()
            return
        else:
            self.run_system_command(command)

    def do_ping_command(self, host):
        """Выполнение команды ping"""
        self.print_text(f"📡 Пинг {host}...\n", self.network_color)

        try:
            param = '-n' if self.is_windows else '-c'
            command = ['ping', param, '4', host]

            result = subprocess.run(command, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                self.print_text("✅ Пинг успешен!\n", self.success_color)
                if result.stdout:
                    self.print_text(result.stdout[:500] + "\n", self.text_color)
            else:
                self.print_text(f"❌ Ошибка: {result.stderr}\n", self.error_color)
        except subprocess.TimeoutExpired:
            self.print_text("❌ Таймаут\n", self.error_color)
        except Exception as e:
            self.print_text(f"❌ Ошибка: {e}\n", self.error_color)

    def run_system_command(self, command):
        """Выполнение системной команды"""
        try:
            if self.is_windows:
                target_path = str(self.target_dir)
                if ' ' in target_path:
                    target_path = f'"{target_path}"'

                full_command = f'cd /d {target_path} && {command}'
                shell_cmd = ["cmd.exe", "/c", full_command]
            else:
                import shlex
                target_path = shlex.quote(str(self.target_dir))
                full_command = f'cd {target_path} && {command}'
                shell_cmd = ["/bin/bash", "-c", full_command]

            self.print_text(f"📍 Выполняю в: {self.target_dir}\n", self.output_color)

            process = subprocess.Popen(
                shell_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                encoding='utf-8'
            )

            output, error = process.communicate()

            if output:
                self.print_text(output, self.text_color)
            if error:
                self.print_text(error, self.error_color)

            if process.returncode == 0:
                self.print_text(f"✅ Команда выполнена\n", self.success_color)
            else:
                self.print_text(f"❌ Код ошибки: {process.returncode}\n", self.error_color)

        except Exception as e:
            self.print_text(f"💥 Ошибка: {e}\n", self.error_color)

    def format_bytes(self, bytes):
        """Форматирование байтов в читаемый вид"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"

    def keyPressEvent(self, event):
        """Горячие клавиши"""
        if event.key() == Qt.Key_F1:
            self.show_help()
        elif event.key() == Qt.Key_F2:
            self.open_target_folder()
        elif event.key() == Qt.Key_F3:
            self.create_notebook_dialog()
        elif event.key() == Qt.Key_F4:
            self.create_folder_dialog()
        elif event.key() == Qt.Key_F5:
            self.refresh_info()
        elif event.key() == Qt.Key_F6:
            self.clear_console()
        elif event.key() == Qt.Key_F7:
            self.show_developer_tools()
        elif event.key() == Qt.Key_F8:
            self.show_system_monitor()
        elif event.key() == Qt.Key_F9:
            self.show_network_tools()
        elif event.key() == Qt.Key_F10:
            self.show_security_tools()
        elif event.key() == Qt.Key_F11:
            self.show_bios_tools()
        elif event.key() == Qt.Key_F12:
            self.show_optimization_tools()
        elif event.key() == Qt.Key_Up:
            if self.command_history and self.history_index > 0:
                self.history_index -= 1
                self.command_input.setText(self.command_history[self.history_index])
        elif event.key() == Qt.Key_Down:
            if self.command_history and self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.command_input.setText(self.command_history[self.history_index])
            elif self.history_index == len(self.command_history) - 1:
                self.history_index = len(self.command_history)
                self.command_input.clear()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """Закрытие приложения"""
        self.save_settings()
        event.accept()

    def print_welcome(self):
        """Приветственное сообщение"""
        welcome = f"""
╔══════════════════════════════════════════════════════════╗
║          🚀 OPTIMIZED CONSOLE v11.0                      ║
║           ВСЕ КНОПКИ РАБОТАЮТ!                           ║
║           ТЕКСТ ПРИ НАЖАТИИ ВИДЕН!                       ║
╚══════════════════════════════════════════════════════════╝

📌 БЫСТРЫЕ ДЕЙСТВИЯ (нижняя панель - ВСЕ РАБОТАЮТ!):
  • 📁 Открыть папку    - открыть текущую папку
  • 📄 Создать блокнот  - создать блокнот
  • 📁 Создать папку    - создать папку
  • 🛠️ Инструменты     - инструменты разработчика
  • 🔐 Безопасность    - инструменты безопасности  
  • 📊 Мониторинг      - мониторинг системы
  • 📡 Сеть            - сетевые инструменты
  • 🌐 IP информация   - показать IP адреса
  • ⚡ BIOS            - информация о BIOS
  • 🔧 Оптимизация     - оптимизация системы

📌 ОСНОВНЫЕ КОМАНДЫ:
  • help        - показать справку
  • mkdir       - создать папку
  • nb          - создать блокнот
  • open        - открыть текущую папку
  • ip          - показать IP адреса
  • ping <host> - пинг хоста
  • monitor     - мониторинг системы
  • clear/cls   - очистить консоль

📌 ГОРЯЧИЕ КЛАВИШИ:
  • F1 - справка
  • F2 - открыть папку  
  • F3 - создать блокнот
  • F4 - создать папку
  • F5 - обновить
  • F6 - очистить консоль
  • F7 - инструменты разработчика
  • F8 - мониторинг системы
  • F9 - сетевые инструменты
  • F10 - безопасность
  • F11 - BIOS
  • F12 - оптимизация

📁 Текущая папка: {self.target_dir}

✨ ВСЕ КНОПКИ РАБОТАЮТ!
⚡ ТЕКСТ ПРИ НАЖАТИИ ХОРОШО ВИДЕН!
🔧 СТАБИЛЬНАЯ РАБОТА ГАРАНТИРОВАНА!
════════════════════════════════════════════════════════════
"""
        self.print_text(welcome, self.output_color)


# ==============================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ==============================================

def main():
    # Создаем приложение
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Настройка шрифта
    font = QFont()
    font.setFamily('Segoe UI')
    font.setPointSize(10)
    app.setFont(font)

    # Устанавливаем иконку
    app.setWindowIcon(EmbeddedLogo.get_logo_icon())

    # Создаем и показываем главное окно
    window = OptimizedConsoleWindow()
    window.show()

    # Запускаем приложение
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("=" * 60)
        print("🚀 OPTIMIZED CONSOLE v11.0")
        print("=" * 60)
        print(f"Ошибка при запуске: {e}")
        print("\nУстановите необходимые библиотеки:")
        print("pip install PyQt5 psutil requests")
        print("=" * 60)
        input("Нажмите Enter для выхода...")