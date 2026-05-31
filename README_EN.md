# Fubon TradeAPI Skill

This project is a Codex Skill for AI agents. It helps users turn natural-language requests into code that follows the official Fubon Neo / Fubon Securities TradeAPI documentation, and helps review existing code for API correctness.

Primary documentation sources:

- Official online index: https://www.fbs.com.tw/TradeAPI/llms.txt
- Official online full docs: https://www.fbs.com.tw/TradeAPI/llms-full.txt
- Bundled `llms.txt` and `llms-full.txt`: local cache for offline use and deterministic searches.

## What This Skill Covers

- SDK installation, version compatibility, local environment checks, and latest-version setup.
- Password login, API Key login, certificate paths, and account responses.
- Stock market data REST and WebSocket workflows.
- Futures/options market data and trading/account workflows.
- Stock trading: place, modify, cancel, and query orders.
- Smart/conditional orders: single condition, multi condition, TPSL, trailing profit, and time-slice orders.
- Large Fubon API project audits: scan architecture, SDK usage points, settings, risk controls, and documentation consistency.
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

One-command install or update:

Windows PowerShell:

```powershell
$skill="$env:USERPROFILE\.codex\skills\fubon-trade-api"; New-Item -ItemType Directory -Force (Split-Path $skill) | Out-Null; if (Test-Path "$skill\.git") { git -C $skill pull } else { git clone https://github.com/Kelu0427/fubon-tradeapi-ai-skill.git $skill }
```

macOS / Linux:

```bash
skill="$HOME/.codex/skills/fubon-trade-api"; mkdir -p "$(dirname "$skill")"; if [ -d "$skill/.git" ]; then git -C "$skill" pull; else git clone https://github.com/Kelu0427/fubon-tradeapi-ai-skill.git "$skill"; fi
```

For manual installation, copy the whole folder to:

```text
<CODEX_HOME>/skills/fubon-trade-api
```

`<CODEX_HOME>` is usually `%USERPROFILE%\.codex` on Windows or `~/.codex` on macOS/Linux.

After copying, start a new Codex session so the Skill metadata can be reloaded.

## Usage Examples

| Category | Prompt example |
| --- | --- |
| SDK / install / environment check | Use `$fubon-trade-api` to check whether my local environment meets Fubon TradeAPI SDK requirements, including Python version, operating system, whether the SDK is installed, and help install or update to the latest official version. |
| Login | Use `$fubon-trade-api` to write a Python login example using environment variables for the ID, password, certificate path, and certificate password. |
| API Key login | Use `$fubon-trade-api` to write an API Key login example and verify the minimum SDK version required by the official docs. |
| Market data / REST | Use `$fubon-trade-api` to write Python code that logs in and queries the real-time quote for 2330. Do not place an order. |
| Market data / WebSocket | Use `$fubon-trade-api` to write a stock trades WebSocket subscription example with connection, subscription, callback, and disconnect handling. |
| Trading / stock order | Use `$fubon-trade-api` to write a stock limit-buy example with obvious placeholders and a final confirmation comment before sending. |
| Trading / modify and cancel | Use `$fubon-trade-api` to write stock order price-modification and cancellation examples, and verify which order identifiers are required. |
| Accounting / stock | Use `$fubon-trade-api` to find stock accounting and order-query methods in the official docs and list their Python method names. |
| Futures/options | Use `$fubon-trade-api` to write a futures margin query example and verify the namespace, method name, and account type. |
| Smart condition orders | Use `$fubon-trade-api` to write a TPSL condition-order example and explain which fields may require SDK-version checks. |
| Large project audit | Use `$fubon-trade-api` to audit this large Taiwan stock automation project's Fubon API integration. Scan login, market data, trading, accounting, settings, secrets, paper/live gates, risk controls, and official API consistency. Output P0/P1/P2 findings, fixes, and validation steps. Do not actually log in or place orders. |
| Code review | Use `$fubon-trade-api` to review this `place_order` code and verify enums, argument order, price types, and live-order risk. |
| Error handling | Use `$fubon-trade-api` to add error handling for a market-data REST query and verify `FugleAPIError` usage from the official docs. |

## Safety Notes

- `llms.txt` is only an index. Use `llms-full.txt` as the source of truth for code generation and code review.
- Prefer official online docs; use bundled local docs as an offline fallback or after running `sync`.
- Trading and conditional-order examples can place real orders. Use placeholders and require parameter review before live use.
- Do not paste personal IDs, passwords, API keys, certificate passwords, private keys, or account identifiers into chat.
- Login examples should use environment variables. Copy `.env.example` to `.env` and fill in your own values; `.env` must not be committed to git.
- When API behavior depends on SDK version, follow the version constraints in the official docs or the freshly synced local cache.

## License

This project is licensed under the [MIT License](LICENSE).
