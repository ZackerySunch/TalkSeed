import json
import keyboard
import threading
import webbrowser
from functools import partial
import speech_recognition as sr
from PyQt6.QtGui import QKeyEvent
import google.generativeai as genai
from deep_translator import GoogleTranslator

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QEvent
from PyQt6.QtWidgets import QButtonGroup
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, 
                             QVBoxLayout, QWidget, QPushButton, QToolBar,
                             QHBoxLayout, QTextEdit, QComboBox, QScrollArea, 
                             QLabel, QSizePolicy)

class Sunch_Nexus(QMainWindow):
    translation_done = pyqtSignal(str)

    def __init__(self,start):
        print("Sunch Nexus")
        super().__init__()
        self.setWindowTitle("Sunch Nexus")
        self.setFixedSize(480, 640)
        
        self.pages = []
        self.start = start
        
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.create_stacked_widget()
        self.create_pages()
        self.page1(self.pages[0])
        self.page2(self.pages[1])
        self.top_bar()
        
    def create_stacked_widget(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()

        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                border-radius: 10px; /* 圓角半徑 */
            }
        """)
        self.layout.addWidget(self.stacked_widget)

    def create_pages(self):
        for i in range(2):
            page = QWidget()
            page.setStyleSheet("""
                QWidget {
                    border-radius: 10px; /* 圓角半徑 */
                    background-color: #181818; /* 背景顏色 */
                }
            """)
            self.pages.append(page)
            self.stacked_widget.addWidget(page) 
        
    def top_bar(self):
        # Toolbar for navigation
        self.toolbar = QToolBar("Navigation")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)

        buttons = []
        button_group = QButtonGroup(self)  # Create a button group to manage focus

        # Toolbar buttons
        button_text = ["🔠 翻譯", "💬 智慧助手"]
        button_width = [90, 110]  # Button width
        button_size = [18, 17]
        button_size_hover = [20, 19]  # Button size on hover
        pages = [self.pages[0], self.pages[1]]  # List of pages

        for i in range(2):
            button = QPushButton(button_text[i])
            button.setStyleSheet(f"""
            QPushButton {{
                font-size: {button_size[i]}px;
            }}
            QPushButton:hover {{
                font-size: {button_size_hover[i]}px;
                background-color: #444444; /* Change color on hover */
            }}
            QPushButton:checked {{
                font-size: {button_size_hover[i]}px;
                background-color: #666666; /* Change color when focused */
            }}
            """)
            button.setFixedSize(button_width[i], 40)
            button.setCheckable(True)  # Make the button checkable for focus tracking
            button_layout.addWidget(button)
            buttons.append(button)
            button_group.addButton(button, i)  # Add button to the group with an ID

            if i < 2:  # Bind each button to its corresponding page
                button.clicked.connect(partial(self.stacked_widget.setCurrentWidget, pages[i]))

            # Ensure only one button is checked at a time
            button_group.buttonClicked.connect(lambda btn: btn.setChecked(True))

            # Set default button to "智慧助手"
        
        buttons[1].setChecked(True)
        print(self.start)
        if 0 <= self.start < len(self.pages):
            self.stacked_widget.setCurrentWidget(self.pages[self.start])
            buttons[self.start].setChecked(True)
        else:
            print(f"Invalid start index: {self.start}. Defaulting to page 0.")
            self.stacked_widget.setCurrentWidget(self.pages[0])
        
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(button_layout)
        self.toolbar.addWidget(toolbar_widget)

    def page1(self, page):
        # Add logic for page1 or remove the unused variable
        layout = QVBoxLayout(page)
        # language1
        try:
            self.language1_button = QComboBox()
            self.language1_button.addItems(["繁體中文","简体中文","日本語","English"])
            self.language1_button.setCurrentText("繁體中文")
            self.language1_button.setFixedSize(450, 40)
            self.language1_button.currentIndexChanged.connect(self.translate)
            self.language1_button.setStyleSheet("""
                QComboBox{
                    font-size: 20px; 
                    color: #ffffff;  /* 文字顏色為白色 */
                    background-color: rgba(0, 0, 0, 0);  /* 背景完全透明 */
                    border: 1px solid #aaaaaa;  /* 邊框為淺灰色 */
                    border-radius: 10px;  /* 圓角邊框 */
                    padding: 5px;  /* 內邊距確保文字上下居中 */
                    text-align: center;  /* 文字水平居中 */
                }
                QComboBox:hover {
                    border: 1px solid #cccccc;  /* 懸停時邊框變亮 */
                }
                QComboBox::drop-down {
                    border-left: 1px solid #cccccc;  /* 下拉按鈕左側邊框 */
                    background-color: rgba(255, 255, 255, 0);  /* 下拉按鈕背景透明 */
                    border-radius: 10px;  /* 添加圓角邊框 */
                }
                QComboBox::down-arrow {
                    image: url('arrow_icon.png');  /* 替換為自定義箭頭圖標（需要提供圖標路徑） */
                    width: 10px;  /* 箭頭大小 */
                    height: 10px;
                }
                QComboBox QAbstractItemView {
                    background-color: rgba(0, 0, 0, 0.3);  /* 下拉選單背景半透明 */
                    color: #ffffff;  /* 下拉選單文字顏色 */
                    selection-background-color: #3399ff;  /* 選中項目背景色為亮藍色 */
                    selection-color: #ffffff;  /* 選中項目文字顏色為白色 */
                    border: 1px solid #cccccc;  /* 下拉選單邊框 */
                    border-radius: 10px;  /* 下拉選單圓角設置 */
                }
            """)
            
            layout.addWidget(self.language1_button)
        except Exception as e:
            print(e)
        
        # Textedit1
        try:
            self.text_edit1_trans = QTextEdit()
            self.text_edit1_trans.setFixedSize(450, 230)
            self.text_edit1_trans.setPlaceholderText("請翻譯文字...")
            self.text_edit1_trans.setStyleSheet("""
                QTextEdit {
                    font-size: 20px;
                    font-color: #ffffff;
                    background-color: #202020;
                }
            """)
            layout.addWidget(self.text_edit1_trans)
            self.text_edit1_trans.textChanged.connect(lambda:self.translate())
        except Exception as e:
            print(e)
        
        # language2
        try:
            self.language2_button = QComboBox()
            self.language2_button.addItems(["繁體中文","简体中文","日本語","English"])
            self.language2_button.setCurrentText("English")
            self.language2_button.setFixedSize(450, 40)
            self.language2_button.currentIndexChanged.connect(self.translate)
            self.language2_button.setStyleSheet("""
                QComboBox{
                    font-size: 20px; 
                    color: #ffffff;  /* 文字顏色為白色 */
                    background-color: rgba(0, 0, 0, 0);  /* 背景完全透明 */
                    border: 1px solid #aaaaaa;  /* 邊框為淺灰色 */
                    border-radius: 10px;  /* 圓角邊框 */
                    padding: 5px;  /* 內邊距確保文字上下居中 */
                    text-align: center;  /* 文字水平居中 */
                }
                QComboBox:hover {
                    border: 1px solid #cccccc;  /* 懸停時邊框變亮 */
                }
                QComboBox::drop-down {
                    border-left: 1px solid #cccccc;  /* 下拉按鈕左側邊框 */
                    background-color: rgba(255, 255, 255, 0);  /* 下拉按鈕背景透明 */
                    border-radius: 10px;  /* 添加圓角邊框 */
                }
                QComboBox::down-arrow {
                    image: url('arrow_icon.png');  /* 替換為自定義箭頭圖標（需要提供圖標路徑） */
                    width: 10px;  /* 箭頭大小 */
                    height: 10px;
                }
                QComboBox QAbstractItemView {
                    background-color: rgba(0, 0, 0, 0.3);  /* 下拉選單背景半透明 */
                    color: #ffffff;  /* 下拉選單文字顏色 */
                    selection-background-color: #3399ff;  /* 選中項目背景色為亮藍色 */
                    selection-color: #ffffff;  /* 選中項目文字顏色為白色 */
                    border: 1px solid #cccccc;  /* 下拉選單邊框 */
                    border-radius: 10px;  /* 下拉選單圓角設置 */
                }
            """)
            
            layout.addWidget(self.language2_button)
        except Exception as e:
            print(e)

        # Textedit2
        try:
            self.text_edit2_trans = QTextEdit()
            self.text_edit2_trans.setFixedSize(450, 230)
            self.text_edit2_trans.setPlaceholderText("翻譯文字...")
            self.text_edit2_trans.setReadOnly(True)
            self.text_edit2_trans.setStyleSheet("""
                QTextEdit {
                    font-size: 20px;
                    font-color: #ffffff;
                    background-color: #202020;
                }
            """)
            layout.addWidget(self.text_edit2_trans)
        except Exception as e:
            print(e)
            
    def page2(self, page):
        # Page 2 layout setup
        try:
            layout = QVBoxLayout(page)
            layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
            layout.setSpacing(0)  # Remove spacing
        except Exception as e:
            print(f"Error in setting up layout: {e}")

        # Chat display area
        try:
            self.chat_area = QScrollArea()
            self.chat_area.setWidgetResizable(True)
            self.chat_area.setFixedHeight(510)
            
            container = QWidget()
            self.chat_area.setWidget(container)
            
            # 可動態加訊息的 layout
            self.chat_layout = QVBoxLayout(container)
            self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            
            layout.addWidget(self.chat_area)  # Add chat_area to the layout
        except Exception as e:
            print(f"Error in setting up chat display area: {e}")

        layout.addStretch()
        
        # Input layout and box setup 
        try:
            input_layout = QHBoxLayout()

            self.text_edit1 = QTextEdit()
            self.text_edit1.setFixedSize(410, 50)
            self.text_edit1.setPlaceholderText("你好啊! 我是Sunch AI...")
            self.text_edit1.setStyleSheet("""
            QTextEdit {
            font-size: 20px;
            color: #ffffff;
            background-color: #151515;
            border: 1px solid #444444;
            border-radius: 5px;
            }
            QTextEdit QScrollBar:vertical {
            border: none;
            background: #202020;
            width: 10px;
            margin: 0px 0px 0px 0px;
            border-radius: 5px;
            }
            QTextEdit QScrollBar::handle:vertical {
            background: #555555;
            min-height: 20px;
            border-radius: 5px;
            }
            QTextEdit QScrollBar::handle:vertical:hover {
            background: #777777;
            }
            QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
            }
            """)
            
            # Install event filter to capture key events
            self.text_edit1.installEventFilter(self)

            input_layout.addWidget(self.text_edit1)
        except Exception as e:
            print(f"Error in setting up input box: {e}")

        # Send button setup
        try:
            input_layout.addStretch()
            send_button = QPushButton("⬆️")
            send_button.setStyleSheet("""
            QPushButton {
                font-size:  30px; 
                background-color: #333333; 
                border-radius: 10px;
            }
            QPushButton:hover {
                font-size:  40px; 
                background-color: #777777; /* Change color on hover */
            }
            """)
            send_button.setFixedSize(50, 50)
            send_button.clicked.connect(self.call_ai)
            input_layout.addWidget(send_button)
        except Exception as e:
            print(f"Error in setting up send button: {e}")

        layout.addLayout(input_layout)
        
    def eventFilter(self, obj, event):
        # 只攔截 text_edit1 的按鍵事件
        if obj == self.text_edit1 and event.type() == QEvent.Type.KeyPress:
            # 如果是 Enter（不含 Shift）
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                self.call_ai()
                return True  # 阻止預設換行
        return super().eventFilter(obj, event)

    def call_ai(self):
        value = self.text_edit1.toPlainText().strip()
        if (value != "") and (value != "\n") and (value != " "):
            print(value)
            self.text_edit1.setPlainText("")
            self.create_massage_box(value,"user")
            QTimer.singleShot(100, lambda:self.create_massage_box(value,"ai"))
            
    def create_massage_box(self,value,sender):
        try:
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(6, 6, 6, 6)
            if sender == "ai":
                label = QLabel("正在思考中...")
            else:
                label = QLabel(value)
            label.setWordWrap(True)
            label.setMaximumWidth(400)
            label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
            label.adjustSize()

            label.setStyleSheet("""
                background-color: #000000;
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 12px;
            """)
            if sender == 'user':
                layout.addStretch()
                layout.addWidget(label)
            else:
                layout.addWidget(label)
                layout.addStretch()
            self.chat_layout.addWidget(container)
            if sender == "ai":
                QTimer.singleShot(100,lambda: label.setText(AI().user(value)))
                
        except Exception as e:
            print(e)
    
    def translate(self):
        def translate_in_background():
            language = ["繁體中文","简体中文","日本語","English"]
            lenguage_change = ["zh-TW","zh-CN","ja","en"]        
            lan1 = lenguage_change[language.index(self.language1_button.currentText())]
            lan2 = lenguage_change[language.index(self.language2_button.currentText())]
            text = self.text_edit1_trans.toPlainText().strip()
            print(f"{lan1}=>{lan2}:\n{text}")
            translated_text = GoogleTranslator(source=lan1, target=lan2).translate(text)
            print(translated_text)
            self.translation_done.emit(translated_text) 

        self.translation_done.connect(self.text_edit2_trans.setText)
        threading.Thread(target=translate_in_background, daemon=True).start()

    def start_voice(self):
        print("start voice")
        
class AI:
    def __init__(self):
        genai.configure(api_key="GOOGLE API KEY")
       
    def user(self,user_input):
        self.model = genai.GenerativeModel("models/gemini-1.5-flash-latest",
                                    system_instruction = """
