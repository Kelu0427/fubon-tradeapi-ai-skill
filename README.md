# Fubon TradeAPI Skill

這是一個給 AI agent 使用的 Codex Skill，目標是讓使用者用自然語言描述需求後，agent 可以依照富邦新一代 API / Fubon Neo / Fubon Securities TradeAPI 官方文件，協助產生、檢查與修正正確的 API 程式碼。

> English version: [README_EN.md](README_EN.md)

## 文件來源

本專案採用「官方線上文件優先、本地快取備援」：

- 官方索引文件：https://www.fbs.com.tw/TradeAPI/llms.txt
- 官方完整文件：https://www.fbs.com.tw/TradeAPI/llms-full.txt
- 本地 `llms.txt` / `llms-full.txt`：離線備援與可重現搜尋用快取

## 支援範圍

- SDK 安裝、版本相容性、本地環境檢查與最新版安裝
- 一般登入、API Key 登入、憑證路徑與帳號回傳資料
- 股票行情 REST / WebSocket
- 期貨與選擇權行情、交易與帳務查詢
- 股票下單、改價、刪單、委託與成交查詢
- 智慧條件單：單一條件、多條件、停損停利、移動停利、分時分量
- 大型 Fubon API 串接專案檢查：掃描整體架構、SDK 使用點、設定、風控與文件一致性
- 程式碼審查：方法名稱、enum、參數順序、物件欄位、版本限制、實單風險

## 專案結構

```text
fubon-tradeapi-ai-skill/
|-- SKILL.md
|-- LICENSE
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

一鍵安裝或更新：

Windows PowerShell：

```powershell
$skill="$env:USERPROFILE\.codex\skills\fubon-trade-api"; New-Item -ItemType Directory -Force (Split-Path $skill) | Out-Null; if (Test-Path "$skill\.git") { git -C $skill pull } else { git clone https://github.com/Kelu0427/fubon-tradeapi-ai-skill.git $skill }
```

macOS / Linux：

```bash
skill="$HOME/.codex/skills/fubon-trade-api"; mkdir -p "$(dirname "$skill")"; if [ -d "$skill/.git" ]; then git -C "$skill" pull; else git clone https://github.com/Kelu0427/fubon-tradeapi-ai-skill.git "$skill"; fi
```

手動安裝時，將整個資料夾複製到：

```text
<CODEX_HOME>/skills/fubon-trade-api
```

`<CODEX_HOME>` 通常是使用者家目錄下的 `.codex`，例如 Windows 的 `%USERPROFILE%\.codex`，或 macOS/Linux 的 `~/.codex`。

複製完成後，重新開啟新的 Codex session，讓 Skill metadata 重新載入。

## 使用範例

| 種類 | 提示詞範例 |
| --- | --- |
| SDK / 安裝 / 環境檢查 | 使用 `$fubon-trade-api` 幫我檢查本機環境是否符合富邦 TradeAPI SDK 要求，包含 Python 版本、作業系統、SDK 是否已安裝，並協助安裝或更新到官方最新版。 |
| 登入 | 使用 `$fubon-trade-api` 幫我寫 Python 登入範例，帳密、憑證路徑和憑證密碼都改用環境變數。 |
| API Key 登入 | 使用 `$fubon-trade-api` 幫我寫 API Key 登入範例，並確認官方文件要求的 SDK 最低版本。 |
| 行情 / REST | 使用 `$fubon-trade-api` 幫我寫 Python 程式：登入後查詢 2330 即時報價，不要下單。 |
| 行情 / WebSocket | 使用 `$fubon-trade-api` 幫我寫訂閱股票成交明細 WebSocket 的範例，包含連線、訂閱、callback 和斷線處理。 |
| 交易 / 股票下單 | 使用 `$fubon-trade-api` 幫我寫股票限價買進範例，但請用明顯 placeholder，並加上送出前確認註解。 |
| 交易 / 改刪單 | 使用 `$fubon-trade-api` 幫我寫股票委託改價與刪單範例，並確認需要哪些委託識別欄位。 |
| 帳務 / 股票 | 使用 `$fubon-trade-api` 幫我查官方文件裡股票帳務與委託查詢有哪些方法，並列出 Python method name。 |
| 期貨 / 選擇權 | 使用 `$fubon-trade-api` 幫我寫期貨保證金查詢範例，確認 namespace、method name 和帳號型別。 |
| 智慧條件單 | 使用 `$fubon-trade-api` 幫我寫停損停利條件單範例，並說明哪些欄位可能因 SDK 版本不同而需要確認。 |
| 大型專案檢查 | 使用 `$fubon-trade-api` 幫我檢查這個大型台股自動交易專案的 Fubon API 串接，請掃描登入、行情、交易、帳務、設定檔、secret、paper/live gate、風控與官方 API 一致性，並輸出 P0/P1/P2 問題、修正建議與驗證步驟；不要實際登入或下單。 |
| 程式碼審查 | 使用 `$fubon-trade-api` 幫我檢查這段 `place_order` 程式碼，確認 enum、參數順序、價格型別和是否有實單風險。 |
| 錯誤處理 | 使用 `$fubon-trade-api` 幫我補上行情 REST 查詢的錯誤處理，請依官方文件確認 `FugleAPIError` 用法。 |

## 注意事項

- `llms.txt` 只是索引，產生或審查程式碼時應以 `llms-full.txt` 為準。
- 優先使用官方線上文件；無網路時才使用本地快取，或先執行 `sync` 更新快取。
- 交易與條件單範例可能會送出真實委託，執行前必須檢查帳號、商品、價格、數量與買賣方向。
- 不要在聊天中貼上身分證字號、密碼、API Key、憑證密碼、私鑰或帳號等敏感資料。
- 需要登入的範例應使用環境變數；可複製 `.env.example` 成 `.env` 後填入自己的資料，`.env` 不應提交到 Git。
- 若 API 行為與 SDK 版本有關，依官方文件或剛同步的本地快取為準。

## 授權

本專案採用 [MIT License](LICENSE)。
