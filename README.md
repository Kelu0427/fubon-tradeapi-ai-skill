# Fubon TradeAPI Skill

這是一個給 AI agent 使用的 Codex Skill，目標是讓使用者用自然語言描述需求後，agent 可以依照富邦新一代 API / Fubon Neo / Fubon Securities TradeAPI 官方文件，協助產生、檢查與修正正確的 API 程式碼。

> English version: [README_EN.md](README_EN.md)

## 文件來源

本專案採用「官方線上文件優先、本地快取備援」：

- 官方索引文件：https://www.fbs.com.tw/TradeAPI/llms.txt
- 官方完整文件：https://www.fbs.com.tw/TradeAPI/llms-full.txt
- 本地 `llms.txt` / `llms-full.txt`：離線備援與可重現搜尋用快取

## 支援範圍

- SDK 安裝與版本相容性
- 一般登入、API Key 登入、憑證路徑與帳號回傳資料
- 股票行情 REST / WebSocket
- 期貨與選擇權行情、交易與帳務查詢
- 股票下單、改價、刪單、委託與成交查詢
- 智慧條件單：單一條件、多條件、停損停利、移動停利、分時分量
- 程式碼審查：方法名稱、enum、參數順序、物件欄位、版本限制、實單風險

## 專案結構

```text
fubon-tradeapi-ai-skill/
|-- SKILL.md
|-- README.md
|-- README_EN.md
|-- llms.txt
|-- llms-full.txt
|-- agents/
|   `-- openai.yaml
|-- references/
|   `-- fubon-api-guidance.md
`-- scripts/
    `-- search_docs.py
```

## 安裝成 Codex Skill

將整個資料夾複製到：

```text
<CODEX_HOME>/skills/fubon-trade-api
```

`<CODEX_HOME>` 通常是使用者家目錄下的 `.codex`，例如 Windows 的 `%USERPROFILE%\.codex`，或 macOS/Linux 的 `~/.codex`。

複製完成後，重新開啟新的 Codex session，讓 Skill metadata 重新載入。

## 使用範例

```text
使用 $fubon-trade-api 幫我寫 Python 程式：登入富邦 TradeAPI，查詢 2330 即時報價，不要下單。
```

```text
使用 $fubon-trade-api 幫我檢查這段 place_order 程式碼，確認 enum、參數順序與價格型別是否符合官方文件。
```

```text
使用 $fubon-trade-api 幫我寫 API Key 登入範例，敏感資料請用環境變數。
```

## 查詢官方文件

網路可用時，優先查官方線上文件：

```powershell
python .\scripts\search_docs.py search "place_order OrderType PriceType TimeInForce" --online
python .\scripts\search_docs.py section "Intraday Quote" --online
python .\scripts\search_docs.py lines 23770 23820 --online
```

離線時使用本地快取：

```powershell
python .\scripts\search_docs.py search "place_order OrderType PriceType TimeInForce"
```

從官方 URL 更新本地快取：

```powershell
python .\scripts\search_docs.py sync
```

## 注意事項

- `llms.txt` 只是索引，產生或審查程式碼時應以 `llms-full.txt` 為準。
- 優先使用官方線上文件；無網路時才使用本地快取，或先執行 `sync` 更新快取。
- 交易與條件單範例可能會送出真實委託，執行前必須檢查帳號、商品、價格、數量與買賣方向。
- 不要在聊天中貼上身分證字號、密碼、API Key、憑證密碼、私鑰或帳號等敏感資料。
- 若 API 行為與 SDK 版本有關，依官方文件或剛同步的本地快取為準。
