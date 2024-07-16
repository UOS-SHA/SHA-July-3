import React from 'react';

const RecentComments = ({ comments }) => (
	<div>
	{comments.map(comment => (
		<div>
			<p>{comment.username}: {comment.content}</p>
		</div>
	))}
	</div>
);

export default RecentComments;
