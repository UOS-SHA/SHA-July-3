import React from 'react';

const NewPosts = ({ posts }) => (
	  <div>
	    <h2>New Posts</h2>
	    {posts.slice(0, 10).map(post => (
		          <div key={post.id}>
		            <h3>{post.title}</h3>
		            <p>by {post.username[0]}</p>
		            <p>Likes: {post.likes}</p>
		            <p>Created at: {new Date(post.creation_time).toLocaleString()}</p>
		          </div>
		        ))}
	  </div>
);

export default NewPosts;
