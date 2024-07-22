import React from 'react';

const TopPosts = ({ posts }) => {
	if (!posts || posts.length === 0) {
		return (<div>인기 글이 없습니다.</div>);
	}

	return (<div>
		{posts.map(post => (
			<div>
			<h3><a href={'/post/' + post.id}>{post.title}</a></h3>
			<p>by {post.username} (❤️ {post.likes})</p>
			</div>
		))}
		</div>);
};

export default TopPosts;
