// UsersList.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export default function UsersList({ users }) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {users.map(user => (
          <Link to={`/users/${user.user_id}`} key={user.user_id}>
            <div className="card cursor-pointer hover:shadow-lg transition-shadow">
              <div className="card-content flex items-center p-4">
                <img
                  src={user.profile_picture}
                  alt={user.full_name}
                  className="rounded-full w-24 h-24"
                />
                <div className="ml-4">
                  <h2 className="text-xl font-semibold">{user.full_name}</h2>
                  <p className="text-gray-600">{user.job_title}</p>
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    );
  }
