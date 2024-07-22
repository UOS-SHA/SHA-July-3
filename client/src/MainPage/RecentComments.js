import React from 'react';

const RecentComments = ({ comments }) => {
	if (!comments || comments.length === 0) {
		return (<div>새 댓글이 없습니다.</div>);
	}

	return (<div>
	{comments.map(comment => (
		<div>
			<p><a href={'/post/' + comment.post_id}>{comment.username}: {comment.content}</a></p>
		</div>
	))}
	</div>);
};

export default RecentComments;
