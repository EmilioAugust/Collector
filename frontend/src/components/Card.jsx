import React from 'react';

const Card = ({ 
    item, 
    type, 
    onStatusChange, 
    onDelete, 
    onClick, 
    onAdd, 
    isSearchResult = false 
}) => {
    // Функция для получения года из даты
    const getYearFromDate = (dateString) => {
        if (!dateString) return null;
        try {
            const date = new Date(dateString);
            return isNaN(date) ? null : date.getFullYear();
        } catch {
            return null;
        }
    };

    // Функция для извлечения годов сериала (работает для поиска и коллекции)
    const getSeriesYears = () => {
        if (type !== 'series') return null;

        // Пробуем разные поля для даты премьеры
        const premiereDate = item.premiered || item.first_air_date || item.release_date;
        const endDate = item.ended || item.last_air_date;
        
        // Получаем год начала
        let startYear = null;
        if (premiereDate) {
            startYear = getYearFromDate(premiereDate);
        }
        
        // Если нет даты премьеры, пробуем год из других полей
        if (!startYear) {
            if (item.year && !isNaN(parseInt(item.year))) {
                startYear = parseInt(item.year);
            } else if (item.Year && !isNaN(parseInt(item.Year))) {
                startYear = parseInt(item.Year);
            } else if (item.first_air_year) {
                startYear = parseInt(item.first_air_year);
            }
        }
        
        if (!startYear) return null;
        
        // Получаем год окончания
        let endYear = null;
        if (endDate) {
            endYear = getYearFromDate(endDate);
        }
        
        // Если нет даты окончания, проверяем другие поля
        if (!endYear && item.last_air_year) {
            endYear = parseInt(item.last_air_year);
        }
        
        // Формируем строку с годами
        if (endYear) {
            return `${startYear} - ${endYear}`;
        } else {
            return `${startYear} - ...`;
        }
    };

    // Функция для получения года для фильмов и книг
    const getSimpleYear = () => {
        if (type === 'series') return null;
        
        if (item.year) return item.year;
        if (item.Year) return item.Year;
        if (item.release_date) return getYearFromDate(item.release_date);
        if (item.first_publish_year) return item.first_publish_year;
        if (item.publication_year) return item.publication_year;
        
        return null;
    };

    // Функция для получения имени
    const getName = () => {
        return item.name || item.title || item.Title || 'Untitled';
    };

    // Функция для получения автора (для книг)
    const getAuthor = () => {
        if (type !== 'books') return null;
        return item.author || item.author_name;
    };

    // Функция для получения статуса (только для коллекции)
    const getStatus = () => {
        return isSearchResult ? null : (item.status || '');
    };

    // Получаем данные
    const name = getName();
    const seriesYears = getSeriesYears();
    const simpleYear = getSimpleYear();
    const author = getAuthor();
    const status = getStatus();
    const normalizedStatus = status ? status.toLowerCase() : '';
    
    // Определяем что показывать как год
    const displayYear = type === 'series' ? seriesYears : simpleYear;
    
    // Определяем источник изображения
    let imageSrc = '';
    let hasImage = false;
    
    if (type === 'books' && item.cover) {
        imageSrc = `https://covers.openlibrary.org/b/olid/${item.cover}-L.jpg`;
        hasImage = true;
    } else if ((type === 'movies' || type === 'series') && (item.poster || item.Poster || item.image)) {
        const poster = item.poster || item.Poster || item.image?.medium || item.image?.original;
        imageSrc = poster;
        hasImage = imageSrc && imageSrc !== 'N/A' && imageSrc !== 'null' && imageSrc !== '';
    }
    
    // Первая буква для placeholder
    const firstLetter = name.charAt(0).toUpperCase();
    
    // Обработчики событий
    const handleStatusChange = (e) => {
        e.stopPropagation();
        const newStatus = e.target.value;
        if (newStatus && item.id) {
            onStatusChange(item.id || item._id, newStatus);
            e.target.value = '';
        }
    };
    
    const handleDelete = (e) => {
        e.stopPropagation();
        const itemId = item.id || item._id;
        if (itemId && window.confirm(`Are you sure you want to delete "${name}"?`)) {
            onDelete(itemId);
        }
    };
    
    const handleAdd = (e) => {
        e.stopPropagation();
        if (onAdd) {
            onAdd(item);
        }
    };
    
    const handleCardClick = () => {
        if (!isSearchResult && onClick) {
            onClick(item);
        }
    };
    
    // Определяем доступные статусы (только для коллекции)
    const getAvailableStatuses = () => {
        if (!isSearchResult && status) {
            if (type === 'movies' || type === 'series') {
                return ['Watched', 'Watching', 'Planning'];
            } else if (type === 'books') {
                return ['Read', 'Reading', 'Planning'];
            }
        }
        return [];
    };
    
    const availableStatuses = getAvailableStatuses();
    const otherStatuses = availableStatuses.filter(s => s !== status);
    
    return (
        <div 
            className="card" 
            onClick={handleCardClick}
            data-search={isSearchResult}
            data-type={type}
        >
            <div className="card-image-container">
                {hasImage ? (
                    <img 
                        src={imageSrc} 
                        alt={name}
                        className="card-image"
                        onError={(e) => {
                            e.target.style.display = 'none';
                            const placeholder = e.target.nextElementSibling;
                            if (placeholder) placeholder.style.display = 'flex';
                        }}
                    />
                ) : null}
                <div 
                    className="image-placeholder" 
                    style={{ display: hasImage ? 'none' : 'flex' }}
                >
                    <span className="placeholder-text">{firstLetter}</span>
                </div>
            </div>
            
            <div className="card-content">
                <div className="card-header">
                    <h3 className="card-title" title={name}>
                        {name}
                    </h3>
                    
                    {(status || displayYear || author) && (
                        <div className="card-meta">
                            <div className="meta-row">
                                {status && (
                                    <span className={`status-badge status-${normalizedStatus}`}>
                                        {status}
                                    </span>
                                )}
                                
                                {/* Показываем годы для сериалов или год для других типов */}
                                {displayYear && (
                                    <span className={`year-badge ${type === 'series' ? 'series-years' : ''}`}>
                                        {displayYear}
                                    </span>
                                )}
                            </div>
                            
                            {/* Автор для книг */}
                            {author && type === 'books' && (
                                <div className="meta-row">
                                    <span className="year-badge">
                                        {Array.isArray(author) ? author.join(', ') : author}
                                    </span>
                                </div>
                            )}
                        </div>
                    )}
                </div>
                
                <div className="card-actions" onClick={e => e.stopPropagation()}>
                    {isSearchResult ? (
                        <button 
                            className="delete-btn add-btn"
                            onClick={handleAdd}
                        >
                            Add
                        </button>
                    ) : (
                        <>
                            {status && otherStatuses.length > 0 && (
                                <select 
                                    className="status-select" 
                                    onChange={handleStatusChange}
                                    defaultValue=""
                                >
                                    <option value="" disabled>Change status</option>
                                    {otherStatuses.map(statusOption => (
                                        <option key={statusOption} value={statusOption}>
                                            {statusOption}
                                        </option>
                                    ))}
                                </select>
                            )}
                            
                            <button 
                                className="delete-btn"
                                onClick={handleDelete}
                            >
                                Delete
                            </button>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Card;