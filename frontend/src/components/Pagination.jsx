import React from 'react';

const Pagination = ({ currentPage, hasNextPage, onPageChange }) => {
    if (currentPage === 1 && !hasNextPage) return null;
    
    return (
        <div className="pagination">
            {currentPage > 1 && (
                <button onClick={() => onPageChange(currentPage - 1)}>
                    ◀ Prev
                </button>
            )}
            
            <button className="active">
                Page {currentPage}
            </button>
            
            {hasNextPage && (
                <button onClick={() => onPageChange(currentPage + 1)}>
                    Next ▶
                </button>
            )}
        </div>
    );
};

export default Pagination;