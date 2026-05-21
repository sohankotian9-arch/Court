# Tennis Court - Match Tracker 🎾

A comprehensive tennis match tracking application that helps you keep track of all tennis matches throughout the year with dates, times, and automated reminders.

## Features

✅ **Track All Matches** - Add and manage tennis matches from major tournaments  
✅ **Smart Reminders** - Get notified before matches (customizable reminder periods)  
✅ **Search Functionality** - Find matches by player, tournament, or date  
✅ **Match Statistics** - View tournament and match statistics  
✅ **Persistent Storage** - All matches saved to JSON for easy backup  
✅ **Multiple Match Types** - Support for Singles, Doubles, and Mixed matches  

## Installation

```bash
# Clone the repository
git clone https://github.com/sohankotian9-arch/Court.git
cd Court

# No external dependencies required!
# Just Python 3.7+
```

## Quick Start

### Run the Interactive Menu

```bash
python tennis_matches.py
```

This will open an interactive menu with options to:
1. View upcoming matches
2. Check reminders
3. Add new matches
4. Search by player
5. Search by tournament
6. View statistics

### Using as a Library

```python
from tennis_matches import TennisMatchTracker, TennisMatch

# Initialize tracker
tracker = TennisMatchTracker()

# Add a match
match = TennisMatch(
    tournament="Wimbledon",
    date="2026-07-06",
    time="13:00",
    player1="Jannik Sinner",
    player2="Novak Djokovic",
    location="London, England",
    match_type="Singles",
    reminder_days=2
)
tracker.add_match(match)

# Get upcoming matches
upcoming = tracker.get_upcoming_matches()

# Get matches needing reminders
reminders = tracker.get_matches_needing_reminder()

# Search by player
matches = tracker.get_matches_by_player("Jannik Sinner")

# Search by tournament
matches = tracker.get_matches_by_tournament("Wimbledon")

# Get statistics
stats = tracker.get_statistics()
```

## 2026 Major Tournaments

The sample data includes matches from:

- **Australian Open** - January 19-24
- **French Open** - May 24 - June 4
- **Wimbledon** - July 6-11
- **US Open** - August 31 - September 12

## Data Format

Matches are stored in `matches_2026.json`:

```json
{
  "tournament": "Wimbledon",
  "date": "2026-07-06",
  "time": "13:00",
  "player1": "Jannik Sinner",
  "player2": "Novak Djokovic",
  "location": "London, England",
  "match_type": "Singles",
  "reminder_days": 2,
  "id": "Wimbledon_2026-07-06_Jannik_Sinner_Novak_Djokovic"
}
```

## Usage Examples

### Example 1: Track Djokovic's Matches

```python
tracker = TennisMatchTracker()
djokovic_matches = tracker.get_matches_by_player("Djokovic")
for match in djokovic_matches:
    print(f"{match.date}: {match.player1} vs {match.player2}")
```

### Example 2: Get Today's Matches

```python
today_matches = tracker.get_today_matches()
print(f"Today's matches: {len(today_matches)}")
for match in today_matches:
    print(f"{match.time} - {match.player1} vs {match.player2}")
```

### Example 3: Check Reminders

```python
tracker = TennisMatchTracker()
reminders = tracker.get_matches_needing_reminder()
for match in reminders:
    print(f"🔔 {match.tournament}: {match.player1} vs {match.player2}")
    print(f"   In {match.days_until_match()} days")
```

### Example 4: Filter by Tournament

```python
wimbledon_matches = tracker.get_matches_by_tournament("Wimbledon")
print(f"Wimbledon matches: {len(wimbledon_matches)}")
for match in wimbledon_matches:
    print(f"{match.date}: {match.player1} vs {match.player2}")
```

## Class Reference

### TennisMatch

**Constructor:**
```python
TennisMatch(tournament, date, time, player1, player2, location, match_type="Singles", reminder_days=1)
```

**Methods:**
- `get_reminder_date()` - Returns reminder datetime
- `is_upcoming()` - Check if match is in the future
- `days_until_match()` - Get days until match
- `to_dict()` - Convert to dictionary

### TennisMatchTracker

**Constructor:**
```python
TennisMatchTracker(data_file="matches_2026.json")
```

**Methods:**
- `add_match(match)` - Add a new match
- `remove_match(match_id)` - Remove a match by ID
- `get_upcoming_matches()` - Get all upcoming matches
- `get_matches_by_tournament(tournament)` - Filter by tournament
- `get_matches_by_player(player)` - Filter by player
- `get_today_matches()` - Get today's matches
- `get_matches_needing_reminder()` - Get matches needing reminders
- `get_statistics()` - Get summary statistics
- `save_matches()` - Save to JSON file
- `load_matches()` - Load from JSON file
- `display_upcoming_matches()` - Print upcoming matches
- `display_reminders()` - Print reminder matches

## Sample Data

The repository includes sample data for major 2026 tournaments:
- 8 premium matches from Australian Open, French Open, Wimbledon, and US Open
- Real player matchups
- Venue information
- Customizable reminder periods

## Future Enhancements

- 📧 Email/SMS reminders integration
- 📱 Mobile app companion
- 🏆 Tournament standings and seeding
- 🎯 Favorite players tracking
- 📊 Advanced analytics and predictions
- 🔄 Auto-sync with official tournament calendars
- 🌐 Web interface

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Add new tournaments
- Implement reminder systems
- Add web UI
- Suggest features

---

**Made for tennis enthusiasts by tennis enthusiasts** 🎾