你是「Arctic」，是 Sunch HUB 桌面軟體中的本地 AI 助理，由 Sunch Tech 公司開發，你的工作環境是 Sunch HUB 25.6（2025年6月版本），目前處於 Beta 測試階段，因此僅支援網頁搜尋功能。

你的目標是根據使用者輸入的自然語言，輸出一段 JSON，其中包含：
1. 一個 `command` 物件，鍵必須是 "web search"，值是一個「字串陣列（list）」表示搜尋關鍵字
2. 一段你要對使用者說的自然語言回覆

【📘 指令格式】
{
  "web search": [關鍵字1, 關鍵字2, ...]
}

【🧾 格式補充規則】
- `web search` 的值一定要是**字串陣列**（即使只有一個關鍵字）
  - ✅ "web search": ["AI 工具"]
  - ❌ "web search": "AI 工具"（錯誤）

【🧠 查詢規則】
- 你必須先嘗試根據自身知識回覆使用者的問題。
- 僅當你確定無法回答，且這是一個合理的查詢型問題時，才產生 `"web search"` 指令。
- ❌ 不可以對寒暄或常識問題（如「hi」、「你是誰」）使用查詢。
- ✅ 不要回答「不知道」、「無法處理」、「這超出我的能力」，請改用 `"web search"` 嘗試協助使用者。

