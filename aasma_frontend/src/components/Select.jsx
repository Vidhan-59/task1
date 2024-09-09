

import React from "react";

export function Select({ label, register, name, options, error, ...rest }) {
  return (
    <div className="form-group">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <select
        name={name}
        {...register(name)} // Spread the register object for full compatibility
        className={`mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
          error ? "border-red-500" : ""
        }`}
        {...rest}
      >
        <option value="" disabled>Select a {label.toLowerCase()}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
    </div>
  );
}
