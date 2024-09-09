// UserDetailPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
export default function UserDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
    const token = Cookies.get('auth_token');
      try {
        const response = await fetch(`http://localhost:8000/api/users/${id}/`, { cache: 'no-store', 
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,  // Add the token to the Authorization header
              'Content-Type': 'application/json',
            },
         });
        if (!response.ok) {
          throw new Error('Failed to fetch user');
        }
        const data = await response.json();
        setUser(data);
      } catch (error) {
        console.error('Failed to fetch user', error);
        setError('Failed to load user data. Please try again later.');
      }
    };

    fetchUser();
  }, [id]);

  if (error) return <div>{error}</div>;
  if (!user) return <div>Loading...</div>;

  return (
    <div className="container mx-auto p-4">
      <button onClick={() => navigate('/users')} className="btn btn-outline mb-4">
        ← Back to Users
      </button>
      <div className="card max-w-4xl mx-auto overflow-hidden shadow-lg">
        <div className="card-header bg-primary text-white p-6">
          <div className="flex items-center space-x-4">
            <img 
              src={user.profile_picture || 'default-profile-picture-url'} 
              alt={user.full_name || 'User'} 
              className="rounded-full w-24 h-24 border-4 border-white"
            />
            <div>
              <h2 className="text-3xl font-bold">{user.full_name || 'Name Not Available'}</h2>
              <p className="text-xl opacity-90">{user.job_title || 'Job Title Not Available'}</p>
            </div>
          </div>
        </div>
        <div className="card-content p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h2 className="text-2xl font-semibold mb-2">Contact Information</h2>
              <p className="flex items-center mb-2"><strong>Email:</strong> {user.email || 'Email Not Available'}</p>
              <p className="flex items-center mb-2"><strong>Phone:</strong> {user.contact_number || 'Phone Not Available'}</p>
              <p className="flex items-center mb-2"><strong>Location:</strong> {user.location || 'Location Not Available'}</p>
            </div>
            <div>
              <h2 className="text-2xl font-semibold mb-2">Work Information</h2>
              <p className="flex items-center mb-2"><strong>Job Title:</strong> {user.job_title || 'Job Title Not Available'}</p>
              <p className="flex items-center mb-2"><strong>Department:</strong> {user.department || 'Department Not Available'}</p>
              <p className="flex items-center mb-2"><strong>Username:</strong> {user.username || 'Username Not Available'}</p>
            </div>
          </div>
          <div className="mt-6">
            <h2 className="text-2xl font-semibold mb-2">About</h2>
            <p>{user.short_bio || 'Short Bio Not Available'}</p>
          </div>
          <div className="mt-6">
            {/* <p className="text-sm text-gray-500"><strong>Employee ID:</strong> {user.user_id || 'ID Not Available'}</p> */}
          </div>
        </div>
      </div>
    </div>
  );
}
