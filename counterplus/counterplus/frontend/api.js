// Talks to the FastAPI backend. If BACKEND_URL (from config.js) is set,
// requests go to that deployed backend; otherwise they go to the same
// origin the frontend is served from (for local testing with one server).
const API_BASE = (typeof BACKEND_URL !== "undefined" && BACKEND_URL) ? `${BACKEND_URL}/api` : "/api";

function getToken() {
  return localStorage.getItem("counterplus_token");
}

function setToken(token) {
  localStorage.setItem("counterplus_token", token);
}

function clearToken() {
  localStorage.removeItem("counterplus_token");
}

async function apiRequest(path, { method = "GET", body = null, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getToken();
    if (!token) throw new Error("Not logged in");
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  let data = null;
  try {
    data = await res.json();
  } catch (_) {
    // no body
  }

  if (!res.ok) {
    const message = (data && data.detail) || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

const api = {
  getCaptcha: () => apiRequest("/auth/captcha"),
  register: (payload) => apiRequest("/auth/register", { method: "POST", body: payload }),
  login: (payload) => apiRequest("/auth/login", { method: "POST", body: payload }),
  me: () => apiRequest("/auth/me", { auth: true }),
  walletBalance: () => apiRequest("/wallet/balance", { auth: true }),
  walletTopup: (amount) => apiRequest("/wallet/topup", { method: "POST", body: { amount }, auth: true }),
  operators: () => apiRequest("/operators"),
  recharge: (payload) => apiRequest("/recharge", { method: "POST", body: payload, auth: true }),
  transactions: () => apiRequest("/transactions", { auth: true }),
};

function requireAuth() {
  if (!getToken()) {
    window.location.href = "login.html";
  }
}
