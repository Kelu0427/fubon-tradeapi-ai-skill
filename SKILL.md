---
name: fubon-trade-api
description: Use when helping users write, review, debug, or validate code for Fubon Neo / Fubon Securities TradeAPI / 富邦新一代 API / 富邦證券 API, including natural-language requests about market data, stock trading, futures/options trading, account queries, conditional orders, SDK installation, authentication, certificates, and API Key login. This skill uses the official online llms.txt and llms-full.txt first, with bundled local copies as offline fallback.
metadata:
  short-description: Build and verify Fubon TradeAPI code
---

# Fubon TradeAPI Skill

Use this skill whenever the user asks for help with Fubon Neo, Fubon Securities API, Fubon TradeAPI, 富邦新一代 API, 富邦證券 API, or natural-language-to-code assistance for Fubon market data, trading, account, futures/options, or condition-order workflows.

## Source Of Truth

- Official online index: `https://www.fbs.com.tw/TradeAPI/llms.txt`. Use first for navigation when network is available.
- Official online full docs: `https://www.fbs.com.tw/TradeAPI/llms-full.txt`. Use for exact signatures, object fields, examples, constants, version notes, and error codes when network is available.
- Bundled `llms.txt` and `llms-full.txt`: local cache and offline fallback.
- `references/fubon-api-guidance.md`: local workflow and recurring gotchas for agents.
- `scripts/search_docs.py`: deterministic search/extract/sync helper for official online docs and local cached docs.

Do not invent API names, enum names, parameter order, or object fields. Prefer official online `llms-full.txt`; if network is unavailable, use the bundled `llms-full.txt` cache and say it is the local snapshot.

## Workflow

1. Classify the user's intent:
   - SDK setup/version compatibility
   - authentication, password login, API Key login, certificate login
   - market data REST
   - market data WebSocket
   - stock trading and stock account queries
   - futures/options trading and account queries
   - smart/conditional orders
   - error handling, reconnect, or rate limit behavior
2. Determine the target language. If unspecified, default to Python and say that assumption.
3. Search the docs with `scripts/search_docs.py`; add `--online` when current official docs are needed and network is available.
4. Read the exact matching section(s) from `llms-full.txt`; prefer official examples in the user's language.
5. Produce code that includes imports, login/init steps, object construction, API call, response/error handling, and logout/cleanup when relevant.
6. If reviewing code, check every SDK call, enum, object field, and argument order against `llms-full.txt`.

## Intent Mapping

Use these natural-language cues and stable API terms to choose searches:

- setup/version/install/Python version/SDK: search `SDK`, `compatibility`, `Python 3.13`, `v2.2.8`.
- login/certificate/API Key/account: search `login`, `apikey_login`, `API Key`, `certPath`, `Account`.
- stock quote/price/K-line/books/trades: search `Intraday Quote`, `intraday.quote`, `Historical Candles`, `Trades`, `Books`.
- WebSocket/subscribe/realtime streaming: search `websocket_client`, `subscribe`, `Trades`, `Books`, `Candles`.
- stock order/buy/sell/modify/cancel/order result: search `place_order`, `Order Object`, `modify_price`, `cancel_order`, `get_order_results`.
- futures/options/margin/position: search `trading-future`, `place_order`, `query_margin_equity`, `query_single_position`, `query_estimate_margin`.
- conditional order/TPSL/trailing profit/time slice: search `smart-condition`, `single_condition`, `multi_condition`, `TPSL`, `trail_profit`, `time_slice_order`.

## Search Examples

```bash
python scripts/search_docs.py sync
python scripts/search_docs.py search "place_order OrderType PriceType TimeInForce" --online
python scripts/search_docs.py search "API Key apikey_login" --online
python scripts/search_docs.py section "Intraday Quote" --online
python scripts/search_docs.py section "API Key"
python scripts/search_docs.py lines 23770 23820
```

On Windows PowerShell:

```powershell
python .\scripts\search_docs.py search "place_order OrderType PriceType TimeInForce"
```

## Response Requirements

- State the verified SDK version or version constraint when relevant.
- Name the exact documentation anchors searched when giving non-trivial code, e.g. `place_order`, `Order Object`, `Intraday Quote`, `apikey_login`.
- Use placeholders for secrets and personal data. Never ask users to paste passwords, API keys, private keys, ID numbers, or certificate passwords into chat.
- For trading code, explicitly identify whether it may place a real order. Prefer dry-run/review snippets unless the user explicitly asks for live order code.
- For live order examples, make the account/order parameters obvious placeholders and include a final confirmation step in comments.
- For market data examples, include `sdk.login(...)` and `sdk.init_realtime()` when the official docs require login for market data permission.
- Prefer modern behavior documented for SDK v2.2.8 unless the user states an older version.
- If the docs are ambiguous or language-specific, answer with the verified language only and say what still needs checking for other languages.

## Common Python Anchors

Verify details in `llms-full.txt` before finalizing, but these anchors help search:

- SDK import: `from fubon_neo.sdk import FubonSDK`
- Stock order object: `from fubon_neo.sdk import Order`
- Trading constants commonly include `BSAction`, `OrderType`, `PriceType`, `MarketType`, `TimeInForce`
- Market data REST client: `sdk.marketdata.rest_client.stock` or `sdk.marketdata.rest_client.futopt`
- Market data WebSocket client: `sdk.marketdata.websocket_client.stock` or `sdk.marketdata.websocket_client.futopt`
- Stock trading namespace: `sdk.stock`
- Futures/options trading namespace: commonly documented under `trading-future`

## Quality Checklist

Before answering:

- You searched official online `llms-full.txt` when possible, or the bundled local cache when offline. Do not rely on `llms.txt` alone.
- The code path matches the requested domain: stock vs futures/options, REST vs WebSocket, trading vs condition order.
- The code imports every SDK class/constant it uses.
- Function/method names match the target language casing (`place_order` in Python, `placeOrder` in JavaScript, `PlaceOrder` in C#).
- Enum/member casing matches the target language.
- Date/time strings match the documented format.
- Quantity units are clear: stocks usually use shares; futures/options use lots/contracts per docs.
- Price fields follow the documented type: many order APIs use string prices.
- Market/order/price/time-in-force combinations are plausible and documented.
- Error handling follows the documented SDK version behavior where available.
- Secrets are placeholders or environment variables.

