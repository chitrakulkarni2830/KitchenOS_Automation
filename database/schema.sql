-- KitchenOS SQLite Database Schema

-- Enable Foreign Key constraints
PRAGMA foreign_keys = ON;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'chef', 'cook')),
    created_at TEXT DEFAULT (datetime('now', 'utc'))
);

-- Ingredients Catalog Table
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    unit TEXT NOT NULL CHECK(unit IN ('g', 'kg', 'ml', 'l', 'piece', 'cup', 'tsp', 'tbsp')),
    cost_per_unit REAL NOT NULL CHECK(cost_per_unit >= 0),
    category TEXT NOT NULL CHECK(category IN ('vegetables', 'grains', 'dairy', 'spices', 'proteins', 'pantry', 'oils')),
    created_at TEXT DEFAULT (datetime('now', 'utc'))
);

-- Pantry Inventory Table
CREATE TABLE IF NOT EXISTS pantry_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    expiry_date TEXT NOT NULL, -- YYYY-MM-DD format
    status TEXT NOT NULL CHECK(status IN ('fresh', 'warning', 'expired')),
    created_at TEXT DEFAULT (datetime('now', 'utc')),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
);

-- Recipes Table
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    servings INTEGER NOT NULL CHECK(servings > 0),
    prep_time INTEGER NOT NULL CHECK(prep_time > 0), -- in minutes
    instructions TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now', 'utc'))
);

-- Recipe Ingredients Mapping Table
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK(quantity > 0),
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
);

-- Indexing for Query Optimization
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_ingredients_name ON ingredients(name);
CREATE INDEX IF NOT EXISTS idx_pantry_ingredient ON pantry_items(ingredient_id);
CREATE INDEX IF NOT EXISTS idx_recipe_name ON recipes(name);
CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_map ON recipe_ingredients(recipe_id, ingredient_id);
