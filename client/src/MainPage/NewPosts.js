import React from 'react';

const NewPosts = ({ posts }) => {
	console.log(posts);
	if (!posts || posts.length === 0) {
		return (<div>새 글이 없습니다.</div>);
	}

	return (<div>
			<h2>새 글</h2>
			{posts.slice(0, 10).map(post => (
				<div key={post.id}>
					<h3>{post.title}</h3>
					<p>by {post.username}</p>
					<p>Likes: {post.likes}</p>
					<p>Created at: {new Date(post.creation_time).toLocaleString()}</p>
				</div>
		))}
		</div>);
};

export default NewPosts;
