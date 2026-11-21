# 0004: Label stations without hourly measurements

**Status:** accepted, 0.1.0

## Context

Several stations returned no hourly PM data on the first run.

## Decision

Mark them "forecast only" in the selector and say "model, no measurement" in the now card.

## Tradeoff

- Fewer stations look complete
- No model value is ever shown as a measurement
