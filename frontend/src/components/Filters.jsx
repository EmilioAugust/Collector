import React from 'react';

const STATUS_MAP = {
    movies: ["All", "Watched", "Watching", "Planning"],
    series: ["All", "Watched", "Watching", "Planning"],
    books: ["All", "Read", "Reading", "Planning"]
};

const Filters = ({ currentTab, currentStatus, onStatusChange }) => {
    const statuses = STATUS_MAP[currentTab] || [];
    
    return (
        <div className="filters">
            {statuses.map(status => (
                <div
                    key={status}
                    className={`filter ${status === currentStatus ? 'active' : ''}`}
                    onClick={() => onStatusChange(status)}
                >
                    {status}
                </div>
            ))}
        </div>
    );
};

export default Filters;