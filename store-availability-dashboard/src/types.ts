export interface StoreMetrics {
    store_id: string;
    uptime_seconds: number;
    downtime_seconds: number;
    availability_percent: number;
    state_changes: number;
    interval_count: number;
    from_date?: string;
    to_date?: string;
}

export interface GlobalMetrics {
    total_stores: number;
    avg_availability_percent: number;
    total_uptime_seconds: number;
    total_downtime_seconds: number;
    from_date?: string;
    to_date?: string;
}

export interface Interval {
    store_id: string;
    state: string;
    start: string;
    end: string;
    duration_seconds: number;
}

export interface ChatResponse {
    answer: string;
    sources: string[];
}