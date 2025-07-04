import React, { useState } from 'react';
import './App.css';

function App() {
  const [userId, setUserId] = useState('');
  const [userRank, setUserRank] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loadingLeaderboard, setLoadingLeaderboard] = useState(false);
  const [loadingUser, setLoadingUser] = useState(false);
  const [userError, setUserError] = useState('');

  // Fetch Top 10 Leaderboard
  const fetchLeaderboard = async () => {
    setLoadingLeaderboard(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/leaderboard/top/');
      const data = await res.json();
      setLeaderboard(data);
    } catch (err) {
      setLeaderboard([]);
    }
    setLoadingLeaderboard(false);
  };

  // Fetch User Rank
  const fetchUserRank = async (e) => {
    e.preventDefault();
    setLoadingUser(true);
    setUserError('');
    setUserRank(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/leaderboard/rank/${userId}/`);
      console.log(res, "hello sanket");
      if (!res.ok) throw new Error('User not found');
      const data = await res.json();
      setUserRank(data);
    } catch (err) {
      setUserError('User not found or error fetching data');
    }
    setLoadingUser(false);
  };

  React.useEffect(() => {
    fetchLeaderboard();
  }, []);

  return (
    <div className="App">
      <h1>Game Leaderboard</h1>
      <section>
        <h2>Top 10 Leaderboard Rankings</h2>
        {loadingLeaderboard ? (
          <p>Loading...</p>
        ) : (
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry) => (
                <tr key={entry.user_id}>
                  <td>{entry.rank}</td>
                  <td>{entry.username}</td>
                  <td>{entry.total_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
      <section style={{ marginTop: '2rem' }}>
        <h2>User Rank Lookup</h2>
        <form onSubmit={fetchUserRank} className="user-rank-form">
          <input
            type="number"
            placeholder="Enter User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            required
          />
          <button type="submit" disabled={loadingUser}>Check Rank</button>
        </form>
        {loadingUser && <p>Loading...</p>}
        {userError && <p style={{ color: 'red' }}>{userError}</p>}
        {userRank && (
          <div className="user-rank-result">
            <p><strong>Username:</strong> {userRank.username}</p>
            <p><strong>Rank:</strong> {userRank.rank}</p>
            <p><strong>Score:</strong> {userRank.total_score}</p>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
