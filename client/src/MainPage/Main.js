import React, { useState, useEffect } from 'react';
import UserProfile from './UserProfile';
import NewPosts from './NewPosts';
import TopPosts from './TopPosts';
import RecentComments from './RecentComments';
import './MainPage.css';

const MainPage = () => {
	const [data, setData] = useState({
		logged_in_user_id: 0,
		new_posts: [],
		top_posts: [],
		recent_comments: []
	});

	useEffect(() => {
		const fetcher = async () => {
			try {
				const response = await fetch('http://127.0.0.1:5000/');
				console.log(response);
				const data = await response.json();
				setData(data);
			} catch (error) {
				console.error('Error fetching data:', error);
			}
		};

		fetcher();
	});

	if (data === null)
		return (<h1>Loading...</h1>);
	else
		return (
			<div className="main-container">
			<div className="grid-item">
			<h2>계정</h2>
			<UserProfile userId={data.logged_in_user_id} />
			</div>
			<div className="grid-item">
			<h2>새 글</h2>
			<NewPosts posts={data.new_posts} />
			</div>
			<div className="grid-item">
			<h2>최상위 글</h2>
			<TopPosts posts={data.top_posts} />
			</div>
			<div className="grid-item">
			<h2>새 댓글</h2>
			<RecentComments comments={data.recent_comments} />
			</div>
			</div>
		);
};

export default MainPage;
