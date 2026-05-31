# Fubon TradeAPI Agent Guidance

This file summarizes how to use the official online docs and bundled local cache without loading all of `llms-full.txt`.

## Documentation Map

- SDK/version/setup: search `SDK`, `compatibility`, `version`, `Python 3.13`, `v2.2.8`.
- API Key/certificate: search `API Key`, `apikey_login`, `certPath`, `certPass`, `Account`.
- Market data stock REST: search `market-data/http-api`, `rest_client.stock`, endpoint title such as `Intraday Quote`.
- Market data futures/options REST: search `market-data-future/http-api`, `rest_client.futopt`.
- Market data WebSocket: search `websocket-api`, channel name such as `Trades`, `Books`, `Candles`.
- Stock trading: search `trading/library/python`, `PlaceOrder`, `OrderHistory`, `GetOrderResults`, `ModifyPrice`, `CancelOrder`.
- Futures/options trading: search `trading-future/library/python`, `PlaceOrder`, `QueryMarginEquity`, `EstimateMargin`.
- Smart/condition orders: search `smart-condition`, `SingleCondition`, `MultiCondition`, `TPSL`, `TrailProfit`, `TimeSliceOrder`.
- Constants/enum tables: search exact object or constant names, e.g. `Order Object`, `ConditionOrder Object`, `TimeInForce`, `PriceType`.

## Retrieval Pattern

Use broad search first, then section extraction:

```powershell
python .\scripts\search_docs.py sync`npython .\scripts\search_docs.py search "PlaceOrder Python Order Object" --online
python .\scripts\search_docs.py section "PlaceOrder"
python .\scripts\search_docs.py lines 23770 23820
```

If the section title is hard to match because headings vary, search for a stable SDK method name such as `place_order`, `get_order_results`, `apikey_login`, `single_condition`, or `query_margin_equity`.

Search output includes line numbers. When a match is in a long or repeated section, use `lines START END` around the match instead of relying only on `section`.

## Coding Rules

- Prefer official examples from online `llms-full.txt` over memory. Use the bundled local cache when network is unavailable.
- Use `llms.txt` only as a URL/index map. Use `llms-full.txt` to verify code, fields, constants, and version rules. Run `python .\scripts\search_docs.py sync` to refresh the local cache from official URLs.
- Keep target-language naming exact:
  - Python: snake_case methods and PascalCase enum members are both common; verify each constant.
  - JavaScript: camelCase methods.
  - C#: PascalCase methods and members.
- Keep SDK object constructors in documented argument order. Do not reorder constructor arguments unless the docs show keyword arguments.
- Treat trading and condition-order examples as live-order-capable. Use placeholders and comments that force user review.
- When API version matters, use latest documented v2.2.8 behavior unless the user says otherwise.

## Natural Language Handling

- If the user asks to write code and mentions buy, sell, order, modify price, or cancel order, treat the request as live-order-capable and default to a guarded example.
- If the user asks to query data, decide whether it is market data (`rest_client.stock` / `rest_client.futopt`) or account/order data (`sdk.stock` / futures trading namespace) before writing code.
- If the user gives partial intent only, ask at most one clarification when the missing value changes the API surface, such as stock vs futures/options or REST vs WebSocket. Otherwise choose Python and explain the assumption.
- Never fill real credentials, certificate paths, account IDs, symbols, prices, or quantities from guesses. Use placeholders and comments.

## Frequent Pitfalls To Check

- `llms.txt` is only an index; do not use it alone for code. Prefer online docs or a freshly synced local cache.
- Market data examples often still require login before `init_realtime()` to get permission.
- API Key login requires SDK >= v2.2.7; web certificate export login requires SDK >= v2.2.8.
- Python 3.8-3.13 is supported by the documented v2.2.8 SDK; Python 3.14 is not supported in the current docs.
- For condition-order TPSL, SDK v2.2.0 added `trigger`; language defaults differ:
  - C# examples pass `null`.
  - Python/JavaScript examples may omit the field.
- For market-price or non-limit orders, docs may require blank string, `None`, `null`, or omitted price depending on object/language/version. Verify the exact object section.
- Stock order `user_def` rules changed in SDK >= 2.2.8: use only letters and digits, at most 10 characters, when including it.
- Python market data Web API errors are exception-based in SDK >= 2.2.4; import and handle the documented `FugleAPIError` when examples show it.

## Review Output Shape

For code review, lead with defects and cite the exact API mismatch:

- Wrong method/field/enum name
- Wrong namespace/client (`stock` vs `futopt`, REST vs WebSocket)
- Missing login/init step
- Wrong argument order
- Live order risk or secret exposure
- Version incompatibility

For generated code, include a short "verified against docs" note naming the method/object sections searched.

