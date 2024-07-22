import React, { useState, useEffect } from 'react';
import './Post.css';

const Post = ({postId}) => {
	const [data, setData] = useState(null);

	useEffect(() => {
		const fetcher = async() => {
			try {
				const response = await fetch('/api/post/' + postId);
				const data = await response.json();
				setData(data);
			} catch (error) {
				console.error('Error fetching data:', error);
			}
		};

		fetcher();
	}, [postId]);

	if (data === null)
		return (<h1>Loading...</h1>);
	else
		return (
			<div className="post-container">
			<h1>{data.title}</h1>
			<h3>by <a href={'/user/' + data.user_id}>{data.username}</a> on {new Date(data.creation_time).toLocaleString()}</h3>
			<p>{data.content}</p>
			<p>❤️ {data.likes}</p>
			<div className="comment-section">
			{
				data.comments.length === 0 ?
					<div>
					<p>댓글이 없습니다.</p>
					</div>
				:
					data.comments.map(comment => (
						<div className="comment">
						<h3><a href={'/user/' + comment.user_id}>{comment.username}</a> on {new Date(comment.creation_time).toLocaleString()}</h3>
						<p>{comment.content}</p>
						</div>
					))
			}
			</div>
			</div>
		);
};

export default Post;
