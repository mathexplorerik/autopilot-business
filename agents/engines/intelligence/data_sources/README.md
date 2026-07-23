# Data Sources — Market Intelligence Layer

## Purpose

This folder is the **single, canonical abstraction layer** for
market-data used by `TrendEngine` and every intelligence module
built on top of it (Pricing, Bestseller, Competitor, Portfolio,
Dashboard, etc.). Any code that needs demand/competition/profit/
evergreen/seasonal/marketplace signals for a niche should go
through `BaseMarketDataSource` — never invent a new, parallel
data-source abstraction.

**This project previously accumulated two unwired, duplicate
plugin architectures (`data_sources`/`plugins` zip-import, and
`research_v2`/`BaseResearchPlugin`) before consolidating here.
Do not repeat that mistake — see "Architecture Note" below.**

## `BaseMarketDataSource`

The abstract interface every data source implements
(`base_market_data_source.py`). Six required methods, each
returning a 0-100 int:

```python
demand(niche: str) -> int
competition(niche: str) -> int
profit(niche: str) -> int
evergreen(niche: str) -> int
seasonal(niche: str) -> int
marketplace(book_type: str) -> int
```

Plus a `source_name` property for logging/debugging.

`TrendEngine` depends ONLY on this interface
(`agents/engines/trend_engine/trend_engine.py`), never on a
specific implementation:

```python
class TrendEngine:
    def __init__(self, data_source: BaseMarketDataSource = None):
        self.data_source = data_source or HeuristicMarketDataSource()
```

## How to add a new data source

1. Create a new file in this folder: `your_source_market_data_source.py`
2. Subclass `BaseMarketDataSource`, implement all 6 methods
3. **Fallback policy (mandatory):** for any field your source has
   no genuine real signal for, delegate to a fallback source
   (usually `HeuristicMarketDataSource`) rather than fabricating a
   number that looks real but isn't. See
   `google_books_market_data_source.py` for the reference pattern —
   it has a real signal for `competition`/`demand`, and honestly
   defers `profit`/`evergreen`/`seasonal`/`marketplace` to the
   heuristic fallback.
4. **Never raise for a failed network call** — catch the exception
   and fall back to the heuristic source instead. `TrendEngine`
   expects a plain int back from every method, always.
5. Add a standalone test (see Testing below) BEFORE wiring it into
   `TrendEngine` — verify it works in isolation first.
6. Only once standalone-tested: wire it in by constructing
   `TrendEngine(data_source=YourNewSource())` wherever `TrendEngine`
   is created.

## Fallback policy

Every method must return an int, always — never `None`, never raise.
- If your source has a real signal: compute and return it.
- If your source has no real signal for that field: call the
  fallback source's method for that field.
- If your source's real signal call fails (network error, rate
  limit, timeout): catch the exception, call the fallback source.

`HeuristicMarketDataSource` (the JSON/analyzer-backed default) is
always a safe fallback choice — it has no external dependencies and
always succeeds.

## Testing requirements

Before wiring a new source into `TrendEngine`:
- Test every method standalone, confirming it returns a valid 0-100 int
- Test what happens when your source's real API/data call fails —
  confirm it falls back gracefully, doesn't raise
- Run `python3 tests/run_all.py` after wiring — confirm 6/6 still passes

## Architecture note — read before adding anything here

**Do not create a parallel plugin framework.** If you're about to
write a new abstract base class, a new "ResearchResult" dataclass,
or a new "PluginManager" — stop. That almost certainly already
exists here as `BaseMarketDataSource`. Extend it, don't duplicate it.

If a genuinely different DATA CATEGORY is needed later (e.g. author
metadata, review sentiment, pricing history, social signals — not
just niche demand/competition), that may justify a new,
domain-specific interface alongside this one. That's a deliberate
future decision, not a default — until that need is concrete, every
new market-data source implements `BaseMarketDataSource`.

## Current sources

| File | Real signal for | Falls back for |
|---|---|---|
| `heuristic_market_data_source.py` | everything (JSON/analyzer-backed) | n/a (this IS the fallback) |
| `google_books_market_data_source.py` | competition, demand (when rating data available) | profit, evergreen, seasonal, marketplace, and demand/competition on request failure |

`google_books_market_data_source.py` is built and tested but **not
yet wired into `TrendEngine`** — Google's unauthenticated API quota
is rate-limited (HTTP 429 observed in testing within ~1 request).
Wiring it in requires either accepting frequent fallback-to-heuristic
behavior, or obtaining a free Google API key to raise the quota.
