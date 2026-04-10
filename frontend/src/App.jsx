import React, { useState, useEffect, useCallback } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import Auth from './components/Auth';
import Sidebar from './components/Sidebar';
import Content from './components/Content';

function App() {
    const { isAuthenticated, loading: authLoading } = useAuth();
    const [currentTab, setCurrentTab] = useState('movies');
    const [currentStatus, setCurrentStatus] = useState('All');
    
    if (authLoading) {
        return <div className="loading">Loading...</div>;
    }
    
    return (
        <div className="App">
            {!isAuthenticated ? (
                <Auth />
            ) : (
                <div className="layout">
                    <Sidebar 
                        currentTab={currentTab}
                        onTabChange={(tab) => {
                            setCurrentTab(tab);
                            setCurrentStatus('All');
                        }}
                    />
                    <Content 
                        currentTab={currentTab}
                        currentStatus={currentStatus}
                        onStatusChange={setCurrentStatus}
                    />
                </div>
            )}
        </div>
    );
}

const AppWithProviders = () => (
    <AuthProvider>
        <ThemeProvider>
            <App />
        </ThemeProvider>
    </AuthProvider>
);

export default AppWithProviders;
