import React from "react";
import type { StoreMetrics } from "../types";

interface Props {
    metrics: StoreMetrics | null;
}

const AvailabilityTable: React.FC<Props> = ({ metrics }) => {
    if (!metrics) return null;

    return (
        <div className="card">
            <h3>Store Metrics</h3>
            <table className="table">
                <tbody>
                <tr><td>Store</td><td>{metrics.store_id}</td></tr>
                <tr><td>Availability %</td><td>{metrics.availability_percent}</td></tr>
                <tr><td>Uptime (s)</td><td>{metrics.uptime_seconds}</td></tr>
                <tr><td>Downtime (s)</td><td>{metrics.downtime_seconds}</td></tr>
                <tr><td>State changes</td><td>{metrics.state_changes}</td></tr>
                <tr><td>Intervals</td><td>{metrics.interval_count}</td></tr>
                </tbody>
            </table>
        </div>
    );
};

export default AvailabilityTable;