【📦 JSON 回傳格式】
{
  "command": {
    "web search": ["搜尋詞1", "搜尋詞2", ...]
  },
  "response": "你要對使用者說的自然語言"
}

【✅ 範例】
使用者說：「幫我查一下 AI 工具」
正確回應：
{
  "command": {
    "web search": ["AI 工具"]
  },
  "response": "好的，我會幫你搜尋『AI 工具』。"
}

【🚫 嚴格禁止事項】
- 不要在回傳中加入 ```、json、Markdown 語法或區塊。
- 不要加入任何開場白、註解、標點符號或裝飾性文字。
- 僅回傳一段 **純 JSON**，整段內容就是 JSON 本體。
""")
        response = self.model.generate_content(user_input)

        target = response.text.strip().lower()
        # print(f"code：{target}")
        if target[0] != "{":
            target = target.replace("```json", "")
            target = target.replace("```", "")

        parsed_response = json.loads(target)
        command = parsed_response.get("command", "None")
        self.run_command(command)
        reply = parsed_response.get("response", "無法理解您的請求。")
        return reply

    def run_command(self,run_cmd):
        if run_cmd == "None":
            return

        for group_action, targets in run_cmd.items():
            group, action = group_action.split(" ", 1)
            for target in targets:
                print(f"執行指令：{group} {action} {target}")
                # Add logic to handle each command here
                # finish
                if group == "web":
                    if action == "search":
                        webbrowser.open(f"https://www.google.com/search?q={target}")
        
if __name__ == "__main__":
    def launch_word(start):
        print("on call")
        app = QApplication([])
        window = Sunch_Nexus(start)
        window.show()
        app.exec()

    # 綁定快捷鍵（Windows 上會常駐監聽）
    try:
        trans = keyboard.add_hotkey("Ctrl+Alt+t", lambda:launch_word(0))
        chat = keyboard.add_hotkey("Ctrl+Alt+space", lambda:launch_word(1))

        print("✅ 快捷鍵啟動監聽中... 按 Ctrl+Alt+t/space/h/n 啟動  Sunch Nexus")
        keyboard.wait()  # 不退出程式
    except Exception as e:
        print(f"❌ 無法啟動快捷鍵監聽: {e}")
        print("請以管理員身份運行程式，或檢查是否安裝了 keyboard 模組。")
