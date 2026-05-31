# Fubon TradeAPI Skill

This project is a Codex Skill for AI agents. It helps users turn natural-language requests into code that follows the official Fubon Neo / Fubon Securities TradeAPI documentation, and helps review existing code for API correctness.

Primary documentation sources:

- Official online index: https://www.fbs.com.tw/TradeAPI/llms.txt
- Official online full docs: https://www.fbs.com.tw/TradeAPI/llms-full.txt
- Bundled `llms.txt` and `llms-full.txt`: local cache for offline use and deterministic searches.

## What This Skill Covers

- SDK installation and version compatibility.
- Password login, API Key login, certificate paths, and account responses.
- Stock market data REST and WebSocket workflows.
- Futures/options market data and trading/account workflows.
- Stock trading: place, modify, cancel, and query orders.
- Smart/conditional orders: single condition, multi condition, TPSL, trailing profit, and time-slice orders.
- Code review checks for method names, enums, argument order, object fields, version constraints, and live-order risk.

## Project Structure

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

## Install As A Codex Skill

Copy the whole folder to:

```text
<CODEX_HOME>/skills/fubon-trade-api
```

`<CODEX_HOME>` is usually `%USERPROFILE%\.codex` on Windows or `~/.codex` on macOS/Linux.

After copying, start a new Codex session so the Skill metadata can be reloaded.

## Usage Examples

| Category | Prompt example |
| --- | --- |
| SDK / install | Use `$fubon-trade-api` to confirm which Python versions the Fubon TradeAPI SDK supports and give me Windows installation steps. |
| Login | Use `$fubon-trade-api` to write a Python login example using environment variables for the ID, password, certificate path, and certificate password. |
| API Key login | Use `$fubon-trade-api` to write an API Key login example and verify the minimum SDK version required by the official docs. |
| Market data / REST | Use `$fubon-trade-api` to write Python code that logs in and queries the real-time quote for 2330. Do not place an order. |
| Market data / WebSocket | Use `$fubon-trade-api` to write a stock trades WebSocket subscription example with connection, subscription, callback, and disconnect handling. |
| Trading / stock order | Use `$fubon-trade-api` to write a stock limit-buy example with obvious placeholders and a final confirmation comment before sending. |
| Trading / modify and cancel | Use `$fubon-trade-api` to write stock order price-modification and cancellation examples, and verify which order identifiers are required. |
| Accounting / stock | Use `$fubon-trade-api` to find stock accounting and order-query methods in the official docs and list their Python method names. |
| Futures/options | Use `$fubon-trade-api` to write a futures margin query example and verify the namespace, method name, and account type. |
| Smart condition orders | Use `$fubon-trade-api` to write a TPSL condition-order example and explain which fields may require SDK-version checks. |
| Code review | Use `$fubon-trade-api` to review this `place_order` code and verify enums, argument order, price types, and live-order risk. |
| Error handling | Use `$fubon-trade-api` to add error handling for a market-data REST query and verify `FugleAPIError` usage from the official docs. |

## Manual Documentation Search

Use online official docs first when network is available:

```powershell
python .\scripts\search_docs.py search "place_order OrderType PriceType TimeInForce" --online
python .\scripts\search_docs.py section "Intraday Quote" --online
python .\scripts\search_docs.py lines 23770 23820 --online
```

Use local cached docs when offline:

```powershell
python .\scripts\search_docs.py search "place_order OrderType PriceType TimeInForce"
```

Refresh the bundled local cache from official URLs:

```powershell
python .\scripts\search_docs.py sync
```

## Safety Notes

- `llms.txt` is only an index. Use `llms-full.txt` as the source of truth for code generation and code review.
- Prefer official online docs; use bundled local docs as an offline fallback or after running `sync`.
- Trading and conditional-order examples can place real orders. Use placeholders and require parameter review before live use.
- Do not paste personal IDs, passwords, API keys, certificate passwords, private keys, or account identifiers into chat.
- When API behavior depends on SDK version, follow the version constraints in the official docs or the freshly synced local cache.

## License

This project is licensed under the [MIT License](LICENSE).
