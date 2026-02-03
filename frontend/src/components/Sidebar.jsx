import React from 'react';

const Sidebar = ({ currentTab, onTabChange }) => {
    const tabs = [
        { id: 'movies', label: 'Movies' },
        { id: 'series', label: 'Series' },
        { id: 'books', label: 'Books' }
    ];

    return (
        <aside className="sidebar">
            <div className="logo">COLLECTOR</div>
            <nav>
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        className={`nav-btn ${currentTab === tab.id ? 'active' : ''}`}
                        onClick={() => onTabChange(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </nav>
        </aside>
    );
};

export default Sidebar;