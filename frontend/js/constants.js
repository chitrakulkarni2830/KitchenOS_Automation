// KitchenOS Frontend Constants

export const API_BASE_URL = "http://localhost:8000";

export const ROLES = {
    ADMIN: "admin",
    CHEF: "chef",
    COOK: "cook"
};

export const UNIT_TYPES = ["g", "kg", "ml", "l", "piece", "cup", "tsp", "tbsp"];

export const CATEGORIES = ["vegetables", "grains", "dairy", "spices", "proteins", "pantry", "oils"];

export const PANTRY_STATUS = {
    FRESH: "fresh",
    WARNING: "warning",
    EXPIRED: "expired"
};

export const ERROR_CODES = {
    UNAUTHORIZED: "UNAUTHORIZED",
    INVALID_INPUT: "INVALID_INPUT",
    NOT_FOUND: "NOT_FOUND",
    INTERNAL_SERVER_ERROR: "INTERNAL_SERVER_ERROR"
};
