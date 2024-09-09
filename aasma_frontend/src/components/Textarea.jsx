

import React, { forwardRef } from "react";

export const Textarea = forwardRef(({ label, error, ...rest }, ref) => {
  return (
    <div className="form-group">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <textarea
        ref={ref} // Attach the ref here
        className={`mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
          error ? "border-red-500" : ""
        }`}
        {...rest}
      />
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
    </div>
  );
});
