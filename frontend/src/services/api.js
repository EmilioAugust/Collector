const API_BASE_URL = "http://localhost:8000";

export const fetchAuth = async (url, options = {}) => {
    const accessToken = localStorage.getItem("access_token");
    
    if (!accessToken) {
        console.error("No access token found");
        throw new Error("Not authenticated");
    }

    try {
        console.log(`🔗 Making request to: ${url}`);
        console.log(`📝 Request options:`, {
            method: options.method || 'GET',
            headers: options.headers,
            body: options.body ? JSON.parse(options.body) : undefined
        });

        const response = await fetch(`${API_BASE_URL}${url}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {}),
                "Authorization": `Bearer ${accessToken}`
            }
        });

        console.log(`📡 Response status: ${response.status} ${response.statusText}`);

        console.log('📋 Response headers:', Object.fromEntries(response.headers.entries()));

        const responseText = await response.text();
        console.log('📄 Response body:', responseText);

        if (response.status === 422) {
            console.error('❌ 422 Validation Error Details:');
            console.error('URL:', url);
            console.error('Request data:', options.body);
            console.error('Response:', responseText);
            
            let errorDetails = 'Validation failed';
            try {
                const errorJson = JSON.parse(responseText);
                if (errorJson.detail) {
                    if (Array.isArray(errorJson.detail)) {
                        errorDetails = errorJson.detail.map(d => d.msg || d.loc?.join('.')).join(', ');
                    } else {
                        errorDetails = errorJson.detail;
                    }
                }
            } catch (e) {
                // couldn't parse JSON
            }
            
            throw new Error(`422 Validation Error: ${errorDetails}`);
        }

        if (response.status === 401 || response.status === 403) {
            console.error("Auth failed, logging out");
            localStorage.removeItem("access_token");
            throw new Error("Authentication required");
        }

        if (!response.ok) {
            console.error(`HTTP error ${response.status}:`, responseText);
            throw new Error(`Server error: ${response.status} - ${responseText.substring(0, 100)}`);
        }

        try {
            return responseText ? JSON.parse(responseText) : {};
        } catch (e) {
            console.warn('Could not parse response as JSON, returning text');
            return responseText;
        }

    } catch (error) {
        console.error("Fetch error details:", {
            message: error.message,
            url: url,
            options: options
        });
        throw error;
    }
};

// auth function
export const authAPI = {
    login: async (username, password) => {
        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ username, password })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Login failed");
        }
        
        return response.json();
    },
    
    register: async (username, email, password) => {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Registration failed");
        }
        
        return response.json();
    }
};

// function for movies
export const moviesAPI = {
    getMovies: (status = "All") => 
        fetchAuth(status === "All" 
            ? "/films/show_movies" 
            : `/films/show_movies_status?status=${status}`),
    
    searchMovies: async (query, page = 1, limit = 10) => {
        const data = await fetchAuth(
            `/films/show_search_results?query=${encodeURIComponent(query)}&page=${page}&limit=${limit}`
        );
        
        // Трансформируем данные для унификации формата
        if (Array.isArray(data)) {
            return data.map(item => ({
                id: item.imdb_id || item.id,
                title: item.Title || item.title || item.name,
                year: item.Year || item.year,
                poster: item.Poster || item.poster,
                imdb_id: item.imdbID || item.imdb_id,
                // Добавляем другие поля которые могут быть нужны
                ...item
            }));
        }
        return data;
    },
    
    addMovie: (data) => 
        fetchAuth("/films/add_movies", {
            method: "POST",
            body: JSON.stringify(data)
        }),
    
    updateMovieStatus: (id, status) => 
        fetchAuth(`/films/update_movies_status?id=${id}&status=${encodeURIComponent(status)}`, {
            method: "PUT"
        }),
    
    deleteMovie: (id) => 
        fetchAuth(`/films/delete_movies?id=${id}`, {
            method: "DELETE"
        })
};

// function for series
export const seriesAPI = {
    getSeries: (status = "All") => 
        fetchAuth(status === "All" 
            ? "/tv_shows/show_series" 
            : `/tv_shows/show_series_status?status=${status}`),
    
    searchSeries: (query, limit = 20) => 
        fetchAuth(`/tv_shows/show_search_results?query=${encodeURIComponent(query)}&limit=${limit}`),
    
    addSeries: (data) => 
        fetchAuth("/tv_shows/add_series", {
            method: "POST",
            body: JSON.stringify(data)
        }),
    
    updateSeriesStatus: (id, status) => 
        fetchAuth(`/tv_shows/update_series_status?id=${id}&status=${encodeURIComponent(status)}`, {
            method: "PUT"
        }),
    
    deleteSeries: (id) => 
        fetchAuth(`/tv_shows/delete_series?id=${id}`, {
            method: "DELETE"
        })
};

// function for books
export const booksAPI = {
    getBooks: (status = "All") => 
        fetchAuth(status === "All" 
            ? "/books/show_books" 
            : `/books/show_books_status?status=${status}`),
    
    searchBooks: (query, limit = 20) => 
        fetchAuth(`/books/show_search_results_book?query=${encodeURIComponent(query)}&limit=${limit}`),
    
    addBook: (data) => 
        fetchAuth("/books/add_books", {
            method: "POST",
            body: JSON.stringify(data)
        }),
    
    updateBookStatus: (id, status) => 
        fetchAuth(`/books/update_books_status?id=${id}&status=${encodeURIComponent(status)}`, {
            method: "PUT"
        }),
    
    deleteBook: (id) => 
        fetchAuth(`/books/delete_books?id=${id}`, {
            method: "DELETE"
        })
};

// useful functions
export const formatDate = (dateStr) => {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    if (isNaN(d)) return dateStr;
    return d.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric"
    });
};

export const formatSeriesDate = (dateStr) => {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    if (isNaN(d)) return dateStr;
    return d.toLocaleDateString("en-EN", {
        day: "numeric",
        month: "long",
        year: "numeric"
    });
};
