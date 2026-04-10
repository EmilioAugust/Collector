import React, { useEffect } from 'react';
import { formatSeriesDate } from '../services/api';

const Modal = ({ item, type, isOpen, onClose, onStatusChange, onDelete }) => {
    useEffect(() => {
        const handleEsc = (e) => {
            if (e.key === 'Escape') {
                onClose();
            }
        };
        
        if (isOpen) {
            document.addEventListener('keydown', handleEsc);
            document.body.style.overflow = 'hidden';
        }
        
        return () => {
            document.removeEventListener('keydown', handleEsc);
            document.body.style.overflow = 'unset';
        };
    }, [isOpen, onClose]);
    
    if (!isOpen || !item) return null;
    
    const { id, name, title, description, overview, summary, status, year, rating, premiered, ended, author } = item;
    const displayName = name || title || 'Untitled';
    const displayDescription = description || overview || summary || '';
    const currentStatus = status || '';
    const normalizedStatus = currentStatus.toLowerCase();
    const displayRating = rating || '';
    
    const getAvailableStatuses = () => {
        if (type === 'movies' || type === 'series') {
            return ['Watched', 'Watching', 'Planning'];
        } else if (type === 'books') {
            return ['Read', 'Reading', 'Planning'];
        }
        return [];
    };
    
    const availableStatuses = getAvailableStatuses();
    const otherStatuses = availableStatuses.filter(s => s !== currentStatus);
    
    const releaseDate = premiered ? formatSeriesDate(premiered) : year || '';
    const endedDate = ended ? formatSeriesDate(ended) : '';
    
    const getSeriesYearsDisplay = () => {
        if (type !== 'series') return year || '';
        
        const startYear = premiered ? new Date(premiered).getFullYear() : year;
        if (!startYear) return '';
        
        if (ended) {
            const endYear = new Date(ended).getFullYear();
            return `${startYear} - ${endYear}`;
        } else {
            return `${startYear} - ...`;
        }
    };
    
    const seriesYearsDisplay = getSeriesYearsDisplay();
    
    const handleStatusChange = (e) => {
        const newStatus = e.target.value;
        if (newStatus && id) {
            onStatusChange(id, newStatus);
            onClose();
        }
    };
    
    const handleDelete = () => {
        if (id && window.confirm(`Are you sure you want to delete "${displayName}"?`)) {
            onDelete(id);
            onClose();
        }
    };
    
    const handleOverlayClick = (e) => {
        if (e.target === e.currentTarget) {
            onClose();
        }
    };

    return (
        <div className={`modal-overlay ${isOpen ? 'active' : ''}`} onClick={handleOverlayClick}>
            <div className="modal">
                <div className="modal-header">
                    <button className="modal-close" onClick={onClose}>&times;</button>
                    <h2 className="modal-title">{displayName}</h2>
                    <div className="modal-meta">
                        {currentStatus && (
                            <span className={`status-badge status-${normalizedStatus}`}>
                                {currentStatus}
                            </span>
                        )}
                        
                        {/* Показываем годы для сериалов */}
                        {type === 'series' ? (
                            <span className="year-badge">{seriesYearsDisplay}</span>
                        ) : year ? (
                            <span className="year-badge">{year}</span>
                        ) : null}
                        
                        {displayRating && <span className="year-badge">⭐ {displayRating}</span>}
                    </div>
                </div>
                
                <div className="modal-content">
                    {displayDescription && (
                        <div className="modal-description">
                            <h3>Description</h3>
                            <p>{displayDescription}</p>
                        </div>
                    )}
                    
                    <div className="modal-details">
                        {/* Для сериалов показываем даты премьеры и окончания */}
                        {type === 'series' && (
                            <>
                                {premiered && (
                                    <div className="detail-item">
                                        <span className="detail-label">First aired</span>
                                        <span className="detail-value">{formatSeriesDate(premiered)}</span>
                                    </div>
                                )}
                                
                                {ended ? (
                                    <div className="detail-item">
                                        <span className="detail-label">Last aired</span>
                                        <span className="detail-value">{formatSeriesDate(ended)}</span>
                                    </div>
                                ) : (
                                    <div className="detail-item">
                                        <span className="detail-label">Status</span>
                                        <span className="detail-value">Still Running</span>
                                    </div>
                                )}
                            </>
                        )}
                        
                        {/* Для фильмов показываем год */}
                        {type === 'movies' && year && (
                            <div className="detail-item">
                                <span className="detail-label">Release Year</span>
                                <span className="detail-value">{year}</span>
                            </div>
                        )}
                        
                        {/* Для книг показываем автора */}
                        {type === 'books' && author && (
                            <div className="detail-item">
                                <span className="detail-label">Author</span>
                                <span className="detail-value">
                                    {Array.isArray(author) ? author.join(', ') : author}
                                </span>
                            </div>
                        )}
                    </div>
                    
                    <div className="modal-actions">
                        <select 
                            className="modal-status-select"
                            onChange={handleStatusChange}
                            defaultValue=""
                        >
                            <option value="" disabled selected>Change status...</option>
                            {otherStatuses.map(status => (
                                <option key={status} value={status}>
                                    {status}
                                </option>
                            ))}
                        </select>
                        
                        <button 
                            className="modal-delete-btn"
                            onClick={handleDelete}
                        >
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Modal;
