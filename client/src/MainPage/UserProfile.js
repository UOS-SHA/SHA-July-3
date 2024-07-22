import React from 'react';

const UserProfile = ({ userId }) => {
	if (!userId)
		return (
			<div>
			<h2>로그인이 필요합니다.</h2>
			</div>
		);

	return (
		<div>
		<h2>User Profile</h2>
		<p>User ID: {userId}</p>
		</div>
	);
};

export default UserProfile;
