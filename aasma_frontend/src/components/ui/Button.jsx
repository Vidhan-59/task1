import React from 'react';

export function Button({ type = "button", children, className }) {
  return (
    <button
      type={type}
      className={`inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-md font-medium text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black ${className}`}

    >
      {children}
    </button>
  );
}
