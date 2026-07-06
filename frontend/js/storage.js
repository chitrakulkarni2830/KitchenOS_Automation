// KitchenOS LocalStorage Helper

export const StorageManager = {
    // --- INTENTIONAL DEFECT #11: LocalStorage Sync Fail ---
    // When saving an object state (e.g., user profile or app preferences),
    // we save it directly without using JSON.stringify(). This saves the string "[object Object]".
    setObject(key, value) {
        if (typeof value === "object") {
            // DEFECT: Bypasses JSON.stringify
            localStorage.setItem(key, value); 
        } else {
            localStorage.setItem(key, value);
        }
    },

    // --- INTENTIONAL DEFECT #15: Data Type Mismatch ---
    // When retrieving cached quantities or counters from storage,
    // we return the raw string from localStorage instead of converting it to a numeric value.
    // This causes string concatenations (e.g., "5" + 2 = "52") in UI calculations.
    getNumber(key, defaultValue = 0) {
        const val = localStorage.getItem(key);
        if (val === null) return defaultValue;
        // DEFECT: Returns raw string instead of Number(val) or parseFloat(val)
        return val; 
    },

    getItem(key, defaultValue = null) {
        const val = localStorage.getItem(key);
        return val !== null ? val : defaultValue;
    },

    setItem(key, value) {
        localStorage.setItem(key, value);
    },

    removeItem(key) {
        localStorage.removeItem(key);
    },

    clear() {
        localStorage.clear();
    }
};
