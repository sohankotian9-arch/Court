"""Tennis Match Tracker - Track all tennis matches with dates and reminders"""
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class TennisMatch:
    """Represents a single tennis match"""
    
    def __init__(self, tournament: str, date: str, time: str, player1: str, 
                 player2: str, location: str, match_type: str = "Singles",
                 reminder_days: int = 1):
        """
        Initialize a tennis match
        
        Args:
            tournament: Tournament name (e.g., "Australian Open")
            date: Match date in format YYYY-MM-DD
            time: Match time in format HH:MM
            player1: First player name
            player2: Second player name
            location: Match location/venue
            match_type: Type of match (Singles/Doubles/Mixed)
            reminder_days: Days before match to set reminder
        """
        self.tournament = tournament
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.time = time
        self.player1 = player1
        self.player2 = player2
        self.location = location
        self.match_type = match_type
        self.reminder_days = reminder_days
        self.id = self._generate_id()
        
    def _generate_id(self) -> str:
        """Generate unique ID for the match"""
        return f"{self.tournament}_{self.date}_{self.player1}_{self.player2}".replace(" ", "_")
    
    def get_reminder_date(self) -> datetime:
        """Get the reminder date/time"""
        match_datetime = datetime.combine(self.date, 
                                         datetime.strptime(self.time, "%H:%M").time())
        return match_datetime - timedelta(days=self.reminder_days)
    
    def is_upcoming(self) -> bool:
        """Check if match is upcoming"""
        return self.date >= datetime.now().date()
    
    def days_until_match(self) -> int:
        """Get number of days until match"""
        delta = self.date - datetime.now().date()
        return delta.days
    
    def to_dict(self) -> Dict:
        """Convert match to dictionary"""
        return {
            "tournament": self.tournament,
            "date": str(self.date),
            "time": self.time,
            "player1": self.player1,
            "player2": self.player2,
            "location": self.location,
            "match_type": self.match_type,
            "reminder_days": self.reminder_days,
            "id": self.id,
            "days_until": self.days_until_match() if self.is_upcoming() else None
        }
    
    def __str__(self) -> str:
        """String representation of match"""
        return (f"{self.tournament} - {self.date} {self.time}\n"
                f"{self.player1} vs {self.player2}\n"
                f"Location: {self.location} | Type: {self.match_type}")


