# 0001: An hourly GitHub Action instead of a server

**Status:** accepted, 0.1.0

## Context

The GIOŚ API cannot be called from a browser page, and the portfolio runs on free static hosting.

## Decision

A scheduled GitHub Action fetches the 9 stations every hour and commits JSON files the page reads.

## Tradeoff

- Data can be up to an hour behind
- No server, no cost, and the history is versioned in git
