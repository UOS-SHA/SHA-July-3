import React, { useState, useEffect } from 'react';
import UserProfile from './UserProfile';
import NewPosts from './NewPosts';
import TopPosts from './TopPosts';
import RecentComments from './RecentComments';
import './MainPage.css';

const MainPage = () => {
	  const [data, setData] = useState({
		      logged_in_user_id: 0,
		      new_posts: [],
		      top_posts: [],
		      recent_comments: []
		    });

	  useEffect(() => {
		      fetch('/api/data')
		        .then(response => response.json())
		        .then(fetchedData => setData(fetchedData))
		        .catch(error => console.error('Error fetching data:', error));
		    }, []);

	  return (
		      <div className="main-container">
		        <div className="grid-item">
		          <UserProfile userId={data.logged_in_user_id} />
		        </div>
		        <div className="grid-item">
		          <NewPosts posts={data.new_posts} />
		        </div>
		        <div className="grid-item">
		          <TopPosts posts={data.top_posts} />
		        </div>
		        <div className="grid-item">
		          <RecentComments comments={data.recent_comments} />
		        </div>
		      </div>
		    );
};

export default MainPage;
