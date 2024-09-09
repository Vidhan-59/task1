
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import UsersList from "./UsersList";
import UsersPagination from "./UsersPagination";
import Cookies from "js-cookie";
import useDebounce from "./hooks/useDebounce";

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [error, setError] = useState(""); // To hold error messages
  const debouncedSearchQuery = useDebounce(searchQuery, 500); // Debounce search query
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsers = async () => {
      const token = Cookies.get("auth_token");

      if (!token) {
        setError("You are not allowed to access this page. Redirecting to signup...");
        setTimeout(() => {
          navigate("/signup"); // Redirect after 2 seconds
        }, 2000);
        return;
      }

      setLoading(true);
      try {
        const response = await fetch(
          `http://localhost:8000/api/get_users/?page=${page}&search=${debouncedSearchQuery}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch users");
        }

        const data = await response.json();
        setUsers(data.results);
        setHasNext(!!data.next);
        setHasPrevious(!!data.previous);
      } catch (error) {
        console.error("Failed to fetch users", error);
        setError("Failed to fetch users");
      }
      setLoading(false);
    };

    fetchUsers();
  }, [page, debouncedSearchQuery, navigate]);

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
    setPage(1); // Reset to the first page on new search
  };

  const handleAddUserClick = () => {
    navigate("/add_users");
  };

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">User Directory</h1>
      <input
        type="text"
        value={searchQuery}
        onChange={handleSearchChange}
        placeholder="Search users..."
        className="mb-4 p-2 border border-gray-300 rounded"
      />
      <button
        onClick={handleAddUserClick}
        className="bg-blue-500 text-white px-4 py-2 rounded mb-4"
      >
        Add User
      </button>
      {loading ? (
        <div>Loading users...</div>
      ) : (
        <>
          <UsersList users={users} />
          <UsersPagination
            currentPage={page}
            hasNext={hasNext}
            hasPrevious={hasPrevious}
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
}
