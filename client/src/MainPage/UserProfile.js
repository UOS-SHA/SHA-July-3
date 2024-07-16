import React from 'react';

const UserProfile = ({ userId }) => {
	  if (!userId) return null;

	  return (
		      <div>
		        <h2>User Profile</h2>
		        <p>User ID: {userId}</p>
		      </div>
		    );
};

export default UserProfile;
