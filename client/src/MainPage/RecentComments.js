import React from 'react';

const RecentComments = ({ comments }) => (
	<div>
	{comments.map(comment => (
		<div>
			<p><a href={'/post/' + comment.post_id}>{comment.username}: {comment.content}</a></p>
		</div>
	))}
	</div>
);

export default RecentComments;
