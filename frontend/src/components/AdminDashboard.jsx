// src/components/AdminDashboard.jsx
import React, { useState, useEffect } from "react";

function AdminDashboard() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/device_logs")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => setLogs(data))
      .catch((err) => {
        console.error("Error fetching device logs:", err);
        setError("Error fetching device logs");
      });
  }, []);

  // Simple battery indicator based on voltage value
  const renderBattery = (voltage) => {
    if (voltage === null || voltage === undefined) return "N/A";
    // Adjust thresholds as needed
    if (voltage >= 450) return "High";
    if (voltage >= 400) return "Medium";
    return "Low";
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Device Logs</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <table border="1" cellPadding="5" cellSpacing="0">
        <thead>
          <tr>
            <th>ID</th>
            <th>User ID</th>
            <th>Name</th>
            <th>Watering Status</th>
            <th>Battery Voltage</th>
            <th>Battery Indicator</th>+
            <th>Issues</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.user_id}</td>
              <td>{log.name}</td>
              <td>{log.watering_status}</td>
              <td>{log.battery_voltage !== null ? log.battery_voltage : "N/A"}</td>
              <td>{renderBattery(log.battery_voltage)}</td>
              <td>{log.issues || "None"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminDashboard;
