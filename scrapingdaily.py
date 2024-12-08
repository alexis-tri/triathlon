import os
import sqlite3
from difflib import SequenceMatcher
from scraping.scrap import scrap_events

def is_similar(existing_name, new_name, threshold=0.8):
    """
    Compare two names using SequenceMatcher and return True if similarity exceeds the threshold.
    """
    return SequenceMatcher(None, existing_name, new_name).ratio() > threshold

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def find_similar_race(conn, name, place, date, distance=None, threshold=0.8):
    """
    Check if a similar race exists in the database based on name, place, date, and optionally distance.
    """
    cursor = conn.execute('SELECT * FROM courses')
    races = cursor.fetchall()

    for race in races:
        # Handle None or missing values gracefully
        db_name = race["name"] or ""
        db_place = race["place"] or ""
        db_date = race["date"]
        db_distance = str(race["distance"] or "")  # Normalize distance to string

        # Normalize scraped distance to string for comparison
        distance = str(distance or "")

        # Step 1: Compare name and place (fuzzy match) and date (exact match)
        if (
            is_similar(db_name, name, threshold) and
            is_similar(db_place, place, threshold) and
            db_date == date
        ):
            # Step 2: Handle distance comparison only if both are non-empty
            if not db_distance or not distance or db_distance == distance:
                # If distance matches or is irrelevant, consider it a match
                return race

    return None  # No similar race found

if __name__ == "__main__":
    # Scrape new race data
    scraped_races = scrap_events()

    conn = get_db_connection()

    for race in scraped_races:
        name = race[0] or ""  # Default to empty string if None
        place = race[1] or ""
        date = race[2] or ""
        distance = str(race[3] or "")  # Convert to string

        # Ensure data is valid before proceeding
        if not name or not place or not date:
            print(f"Invalid race data skipped: {race}")
            continue

        # Check if a similar race exists in the database
        existing_race = find_similar_race(conn, name, place, date, distance)

        if existing_race:
            # Update distance if it's different or previously missing
            if str(existing_race["distance"] or "") != distance:
                conn.execute(
                    'UPDATE courses SET distance = ? WHERE id = ?',
                    (distance, existing_race["id"])
                )
                print(f"Updated race: {name} - Distance updated to {distance}")
            else:
                print(f"Race already exists: {name} (no changes needed)")
        else:
            # Insert new race if no similar race is found
            conn.execute(
                'INSERT INTO courses (name, place, date, distance) VALUES (?, ?, ?, ?)',
                (name, place, date, distance)
            )
            print(f"Inserted new race: {name}")

    conn.commit()
    conn.close()