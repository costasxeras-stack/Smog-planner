# 0002: Show the measurement and the model side by side

**Status:** accepted, 0.1.0

## Context

A model forecast on a grid of several kilometres smooths local peaks, so it can be far from what a station measures.

## Decision

Show both, compute the gap for the last two days per station, and let the user correct the forecast by the measured ratio, capped at 0.5 to 2.

## Tradeoff

- A simple ratio does not fix timing errors
- The user sees how much to trust the forecast