class TennisMatchTracker:
    """Manages collection of tennis matches"""
    
    def __init__(self, data_file: str = "matches_2026.json"):
        """Initialize the tracker"""
        self.data_file = data_file
        self.matches: List[TennisMatch] = []
        self.load_matches()
    
    def add_match(self, match: TennisMatch) -> None:
        """Add a match to the tracker"""
        self.matches.append(match)
        self.save_matches()
    
    def remove_match(self, match_id: str) -> bool:
        """Remove a match by ID"""
        initial_count = len(self.matches)
        self.matches = [m for m in self.matches if m.id != match_id]
        if len(self.matches) < initial_count:
            self.save_matches()
            return True
        return False
    
    def get_upcoming_matches(self) -> List[TennisMatch]:
        """Get all upcoming matches sorted by date"""
        upcoming = [m for m in self.matches if m.is_upcoming()]
        return sorted(upcoming, key=lambda m: m.date)
    
    def get_matches_by_tournament(self, tournament: str) -> List[TennisMatch]:
        """Get all matches for a specific tournament"""
        return [m for m in self.matches if m.tournament.lower() == tournament.lower()]
    
    def get_matches_by_player(self, player: str) -> List[TennisMatch]:
        """Get all matches involving a specific player"""
        player_lower = player.lower()
        return [m for m in self.matches if player_lower in m.player1.lower() or 
                player_lower in m.player2.lower()]
    
    def get_today_matches(self) -> List[TennisMatch]:
        """Get matches scheduled for today"""
        today = datetime.now().date()
        return [m for m in self.matches if m.date == today]
    
    def get_matches_needing_reminder(self) -> List[TennisMatch]:
        """Get matches that need reminders (within reminder period)"""
        now = datetime.now()
        matches_to_remind = []
        
        for match in self.get_upcoming_matches():
            reminder_datetime = match.get_reminder_date()
            if now >= reminder_datetime and match.is_upcoming():
                matches_to_remind.append(match)
        
        return sorted(matches_to_remind, key=lambda m: m.date)
    
    def save_matches(self) -> None:
        """Save matches to JSON file"""
        data = [m.to_dict() for m in self.matches]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_matches(self) -> None:
        """Load matches from JSON file"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                for match_data in data:
                    match = TennisMatch(
                        tournament=match_data["tournament"],
                        date=match_data["date"],
                        time=match_data["time"],
                        player1=match_data["player1"],
                        player2=match_data["player2"],
                        location=match_data["location"],
                        match_type=match_data.get("match_type", "Singles"),
                        reminder_days=match_data.get("reminder_days", 1)
                    )
                    self.matches.append(match)
        except json.JSONDecodeError:
            print("Error loading matches file")
    
    def display_upcoming_matches(self) -> None:
        """Display all upcoming matches"""
        upcoming = self.get_upcoming_matches()
        if not upcoming:
            print("No upcoming matches found!")
            return
        
        print("\n" + "="*60)
        print("UPCOMING TENNIS MATCHES 2026")
        print("="*60)
        
        for i, match in enumerate(upcoming, 1):
            print(f"\n{i}. {match}")
            print(f"   Days until match: {match.days_until_match()}")
            print(f"   Reminder set for: {match.get_reminder_date().strftime('%Y-%m-%d %H:%M')}")
    
    def display_reminders(self) -> None:
        """Display matches needing reminders"""
        reminders = self.get_matches_needing_reminder()
        if not reminders:
            print("No reminders needed right now!")
            return
        
        print("\n" + "="*60)
        print("MATCH REMINDERS")
        print("="*60)
        
        for i, match in enumerate(reminders, 1):
            print(f"\n🔔 REMINDER #{i}")
            print(f"{match}")
            print(f"Match in {match.days_until_match()} days")
    
    def get_statistics(self) -> Dict:
        """Get match statistics"""
        upcoming = self.get_upcoming_matches()
        tournaments = set(m.tournament for m in self.matches)
        
        return {
            "total_matches": len(self.matches),
            "upcoming_matches": len(upcoming),
            "total_tournaments": len(tournaments),
            "tournaments": sorted(list(tournaments))
        }


if __name__ == "__main__":
    # Example usage
    tracker = TennisMatchTracker()
    
    # Display menu
    while True:
        print("\n" + "="*60)
        print("TENNIS MATCH TRACKER")
        print("="*60)
        print("1. View all upcoming matches")
        print("2. View reminders")
        print("3. Add new match")
        print("4. Search by player")
        print("5. Search by tournament")
        print("6. View statistics")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            tracker.display_upcoming_matches()
        
        elif choice == "2":
            tracker.display_reminders()
        
        elif choice == "3":
            tournament = input("Tournament name: ")
            date = input("Date (YYYY-MM-DD): ")
            time = input("Time (HH:MM): ")
            player1 = input("Player 1: ")
            player2 = input("Player 2: ")
            location = input("Location: ")
            match_type = input("Match type (Singles/Doubles/Mixed) [Singles]: ") or "Singles"
            reminder_days = int(input("Reminder days before match [1]: ") or "1")
            
            match = TennisMatch(tournament, date, time, player1, player2, location, match_type, reminder_days)
            tracker.add_match(match)
            print(f"✓ Match added successfully!")
        
        elif choice == "4":
            player = input("Enter player name: ")
            matches = tracker.get_matches_by_player(player)
            if matches:
                print(f"\nMatches for {player}:")
                for match in sorted(matches, key=lambda m: m.date):
                    print(f"  • {match.date} {match.time} - {match.player1} vs {match.player2}")
            else:
                print(f"No matches found for {player}")
        
        elif choice == "5":
            tournament = input("Enter tournament name: ")
            matches = tracker.get_matches_by_tournament(tournament)
            if matches:
                print(f"\nMatches in {tournament}:")
                for match in sorted(matches, key=lambda m: m.date):
                    print(f"  • {match.date} {match.time} - {match.player1} vs {match.player2}")
            else:
                print(f"No matches found for {tournament}")
        
        elif choice == "6":
            stats = tracker.get_statistics()
            print("\n" + "="*60)
            print("STATISTICS")
            print("="*60)
            print(f"Total matches: {stats['total_matches']}")
            print(f"Upcoming matches: {stats['upcoming_matches']}")
            print(f"Total tournaments: {stats['total_tournaments']}")
            print(f"Tournaments: {', '.join(stats['tournaments'])}")
        
        elif choice == "7":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")
