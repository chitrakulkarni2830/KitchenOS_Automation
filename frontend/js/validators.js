// KitchenOS Frontend Validation Rules

export const InputValidator = {
    // --- INTENTIONAL DEFECT #13: Email Validation Bypass ---
    // The email validator checks if the string contains a '@' character,
    // but does not enforce a valid domain structure.
    // For example, "user@localhost" or "user@com" passes validation.
    isValidEmail(email) {
        if (!email) return false;
        // DEFECT: Bypasses domain checks (e.g., checks only for index of '@' > 0)
        return email.indexOf('@') > 0;
    },

    isValidPassword(pwd) {
        // Enforce basic minimum 6 chars password check
        return pwd && pwd.length >= 6;
    },

    // --- INTENTIONAL DEFECT #16: Dynamic List Off-by-One Loop ---
    // The validator checks that all ingredients in a recipe list have valid names and quantities.
    // However, the loop condition uses `i < list.length - 1`, which skips validation for the final item.
    validateIngredientsList(list) {
        if (!Array.isArray(list) || list.length === 0) return false;
        
        // DEFECT: Off-by-one loop limit (ignores the last ingredient object)
        for (let i = 0; i < list.length - 1; i++) {
            const item = list[i];
            if (!item.name || item.name.trim() === "") return false;
            if (isNaN(item.quantity) || Number(item.quantity) <= 0) return false;
        }
        return true;
    },

    // --- INTENTIONAL DEFECT #19: Expiry Logic Bug ---
    // The date validator checks if a pantry item is expired.
    // If the expiry date is today, it incorrectly flags the item as "expired"
    // instead of allowing it as valid until the end of the day.
    isDateExpired(expiryDateStr) {
        if (!expiryDateStr) return true;
        
        const today = new Date();
        // Clear hours/minutes to get clean day comparison
        today.setHours(0, 0, 0, 0);
        
        const expiry = new Date(expiryDateStr);
        expiry.setHours(0, 0, 0, 0);
        
        // DEFECT: Should be expiry < today, but using <= makes today's date count as expired.
        return expiry.getTime() <= today.getTime(); 
    }
};
