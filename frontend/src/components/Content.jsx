import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import Card from './Card';
import Modal from './Modal';
import Pagination from './Pagination';
import Filters from './Filters';
import { 
    moviesAPI, 
    seriesAPI, 
    booksAPI 
} from '../services/api';

const Content = ({ currentTab, currentStatus, onStatusChange }) => {
    const { logout } = useAuth();
    const { isDark, toggleTheme } = useTheme();
    
    const [collection, setCollection] = useState([]);
    const [searchResults, setSearchResults] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchPage, setSearchPage] = useState(1);
    const [hasNextPage, setHasNextPage] = useState(false);
    const [isSearching, setIsSearching] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [selectedItem, setSelectedItem] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [sortOrder, setSortOrder] = useState('newest');
    
    const sortCollection = (items, order = 'newest') => {
        if (!Array.isArray(items)) return [];

        return [...items].sort((a, b) => {
            const getDate = (item) => {
                if (item.created_at) return new Date(item.created_at).getTime();

                const id = item.id || item._id;
                if (typeof id === 'number') return id;
                if (typeof id === 'string') {
                    return parseInt(id.replace(/\D/g, '')) || 0;
                }
                return 0;
            };

            const diff = getDate(b) - getDate(a);
            return order === 'newest' ? diff : -diff;
        });
    };
    
    const sortedCollection = useMemo(() => {
        return sortCollection(collection, sortOrder);
    }, [collection, sortOrder]);
    
    const loadCollection = useCallback(async () => {
        setLoading(true);
        setError('');
        setIsSearching(false);
        
        try {
            let data = [];
            
            switch (currentTab) {
                case 'movies':
                    data = await moviesAPI.getMovies(currentStatus);
                    break;
                case 'series':
                    data = await seriesAPI.getSeries(currentStatus);
                    break;
                case 'books':
                    data = await booksAPI.getBooks(currentStatus);
                    break;
                default:
                    data = [];
            }
            
            const sortedData = sortCollection(Array.isArray(data) ? data : []);
            setCollection(sortedData);
            setSearchResults([]);
        } catch (err) {
            console.error('Load collection error:', err);
            setError(`Failed to load ${currentTab}: ${err.message}`);
            setCollection([]);
        } finally {
            setLoading(false);
        }
    }, [currentTab, currentStatus]);
    
    const handleSearch = async (page = 1) => {
        if (!searchQuery.trim()) {
            loadCollection();
            return;
        }
        
        setLoading(true);
        setError('');
        setIsSearching(true);
        setSortOrder('newest');
        
        try {
            let data = [];
            
            switch (currentTab) {
                case 'movies':
                    data = await moviesAPI.searchMovies(searchQuery, page, 10);
                    setHasNextPage(data.length === 10);
                    break;
                case 'series':
                    try {
                        const seriesData = await seriesAPI.searchSeries(searchQuery, 20);
                        console.log('Series search data received:', seriesData);
                        
                        let processedData = [];
                        if (Array.isArray(seriesData)) {
                            processedData = seriesData.map(series => {
                                return {
                                    ...series,
                                    name: series.name || series.title || '',
                                    year: series.year || 
                                        (series.premiered ? new Date(series.premiered).getFullYear() : null) ||
                                        (series.first_air_date ? new Date(series.first_air_date).getFullYear() : null),
                                    premiered: series.premiered,
                                    ended: series.ended,
                                    first_air_date: series.first_air_date,
                                    last_air_date: series.last_air_date,
                                    poster: series.image?.medium || series.image?.original || series.poster
                                };
                            });
                        }
                        
                        console.log('Processed series data:', processedData);
                        data = processedData;
                        setHasNextPage(false);
                    } catch (error) {
                        console.error('Series search error:', error);
                        throw error;
                    }
                    break;
                case 'books':
                    data = await booksAPI.searchBooks(searchQuery, 20);
                    setHasNextPage(false);
                    break;
                default:
                    data = [];
            }
            
            const sortedSearchResults = sortCollection(Array.isArray(data) ? data : []);
            setSearchResults(sortedSearchResults);
            setSearchPage(page);
        } catch (err) {
            console.error('Search error:', err);
            setError(`Search failed: ${err.message}`);
            setSearchResults([]);
        } finally {
            setLoading(false);
        }
    };
    
    const handleStatusChange = async (id, newStatus) => {
        try {
            switch (currentTab) {
                case 'movies':
                    await moviesAPI.updateMovieStatus(id, newStatus);
                    break;
                case 'series':
                    await seriesAPI.updateSeriesStatus(id, newStatus);
                    break;
                case 'books':
                    await booksAPI.updateBookStatus(id, newStatus);
                    break;
            }
            
            const updateArray = (arr) => 
                arr.map(item => 
                    (item.id === id || item._id === id) 
                        ? { ...item, status: newStatus } 
                        : item
                );
            
            setCollection(sortCollection(updateArray(collection)));
            setSearchResults(sortCollection(updateArray(searchResults)));
            
            showNotification(`Status updated to "${newStatus}" successfully!`);
        } catch (err) {
            console.error('Update status error:', err);
            showNotification(`Failed to update status: ${err.message}`, 'error');
        }
    };
    
    const handleDelete = async (id) => {
        try {
            switch (currentTab) {
                case 'movies':
                    await moviesAPI.deleteMovie(id);
                    break;
                case 'series':
                    await seriesAPI.deleteSeries(id);
                    break;
                case 'books':
                    await booksAPI.deleteBook(id);
                    break;
            }
            
            const filterArray = (arr) => 
                arr.filter(item => item.id !== id && item._id !== id);
            
            setCollection(sortCollection(filterArray(collection)));
            setSearchResults(sortCollection(filterArray(searchResults)));
            
            showNotification('Item deleted successfully!');
        } catch (err) {
            console.error('Delete error:', err);
            showNotification(`Failed to delete item: ${err.message}`, 'error');
        }
    };
    
    const handleAddItem = async (item) => {
        try {
            let data = {};
            
            switch (currentTab) {
                case 'movies':
                    data = {
                        imdb_id: item.imdbID || item.imdb_id,
                        status: 'Planning',
                        name: item.Title || item.name
                    };
                    await moviesAPI.addMovie(data);
                    break;
                case 'series':
                    data = {
                        tvmaze_id: String(item.tvmaze_id || item.id),
                        status: 'Planning',
                        name: item.name || item.title
                    };
                    await seriesAPI.addSeries(data);
                    break;
                case 'books':
                    data = {
                        olib_id: item.olib_id || item.key?.replace('/works/', '') || '',
                        author: Array.isArray(item.author) ? item.author.join(', ') : item.author,
                        title: item.title || "",
                        cover: item.cover || "",
                        status: 'Planning' || ""
                    };
                    await booksAPI.addBook(data);
                    break;
            }
            
            showNotification('Item added successfully!');
            loadCollection();
        } catch (err) {
            console.error('Add item error:', err);
            showNotification(`Failed to add item: ${err.message}`, 'error');
        }
    };
    
    const handleShowDetails = (item) => {
        setSelectedItem(item);
        setIsModalOpen(true);
    };
    
    const showNotification = (message, type = 'success') => {
        console.log(`${type}: ${message}`);
        if (type === 'error') {
            alert(`Error: ${message}`);
        }
    };
    
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };
    
    useEffect(() => {
        loadCollection();
    }, [loadCollection]);
    
    const displayItems = isSearching ? searchResults : sortedCollection;
    const isSearchActive = isSearching && searchQuery.trim();
    const tabLabels = {
        movies: 'Movies',
        series: 'Series',
        books: 'Books'
    };
    
    return (
        <>
            <div className="content">
                <div className="topbar">
                    <input 
                        id="searchInput" 
                        placeholder="Search..." 
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyPress={handleKeyPress}
                    />
                    <button 
                        id="searchBtn" 
                        onClick={() => handleSearch()}
                    >
                        Search
                    </button>
                    <button id="logoutBtn" onClick={logout}>
                        Logout
                    </button>
                    <button 
                        id="themeToggle" 
                        className="theme-toggle"
                        onClick={toggleTheme}
                    >
                        {isDark ? "☀️" : "🌙"}
                    </button>
                </div>
                
                <div className="filters-bar">
                    {!isSearchActive && (
                            <Filters 
                                currentTab={currentTab}
                                currentStatus={currentStatus}
                                onStatusChange={onStatusChange}
                            />
                    )}
            
                    <div className="items-counter">
                        {isSearchActive ? (
                            <>Found: <strong>{displayItems.length}</strong></>
                        ) : (
                            <>
                                {tabLabels[currentTab]}: <strong>{displayItems.length}</strong>
                            </>
                        )}
                    </div>
                </div>
                {!isSearchActive && (
                    <div className="sort-filter">
                        <button
                            className={sortOrder === 'newest' ? 'active' : ''}
                            onClick={() => setSortOrder('newest')}
                        >
                            Newest
                        </button>
                        <button
                            className={sortOrder === 'oldest' ? 'active' : ''}
                            onClick={() => setSortOrder('oldest')}
                        >
                            Oldest
                        </button>
                    </div>
                )}
                
                {isSearchActive && (
                    <Pagination 
                        currentPage={searchPage}
                        hasNextPage={hasNextPage}
                        onPageChange={handleSearch}
                    />
                )}
                
                {loading ? (
                    <div className="loading">Loading...</div>
                ) : error ? (
                    <div className="error">{error}</div>
                ) : (
                    <div className="grid">
                        {displayItems.length === 0 ? (
                            <div className="empty">
                                No {isSearchActive ? 'results' : currentTab} found
                            </div>
                        ) : (
                            displayItems.map((item, index) => (
                                isSearching ? (
                                    <div key={`search-${index}`} className="card">
                                        <div className="card-image-container">
                                            {item.poster || item.cover ? (
                                                <img 
                                                    src={
                                                        currentTab === 'books' && item.cover 
                                                            ? `https://covers.openlibrary.org/b/olid/${item.cover}-L.jpg`
                                                            : item.Poster || item.poster || item.cover_url
                                                    }
                                                    className="card-image"
                                                    alt={item.Title || item.name || item.title}
                                                    onError={(e) => {
                                                        e.target.style.display = 'none';
                                                        const placeholder = e.target.parentNode.querySelector('.image-placeholder');
                                                        if (placeholder) placeholder.style.display = 'flex';
                                                    }}
                                                />
                                            ) : null}
                                            <div 
                                                className="image-placeholder" 
                                                style={{ 
                                                    display: (!item.poster && !item.cover) ? 'flex' : 'none' 
                                                }}
                                            >
                                                <span className="placeholder-text">
                                                    {(item.Title || item.name || item.title || '').charAt(0).toUpperCase()}
                                                </span>
                                            </div>
                                        </div>
                                        <div className="card-content">
                                            <div className="card-header">
                                                <h3 className="card-title">
                                                    {item.Title || item.name || item.title || 'No title'}
                                                </h3>
                                                {(item.Year || item.year) && (
                                                    <div className="card-meta">
                                                        <div className="meta-row">
                                                            <span className="year-badge">
                                                                {item.Year || item.year}
                                                            </span>
                                                        </div>
                                                    </div>
                                                )}
                                                {item.author && (
                                                    <div className="card-meta">
                                                        <div className="meta-row">
                                                            <span className="year-badge">
                                                                {Array.isArray(item.author) ? item.author.join(', ') : item.author}
                                                            </span>
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                            <div className="card-actions">
                                                <button 
                                                    className="delete-btn add-btn"
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        handleAddItem(item);
                                                    }}
                                                >
                                                    Add
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <Card 
                                        key={item.id || item._id || `collection-${index}`}
                                        item={item}
                                        type={currentTab}
                                        onStatusChange={handleStatusChange}
                                        onDelete={handleDelete}
                                        onClick={handleShowDetails}
                                    />
                                )
                            ))
                        )}
                    </div>
                )}
            </div>
            
            <Modal
                item={selectedItem}
                type={currentTab}
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onStatusChange={handleStatusChange}
                onDelete={handleDelete}
            />
        </>
    );
};

export default Content;
