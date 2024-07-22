import React, { useState } from 'react';
import MainPage from './MainPage/Main.js';
import Post from './Post/Post.js';
import User from './User/User.js';
import Error from './Error.js';
import Banner from './Banner.js';

function App() {
	const [currentRoute, setCurrentRoute] = useState(window.location.pathname);

	const renderContent = () => {
		if (currentRoute === '/signup') {
			return (<Signup />);
		} else if (currentRoute.startsWith('/post/')) {
			const match = currentRoute.match(/^\/post\/(\d+)$/);
			if (match) {
				return (<Post postId={parseInt(match[1], 10)} />);
			}
		} else if (currentRoute.startsWith('/user/')) {
			const match = currentRoute.match(/^\/user\/(\d+)$/);
			if (match) {
				return (<User userId={parseInt(match[1], 10)} />);
			}
		} else if (currentRoute === '/') {
			return (<MainPage />);
		}
		return (<Error />);
	};

	return (
		<div className="App">
		<Banner />
		{renderContent()}
		</div>
	);
}

export default App;
