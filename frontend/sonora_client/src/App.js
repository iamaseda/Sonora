import './App.css';
import React, {useState, useEffect} from 'react'
// Backend not initialized in a virtual environment (pip3 env I believe)
function App() {

  const [members, setMembers] = useState([{}])
  // Fetch the backend API with useEffect
  useEffect(() => {
    // Fetching the main page route
    fetch("/members").then(
      response => response.json()
    ).then(
      members => {
        setMembers(members)
        console.log(members)
      }
    )
    // Empty array passed below so this only runs once
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        {/* if members is undefined, show loading in p tag else map over the array and display each element in a p tag with index as key */}
        {(typeof members.members === 'undefined') ? (
          <p>Loading...</p>
        ) : (
          members.members.map((member, i) => (
            <p key={i}>{member}</p>
          ))
        )}
      </header>
    </div>
  );
}

export default App;
