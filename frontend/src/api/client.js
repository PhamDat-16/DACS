/**
 * API Client for Smart Parking System Backend (FastAPI)
 */
const BASE_URL =
  typeof window !== "undefined" && window.location.port === "3000"
    ? "http://localhost:8000"
    : "";

export class ParkingApi {
  static getToken() {
    return localStorage.getItem("sps_token") || "";
  }

  static setToken(token) {
    localStorage.setItem("sps_token", token);
  }

  static clearToken() {
    localStorage.removeItem("sps_token");
  }

  static async request(endpoint, options = {}) {
    const url = `${BASE_URL}${endpoint}`;
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, { ...options, headers });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Lỗi HTTP ${response.status}`);
      }
      return await response.json();
    } catch (err) {
      console.warn(`[API] Gọi ${endpoint} thất bại:`, err.message);
      throw err;
    }
  }

  // Health
  static checkHealth() {
    return this.request("/api/health");
  }

  // Auth
  static login(email, password) {
    return this.request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  }

  static register(data) {
    return this.request("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  static getCurrentUser() {
    return this.request("/api/users/me");
  }

  // Lots & Slots
  static getLots() {
    return this.request("/api/lots");
  }

  static getLotDetail(lotId) {
    return this.request(`/api/lots/${lotId}`);
  }

  static getAvailableSlotsCount(lotId) {
    return this.request(`/api/lots/${lotId}/available-slots`);
  }

  // A* Navigation
  static getNavigationPath(lotId, slotId, fromX = 0, fromY = 0) {
    return this.request(
      `/api/lots/${lotId}/navigate?slot_id=${slotId}&from_x=${fromX}&from_y=${fromY}`,
    );
  }

  // Bookings
  static createBooking(data) {
    return this.request("/api/bookings", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  static getMyBookings() {
    return this.request("/api/bookings/my");
  }

  // ML Predictions
  static predictDay(dateStr, isHoliday = false) {
    return this.request(
      `/api/predict-occupancy/day?date=${dateStr}&is_holiday=${isHoliday}`,
    );
  }

  static predictSingleHour(dateStr, hour, isHoliday = false) {
    return this.request(
      `/api/predict-occupancy?date=${dateStr}&hour_of_day=${hour}&is_holiday=${isHoliday}`,
    );
  }

  // Vehicles (5-table schema)
  static getVehicles(plate = "") {
    const q = plate ? `?license_plate=${encodeURIComponent(plate)}` : "";
    return this.request(`/api/vehicles${q}`);
  }

  static createVehicle(data) {
    return this.request("/api/vehicles", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  static getVehicleByPlate(plate) {
    return this.request(`/api/vehicles/${encodeURIComponent(plate)}`);
  }

  // Parking Sessions
  static getSessions(status = "") {
    const q = status ? `?status=${encodeURIComponent(status)}` : "";
    return this.request(`/api/sessions${q}`);
  }

  static getActiveSessions() {
    return this.request("/api/sessions/active");
  }

  static checkIn(data) {
    return this.request("/api/sessions/check-in", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  static checkOut(data) {
    return this.request("/api/sessions/check-out", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }
}
