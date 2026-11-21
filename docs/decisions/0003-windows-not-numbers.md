# 0003: Answer with time windows, not just numbers

**Status:** accepted, 0.1.0

## Context

People ask "when should I go", not "what is the PM2.5".

## Decision

Rank start times by the average forecast over the activity's duration, within 6:00 to 22:00, and show the worst time too.

## Tradeoff

- Hides some detail behind a recommendation
- The decision is on the screen in one look
