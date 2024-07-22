import React, { useState, useEffect } from 'react';

const User = ({userId}) => {
	const [user, setUser] = useState(null);

	useEffect(() => {
		const fetcher = async() => {
			try {
				const response = await fetch('/api/user/id/' + userId);
				const data = await response.json();
				setUser(data);
			} catch (error) {
				console.error('Error fetching data:', error);
			}
		};

		fetcher();
	}, [userId]);

	if (user === null)
		return (<h1>Loading...</h1>);
	else
		return (
			<div className="profile">
			<div className="profile-element">
			<h2>{user.username}</h2>
			<hr />
			<p>학년: {user.school_year}학년</p>
			<p>가입 일자: {user.creation_date}</p>
			</div>
			<div className="profile-element">
			<h2>작성 글 목록</h2>
			<hr />
			{
				user.posts.map(post => (
					<h3><a href={'/post/' + post.id}>{post.title}</a> (❤️ {post.likes})</h3>))
			}
			</div>
			<div className="profile-element">
			<h2>작성 댓글 목록</h2>
			<hr />
			{
				user.comments.map(comment => (
					<p><a href={'/post/' + comment.original_post_id}>{comment.content}</a></p>))
			}
			</div>
			</div>
		);
};

export default User;

