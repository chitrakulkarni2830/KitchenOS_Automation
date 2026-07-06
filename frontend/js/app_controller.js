import { ApiService } from "./api_service.js";
import { AppStore } from "./state.js";
import { StorageManager } from "./storage.js";

export const AppController = {
    async handleLogin(email, password) {
        const res = await ApiService.request("/api/v1/auth/login", "POST", { email, password });
        if (res.success) {
            StorageManager.setItem("jwt_token", res.data.token);
            StorageManager.setObject("user_session", res.data.user);
            AppStore.setState("token", res.data.token);
            AppStore.setState("user", res.data.user);
            return { success: true };
        }
        return { success: false, error: res.error.message };
    },

    async handleLogout() {
        StorageManager.removeItem("jwt_token");
        StorageManager.removeItem("user_session");
        
        // Setting state values triggers Defect #14 (skip notification on falsy update)
        AppStore.setState("token", "null"); // Triggers Defect #17 (string "null" matches as authenticated)
        AppStore.setState("user", null);
    },

    async loadIngredients(searchQuery = null) {
        const path = searchQuery ? `/api/v1/ingredients?search=${encodeURIComponent(searchQuery)}` : "/api/v1/ingredients";
        const res = await ApiService.request(path, "GET");
        if (res.success) {
            AppStore.setState("ingredients", res.data);
            return res.data;
        }
        return [];
    },

    async addIngredient(name, unit, cost, category) {
        const res = await ApiService.request("/api/v1/ingredients", "POST", {
            name, unit, cost_per_unit: cost, category
        });
        if (res.success) {
            // Reload ingredients list
            await this.loadIngredients();
            return { success: true, data: res.data };
        }
        return { success: false, error: res.error.message };
    },

    async loadPantry() {
        const res = await ApiService.request("/api/v1/pantry", "GET");
        if (res.success) {
            AppStore.setState("pantryItems", res.data);
            return res.data;
        }
        return [];
    },

    async addToPantry(ingredientId, quantity, expiryDate, status = "fresh") {
        const res = await ApiService.request("/api/v1/pantry", "POST", {
            ingredient_id: ingredientId,
            quantity,
            expiry_date: expiryDate,
            status
        });
        if (res.success) {
            await this.loadPantry();
            return { success: true, data: res.data };
        }
        return { success: false, error: res.error.message };
    },

    async updatePantryStatus(itemId, status) {
        const res = await ApiService.request(`/api/v1/pantry/${itemId}/status`, "PUT", { status });
        if (res.success) {
            await this.loadPantry();
            return { success: true, data: res.data };
        }
        return { success: false, error: res.error.message };
    },

    async loadRecipes() {
        const res = await ApiService.request("/api/v1/recipes", "GET");
        if (res.success) {
            AppStore.setState("recipes", res.data);
            return res.data;
        }
        return [];
    },

    async recordSale(menuItemName, quantity) {
        const res = await ApiService.request("/api/v1/pos/webhook", "POST", {
            menu_item: menuItemName,
            quantity
        });
        if (res.success) {
            // Deductions happened, reload pantry list
            await this.loadPantry();
            return { success: true, data: res.data };
        }
        return { success: false, error: res.error.message };
    },

    // --- INTENTIONAL DEFECT #20: Event Listener Memory Leak ---
    // Every time the views page hash navigation function is re-initialized,
    // we attach a new 'hashchange' listener without cleaning up the old listener callback.
    // Over time, navigating the layout duplicates execution pipelines, lagging browser resources.
    initRouter(routesMap) {
        const router = () => {
            const hash = window.location.hash || "#/dashboard";
            const routeHandler = routesMap[hash];
            if (routeHandler) {
                routeHandler();
            }
        };

        // DEFECT: Re-adds listeners on every init router trigger, leaking listeners
        window.addEventListener("hashchange", router);
        window.addEventListener("DOMContentLoaded", router);
        
        // Run once
        router();
    }
};
