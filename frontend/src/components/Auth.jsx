import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { authAPI } from '../services/api';

const Auth = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isLogin) {
                const data = await authAPI.login(username, password);
                if (!data.access_token) {
                    throw new Error('No access token received');
                }
                login(data.access_token);
            } else {
                if (!email) {
                    throw new Error('Email is required');
                }
                
                await authAPI.register(username, email, password);
                const data = await authAPI.login(username, password);
                login(data.access_token);
            }
        } catch (err) {
            console.error('Auth error:', err);
            setError(err.message || 'Authentication failed');
            
            if (err.message.includes('Failed to fetch')) {
                setError('Cannot connect to server. Make sure backend is running on localhost:8000');
            }
        } finally {
            setLoading(false);
        }
    };

    const toggleMode = () => {
        setIsLogin(!isLogin);
        setError('');
    };

    return (
        <div className="auth">
            <div className="auth-box">
                <h2>{isLogin ? 'Login' : 'Register'}</h2>
                
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        disabled={loading}
                    />
                    
                    {!isLogin && (
                        <input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            disabled={loading}
                        />
                    )}
                    
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={loading}
                    />
                    
                    <button type="submit" disabled={loading}>
                        {loading ? 'Loading...' : (isLogin ? 'Login' : 'Register')}
                    </button>
                </form>
                
                <p className="switch" onClick={toggleMode} style={{ cursor: 'pointer' }}>
                    {isLogin ? 'Create account' : 'Already have an account? Login'}
                </p>
                
                {error && <p className="auth-error">{error}</p>}
            </div>
        </div>
    );
};

export default Auth;