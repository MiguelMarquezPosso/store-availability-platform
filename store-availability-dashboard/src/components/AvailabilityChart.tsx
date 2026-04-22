import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import type { Interval } from "../types";

interface Props {
    intervals: Interval[];
}

const AvailabilityChart: React.FC<Props> = ({ intervals }) => {
    const data = intervals.flatMap((i) => {
        const value = i.state === "online" ? 100 : 0;
        return [
            { time: new Date(i.start).toLocaleString(), availability: value },
            { time: new Date(i.end).toLocaleString(), availability: value }
        ];
    });

    return (
        <div className="card">
            <h3>Availability Timeline</h3>
            <div style={{ width: "100%", height: 280 }}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="time" hide />
                        <YAxis domain={[0, 100]} />
                        <Tooltip />
                        <Line type="stepAfter" dataKey="availability" stroke="#6366f1" strokeWidth={2} dot={false} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default AvailabilityChart;