# TransChat Beta

## 📘 簡介

TransChat 是一款結合 **即時翻譯** 與 **AI 對話功能** 的 Python 桌面小工具，目前處於測試階段（Beta）。本工具旨在提供開發者快速測試語言轉換與簡易自然語言理解的能力，採用 Google Translate API 與 Gemini 模型（可選）作為後端服務。

## ⚙️ 功能介紹

- 🌍 **即時翻譯系統**
  - 自動偵測輸入語言，並即時翻譯為指定語言
  - 支援語言：繁體中文、簡體中文、英文、日文
  - 使用 Google Cloud Translation API

- 🤖 **簡易 AI 對話系統**
  - 可處理簡單指令（目前僅支援 `web search`）
  - 回傳格式為 JSON 指令物件，便於開發整合

- 💬 **仿 ChatGPT UI**
  - 使用 PyQt 設計聊天介面，支援訊息靠左/右、自動捲動等功能
  - 可設定快捷鍵喚起工具視窗

## 🚀 如何使用

- 3-1. pip 安裝與啟動

  請先安裝必要套件：
  pip install PyQt6 keyboard google-generativeai deep-translator SpeechRecognition

- 3-1. API 
  請於程式內 Class AI 的 init 區域填入API

---- 祝您使用愉快 記得幫我按星星 ---- 
