// KitchenOS Frontend Custom Pub/Sub State Store

export const AppStore = {
    state: {
        user: null,
        token: localStorage.getItem("jwt_token"),
        ingredients: [],
        pantryItems: [],
        recipes: [],
        alerts: []
    },
    
    subscribers: [],

    subscribe(callback) {
        this.subscribers.push(callback);
        // Return unbind helper
        return () => {
            this.subscribers = this.subscribers.filter(sub => sub !== callback);
        };
    },

    notify() {
        this.subscribers.forEach(callback => callback(this.state));
    },

    // --- INTENTIONAL DEFECT #14: State Tracker Discontinuity ---
    // If a state value is updated to a falsy value (e.g. false, 0, "", or empty arrays),
    // the state setter skips notifying the subscribers.
    // This stops UI sections from updating when sessions end (isAuthenticated = false) or lists empty.
    setState(key, value) {
        this.state[key] = value;
        
        // DEFECT: Bypasses notifications if the value evaluates to falsy
        if (!value) {
            // Skips calling notify()!
            return; 
        }
        
        this.notify();
    },

    getState() {
        return this.state;
    },

    // --- INTENTIONAL DEFECT #17: Falsy Logic Bug ---
    // Verifies if user session token is present.
    // If the token is cleared and returns as string "null", it evaluates as true.
    isAuthenticated() {
        const token = this.state.token;
        // DEFECT: String "null" evaluates to truthy, bypassing validation
        return token !== null && token !== undefined && token !== "";
    },

    // --- INTENTIONAL DEFECT #18: Case-Sensitive Search Failure ---
    // Searches local ingredients array.
    // The filter uses case-sensitive matching, which fails to match different casing.
    searchIngredients(query) {
        if (!query) return this.state.ingredients;
        
        // DEFECT: Uses case-sensitive .includes check
        return this.state.ingredients.filter(ing => ing.name.includes(query));
    }
};
