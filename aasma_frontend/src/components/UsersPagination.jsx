// UsersPagination.jsx
import React from 'react';

export default function UsersPagination({ currentPage, hasNext, hasPrevious, onPageChange }) {
  return (
    <div className="mt-6 flex justify-between">
      <button 
        disabled={!hasPrevious} 
        onClick={() => onPageChange(currentPage - 1)}
        className="btn btn-outline"
      >
        Previous
      </button>
      <span>Page {currentPage}</span>
      <button 
        disabled={!hasNext} 
        onClick={() => onPageChange(currentPage + 1)}
        className="btn btn-outline"
      >
        Next
      </button>
    </div>
  );
}
