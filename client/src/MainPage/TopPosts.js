import React from 'react';

const TopPosts = ({ posts }) => (
	  <div>
	    <h2>Top Posts</h2>
	    {posts.slice(0, 5).map(post => (
		          <div key={post.id}>
		            <h3>{post.title}</h3>
		            <p>by {post.username[0]}</p>
		            <p>Likes: {post.likes}</p>
		          </div>
		        ))}
	  </div>
);

export default TopPosts;
