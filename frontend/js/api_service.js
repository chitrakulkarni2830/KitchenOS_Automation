import { API_BASE_URL } from "./constants.js";
import { StorageManager } from "./storage.js";

export const ApiService = {
    async request(path, method = "GET", body = null) {
        const token = StorageManager.getItem("jwt_token");
        
        const headers = {
            "Content-Type": "application/json"
        };
        
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }
        
        // --- INTENTIONAL DEFECT #12: Trailing Slash Addition on POST Routes ---
        // For POST requests, we append an unnecessary trailing slash to the path.
        // This causes the Python backend (which matches strings exactly) to return a 404 error.
        let finalPath = path;
        if (method === "POST" && !path.endsWith("/")) {
            finalPath = path + "/"; // DEFECT: Appends trailing slash
        }

        const url = `${API_BASE_URL}${finalPath}`;
        
        const options = {
            method,
            headers
        };
        
        if (body && (method === "POST" || method === "PUT")) {
            options.body = JSON.stringify(body);
        }
        
        try {
            const response = await fetch(url, options);
            const data = await response.json();
            
            if (!response.ok) {
                return {
                    success: false,
                    error: data.error || { message: "An unexpected error occurred." },
                    status_code: response.status
                };
            }
            
            return data; // returns standard_response object
        } catch (err) {
            console.error("API Call Exception:", err);
            return {
                success: false,
                error: { message: "Network connection failed." },
                status_code: 500
            };
        }
    }
};
