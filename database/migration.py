import os
import sqlite3
import sys

# Ensure backend directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database.db_manager import DatabaseManager
from backend.utils.helpers import hash_password

def seed_database():
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        # Check if database is already seeded
        cursor.execute("SELECT COUNT(*) FROM users;")
        if cursor.fetchone()[0] > 0:
            print("Database already seeded. Skipping seeder.")
            return

        # Seed Users
        users = [
            ("admin@kitchenos.com", hash_password("AdminPass123"), "admin"),
            ("chef@kitchenos.com", hash_password("ChefPass123"), "chef"),
            ("cook@kitchenos.com", hash_password("CookPass123"), "cook")
        ]
        cursor.executemany(
            "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?);",
            users
        )

        # Seed Ingredients (Indian Kitchen focus)
        ingredients = [
            ("Basmati Rice", "kg", 120.0, "grains"),
            ("Toor Dal", "kg", 150.0, "grains"),
            ("Mustard Oil", "l", 180.0, "oils"),
            ("Ghee", "kg", 650.0, "dairy"),
            ("Turmeric Powder", "g", 0.40, "spices"), # 400 per kg
            ("Cumin Seeds", "g", 0.60, "spices"),
            ("Onion", "kg", 40.0, "vegetables"),
            ("Tomato", "kg", 60.0, "vegetables"),
            ("Ginger", "g", 0.15, "vegetables"),
            ("Paneer", "kg", 450.0, "dairy"),
            ("Chicken Breast", "kg", 280.0, "proteins"),
            ("Wheat Flour", "kg", 45.0, "grains")
        ]
        cursor.executemany(
            "INSERT INTO ingredients (name, unit, cost_per_unit, category) VALUES (?, ?, ?, ?);",
            ingredients
        )

        # Seed Pantry Items
        pantry_items = [
            (1, 5.0, "2026-12-31", "fresh"), # 5 kg Basmati Rice
            (2, 2.0, "2026-10-15", "fresh"), # 2 kg Toor Dal
            (4, 1.0, "2026-09-30", "fresh"), # 1 kg Ghee
            (7, 3.5, "2026-07-20", "warning"), # 3.5 kg Onion (short shelf life)
            (8, 0.2, "2026-07-05", "expired") # 0.2 kg Tomato (already expired based on 2026-07-06 current time)
        ]
        cursor.executemany(
            "INSERT INTO pantry_items (ingredient_id, quantity, expiry_date, status) VALUES (?, ?, ?, ?);",
            pantry_items
        )

        # Seed Recipes
        # Recipe 1: Jeera Rice
        cursor.execute(
            "INSERT INTO recipes (name, servings, prep_time, instructions) VALUES (?, ?, ?, ?);",
            ("Jeera Rice", 4, 25, "1. Wash rice. 2. Heat ghee in a pan. 3. Add cumin seeds. 4. Add rice and water. 5. Cook until soft.")
        )
        recipe_id = cursor.lastrowid

        # Recipe ingredients mappings
        recipe_ingredients = [
            (recipe_id, 1, 0.4),  # 0.4 kg Basmati Rice
            (recipe_id, 4, 0.05), # 0.05 kg Ghee
            (recipe_id, 6, 10.0)  # 10 g Cumin Seeds
        ]
        cursor.executemany(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?);",
            recipe_ingredients
        )

        conn.commit()
        print("Database seeded successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error seeding database: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_database()
