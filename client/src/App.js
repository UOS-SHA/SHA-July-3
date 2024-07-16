import React, { useState } from 'react';
import Signup from './Signup';
import MainPage from './MainPage/Main.js'

function App() {
	const [currentRoute, setCurrentRoute] = useState(window.location.pathname);

	const renderContent = () => {
		if (currentRoute === '/signup') {
			return <Signup />;
		} else {
			return <MainPage />;
		}
	};

	return (
		<div className="App">
			{renderContent()}
		</div>
	);
}

export default App;
