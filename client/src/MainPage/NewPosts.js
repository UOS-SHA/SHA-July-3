import React from 'react';

const NewPosts = ({ posts }) => {
	if (!posts || posts.length === 0) {
		return (<div>새 글이 없습니다.</div>);
	}

	return (<div>
		{posts.map(post => (
			<div>
				<h3><a href="/post/"{post.id}>{post.title}</a> by {post.username} (❤️ {post.likes})</h3>
				<p>Created at: {new Date(post.creation_time).toLocaleString()}</p>
			</div>
		))}
		</div>);
};

export default NewPosts;
