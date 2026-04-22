import React, { useEffect, useState } from "react";
import api from "../api/client";
import Filters from "../components/Filters";
import AvailabilityChart from "../components/AvailabilityChart";
import AvailabilityTable from "../components/AvailabilityTable";
import Chatbot from "../components/Chatbot";
import type { StoreMetrics, Interval, GlobalMetrics } from "../types";
import "./Dashboard.css";

const Dashboard: React.FC = () => {
    const [stores, setStores] = useState<string[]>([]);
    const [storeId, setStoreId] = useState("");
    const [fromDate, setFromDate] = useState("");
    const [toDate, setToDate] = useState("");

    const [storeMetrics, setStoreMetrics] = useState<StoreMetrics | null>(null);
    const [intervals, setIntervals] = useState<Interval[]>([]);
    const [globalMetrics, setGlobalMetrics] = useState<GlobalMetrics | null>(null);

    const params: any = {};
    if (fromDate) params.from_date = new Date(fromDate).toISOString();
    if (toDate) params.to_date = new Date(toDate).toISOString();

    useEffect(() => {
        api.get<string[]>("/api/availability/stores").then((res) => setStores(res.data));
    }, []);

    useEffect(() => {
        api.get<GlobalMetrics>("/api/availability/global", { params }).then((res) => setGlobalMetrics(res.data));

        if (storeId) {
            api.get<StoreMetrics>(`/api/availability/store/${storeId}`, { params }).then((res) => setStoreMetrics(res.data));
            api.get<Interval[]>(`/api/availability/store/${storeId}/intervals`, { params }).then((res) => setIntervals(res.data));
        } else {
            setStoreMetrics(null);
            setIntervals([]);
        }
    }, [storeId, fromDate, toDate]);

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <div className="dashboard-title">
                    <h1>Store Availability</h1>
                    <p>Monitoreo en tiempo real de disponibilidad y rendimiento.</p>
                </div>
                <span className="badge">{storeId ? `Store: ${storeId}` : "All Stores"}</span>
            </div>

            <Filters
                stores={stores}
                storeId={storeId}
                fromDate={fromDate}
                toDate={toDate}
                onStoreChange={setStoreId}
                onFromChange={setFromDate}
                onToChange={setToDate}
            />

            {globalMetrics && (
                <div className="kpi-grid">
                    <div className="kpi-card">
                        <h4>Avg Availability</h4>
                        <strong>{globalMetrics.avg_availability_percent}%</strong>
                    </div>
                    <div className="kpi-card">
                        <h4>Total Uptime</h4>
                        <strong>{globalMetrics.total_uptime_seconds.toLocaleString()}s</strong>
                    </div>
                    <div className="kpi-card">
                        <h4>Total Downtime</h4>
                        <strong>{globalMetrics.total_downtime_seconds.toLocaleString()}s</strong>
                    </div>
                </div>
            )}

            {storeId && (
                <div className="section-grid">
                    <AvailabilityTable metrics={storeMetrics} />
                    <AvailabilityChart intervals={intervals} />
                </div>
            )}

            <Chatbot storeId={storeId} fromDate={fromDate} toDate={toDate} />
        </div>
    );
};

export default Dashboard;