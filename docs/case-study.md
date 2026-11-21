# Case study: Smog Planner

## The question

In Kraków's heating season the question is not "is the air bad today" but "when in the next day is it least bad". Most air quality apps show a coloured dot for right now. I wanted an app that answers the planning question, shows the official measurements next to the forecast, and is honest about how good the forecast is at each station.

## Approach

I checked what the official API allows, found it cannot be read from a page, and built the smallest bridge: an hourly job writing JSON into the repo. The forecast comes from a public model that a page can read. The product is the planner on top: activity, duration, sensitivity, and the best and worst windows. Every value says whether it is a measurement or a model.

## Findings

### 1. The official API cannot be used from a web page (confirmed)

Browser requests to the GIOŚ API fail, while the same addresses open directly. Requests also failed with HTTP 406 until the Accept header allowed any type. Hence the hourly job.

### 2. Not every station publishes hourly PM data (confirmed)

On the first run, 4 of the 9 Kraków stations returned hourly PM2.5 or PM10, and only Aleja Krasińskiego returned both. The other sensors answered HTTP 400. The app labels those stations "forecast only".

### 3. How far the forecast model is from the stations (to measure)

The page shows the gap station by station. Findings across stations need a few weeks of history: [result].

## Decisions

### An hourly GitHub Action instead of a server

The GIOŚ API cannot be called from a browser page, and the portfolio runs on free static hosting.

**Decision:** A scheduled GitHub Action fetches the 9 stations every hour and commits JSON files the page reads.

Full record: [decisions/0001-github-action-bridge.md](decisions/0001-github-action-bridge.md)

### Show the measurement and the model side by side

A model forecast on a grid of several kilometres smooths local peaks, so it can be far from what a station measures.

**Decision:** Show both, compute the gap for the last two days per station, and let the user correct the forecast by the measured ratio, capped at 0.5 to 2.

Full record: [decisions/0002-measurement-and-model.md](decisions/0002-measurement-and-model.md)

### Answer with time windows, not just numbers

People ask "when should I go", not "what is the PM2.5".

**Decision:** Rank start times by the average forecast over the activity's duration, within 6:00 to 22:00, and show the worst time too.

Full record: [decisions/0003-windows-not-numbers.md](decisions/0003-windows-not-numbers.md)

### Label stations without hourly measurements

Several stations returned no hourly PM data on the first run.

**Decision:** Mark them "forecast only" in the selector and say "model, no measurement" in the now card.

Full record: [decisions/0004-label-missing-data.md](decisions/0004-label-missing-data.md)

## What I learned as a PM

- Public data constraints shape the architecture more than features do
- Being explicit about measurement versus model is the core of trust in an air quality app
- The first real run found data gaps that a mock would have hidden

## Limits

- Measurements up to an hour behind
- Some stations have no hourly PM data
- Forecast correction is a simple ratio

## What I would do next

1. After four weeks of history, publish the model gap per station and the real daily pattern
2. Add other Polish cities from the same API
3. A morning summary as an installable web app notification

## My role

I framed the problem, made the product calls, checked every number and wrote the conclusions. Claude (Anthropic) wrote the code with me. 
