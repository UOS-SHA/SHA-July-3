import React from 'react';

const RecentComments = ({ comments }) => (
	  <div>
	    <h2>Posts with Recent Comments</h2>
	    {comments.map(comment => (
		          <div key={comment.post_id}>
		            <h3>{comment.post_title}</h3>
		            <p>by {comment.username[0]}</p>
		            <p>Comment: {comment.comment_text}</p>
		            <p>Commented at: {new Date(comment.comment_time).toLocaleString()}</p>
		          </div>
		        ))}
	  </div>
);

export default RecentComments;
