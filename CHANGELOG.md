# Changelog

All notable changes to this project. Versions follow [docs/versioning.md](docs/versioning.md).

## [0.1.0] - 2026-11-21

First release.

### Added
- Now: latest measured PM2.5 and PM10 at the chosen station, coloured by the official Polish air quality index, with the time of the measurement
- Planner: the three best start times in the next 36 hours (6:00 to 22:00) for a run, a walk with a child, a bike ride or airing the flat, and the time to avoid. A "sensitive" setting raises the bar
- Chart: two days of measurements and model, three days of forecast, with index bands in the background
- Model check: how far the forecast model was from the station in the last two days, and an optional correction by the measured ratio (limited to 0.5 to 2)
- Daily pattern: average PM2.5 by hour of day from the collected history (grows hourly, kept for 60 days)
- Nearest station by location, and a label on stations without hourly measurements
- Hourly data job: a GitHub Action copies GIOŚ measurements for 9 Kraków stations into the repo, because the GIOŚ API cannot be read from a browser page
- Polish interface
