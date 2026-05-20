# Calendar Sync

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{JURISDICTION_TIMEZONE}}: e.g. "Europe/London", "Europe/Brussels", "Asia/Singapore"
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  No other jurisdiction-specific tokens in this skill.
-->

ICS feed sync to iPhone Calendar / Google Calendar / Outlook — no third-party API, no data processor. Code-aliased summary line (lock-screen safe). Full matter detail in event body.

## ICS Feed Generation

The Calendar Sync generates `.ics` files at `~/.ailawfirm_{{COUNTRY_LOWER}}/calendars/`:

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AI Law Firm {{COUNTRY_LOWER}}//EN
BEGIN:VEVENT
DTSTART:20260609T090000Z
DTEND:20260609T100000Z
SUMMARY:<alias code> — <court abbreviation>
DESCRIPTION:<full matter detail — not visible on lock screen>
LOCATION:<court name>
END:VEVENT
END:VCALENDAR
```

## Alias System

Lock-screen event summaries use code aliases — no client names leak to phone notifications:
- Summary line format: `<matter_alias> — <court_abbreviation> — <hearing_type>`
- Full client + matter details in event body (visible on tap/click, not on lock screen)

## Operations

- **add_hearing**: Add a hearing event → generates/updates the ICS feed
- **add_deadline**: Add a filing deadline → generates ICS event with reminder
- **sync**: Regenerate the ICS file from all active matters' hearings and deadlines
- **subscribe**: Print the ICS feed path for manual subscription in iPhone/Google/Outlook
- **list_upcoming**: Return all events in the next N days

## Timezone

All events rendered in `{{JURISDICTION_TIMEZONE}}`. DST transitions handled per the IANA timezone database.

## No Third-Party API

- No Google Calendar API — Google never sees your calendar data
- No Outlook API — Microsoft never sees your calendar data
- No iCloud API — Apple never sees your calendar data
- ICS is a local file — you subscribe to it; the file stays on your machine

## Storage

ICS files at `~/.ailawfirm_{{COUNTRY_LOWER}}/calendars/`. Local only. Never transmitted. Never synced to third-party cloud.
