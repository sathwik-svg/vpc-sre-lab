/* VPC frontend. API responses are rendered with textContent, never innerHTML. */
(() => {
  "use strict";
  // Same-origin by default. Configure window.VPC_API_BASE before this script only
  // when the API origin is reachable and has an explicit, restrictive CORS policy.
  const API_BASE = (window.VPC_API_BASE || "").replace(/\\/+$/, "");
  const $ = id => document.getElementById(id);
  async function fetchText(path, timeoutMs = 4500) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetch(`${API_BASE}${path}`, {
        method: "GET", headers: { Accept: "application/json, text/plain;q=0.9" },
        cache: "no-store", signal: controller.signal
      });
      const body = await response.text();
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return body;
    } finally { clearTimeout(timeout); }
  }
  async function fetchJson(path) {
    try { return JSON.parse(await fetchText(path)); }
    catch (error) { throw error instanceof SyntaxError ? new Error("Invalid JSON response") : error; }
  }
  function text(id, value) { if ($(id)) $(id).textContent = String(value); }
  function status(id, label, kind = "") {
    if (!$(id)) return;
    $(id).textContent = label;
    $(id).classList.remove("ok", "error");
    if (kind) $(id).classList.add(kind);
  }
  function parseMetrics(raw) {
    const requestMatch = raw.match(/^vpc_http_requests_total(?:\\{[^}]*\\})?\\s+([0-9.eE+-]+)/m);
    const sumMatch = raw.match(/^vpc_http_request_duration_seconds_sum(?:\\{[^}]*\\})?\\s+([0-9.eE+-]+)/m);
    const countMatch = raw.match(/^vpc_http_request_duration_seconds_count(?:\\{[^}]*\\})?\\s+([0-9.eE+-]+)/m);
    const count = countMatch ? Number(countMatch[1]) : 0;
    return { requests: requestMatch ? Number(requestMatch[1]) : null,
      latency: sumMatch && count > 0 ? Number(sumMatch[1]) / count * 1000 : null };
  }
  function probe(id, endpointId, data, expected) {
    const ok = data && data.status === expected;
    text(id, ok ? expected.toUpperCase() : "Check response");
    status(endpointId, ok ? "HEALTHY" : "CHECK RESPONSE", ok ? "ok" : "error");
    return Boolean(ok);
  }
  async function runChecks() {
    const button = $("runChecks");
    if (button) { button.disabled = true; button.textContent = "Checking…"; }
    text("footerStatus", "Checking API");
    const results = await Promise.allSettled([fetchJson("/health"), fetchJson("/ready"), fetchText("/metrics")]);
    let health = false, ready = false, metricsOk = false;
    if (results[0].status === "fulfilled") {
      health = probe("healthValue", "healthEndpointStatus", results[0].value, "healthy");
      text("heroHealth", health ? "Healthy" : "Check");
      status("healthPill", health ? "● OPERATIONAL" : "● CHECK RESPONSE", health ? "ok" : "error");
    } else {
      text("healthValue", "Offline"); text("heroHealth", "Offline");
      status("healthPill", "● UNREACHABLE", "error"); status("healthEndpointStatus", "UNREACHABLE", "error");
    }
    if (results[1].status === "fulfilled") {
      ready = probe("readyValue", "readyEndpointStatus", results[1].value, "ready");
      status("readyPill", ready ? "● READY FOR TRAFFIC" : "● CHECK RESPONSE", ready ? "ok" : "error");
    } else {
      text("readyValue", "Offline"); status("readyPill", "● UNREACHABLE", "error");
      status("readyEndpointStatus", "UNREACHABLE", "error");
    }
    if (results[2].status === "fulfilled") {
      metricsOk = true;
      const m = parseMetrics(results[2].value);
      text("requestValue", m.requests === null ? "—" : m.requests.toLocaleString());
      text("latencyValue", m.latency === null ? "—" : m.latency.toLocaleString(undefined, { maximumFractionDigits: 2 }));
      $("latencyBar").style.width = `${Math.min(100, Math.max(3, (m.latency || 0) * 4))}%`;
      status("metricsEndpointStatus", "REACHABLE", "ok");
    } else {
      text("requestValue", "—"); text("latencyValue", "—");
      status("metricsEndpointStatus", "UNREACHABLE", "error");
    }
    const now = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    text("lastChecked", `Last checked ${now} · ${[health, ready, metricsOk].filter(Boolean).length}/3 endpoints reachable`);
    text("footerStatus", health && ready ? "● API operational" : "● Needs attention");
    if (button) { button.disabled = false; button.textContent = "Run checks ↻"; }
  }
  $("refreshButton")?.addEventListener("click", () => {
    runChecks(); const toast = $("toast");
    if (toast) { toast.textContent = "Refreshing service checks…"; toast.classList.add("show"); setTimeout(() => toast.classList.remove("show"), 2400); }
  });
  $("runChecks")?.addEventListener("click", runChecks);
  $("menuToggle")?.addEventListener("click", () => $("sidebar")?.classList.toggle("open"));
  document.querySelectorAll(".nav-link").forEach(link => link.addEventListener("click", () => {
    document.querySelectorAll(".nav-link").forEach(item => item.classList.remove("active"));
    link.classList.add("active"); $("sidebar")?.classList.remove("open");
  }));
  runChecks();
  setInterval(runChecks, 15000);
})();
