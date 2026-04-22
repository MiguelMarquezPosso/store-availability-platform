import React from "react";

interface Props {
    stores: string[];
    storeId: string;
    fromDate: string;
    toDate: string;
    onStoreChange: (v: string) => void;
    onFromChange: (v: string) => void;
    onToChange: (v: string) => void;
}

const Filters: React.FC<Props> = ({
                                      stores, storeId, fromDate, toDate, onStoreChange, onFromChange, onToChange
                                  }) => {
    return (
        <div className="card">
            <h3>Filters</h3>
            <div className="filters">
                <select value={storeId} onChange={(e) => onStoreChange(e.target.value)}>
                    <option value="">All stores</option>
                    {stores.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
                <input type="datetime-local" value={fromDate} onChange={(e) => onFromChange(e.target.value)} />
                <input type="datetime-local" value={toDate} onChange={(e) => onToChange(e.target.value)} />
            </div>
        </div>
    );
};

export default Filters;