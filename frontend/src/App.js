import React, { useState } from 'react';
import './App.css';

function App() {
  // Auth states
  const [token, setToken] = useState(localStorage.getItem('jwtToken') || '');
  const [loginUser, setLoginUser] = useState('');
  const [loginPass, setLoginPass] = useState('');
  const [loginError, setLoginError] = useState('');
  const [loginLoading, setLoginLoading] = useState(false);

  // User states
  const [userId, setUserId] = useState('');
  const [userRank, setUserRank] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loadingLeaderboard, setLoadingLeaderboard] = useState(false);
  const [loadingUser, setLoadingUser] = useState(false);
  const [userError, setUserError] = useState('');

  // Submit Score states
  const [scoreUserId, setScoreUserId] = useState('');
  const [scoreValue, setScoreValue] = useState('');
  const [scoreGameMode, setScoreGameMode] = useState('');
  const [scoreLoading, setScoreLoading] = useState(false);
  const [scoreResult, setScoreResult] = useState(null);
  const [scoreError, setScoreError] = useState('');

  // Login handler
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginLoading(true);
    setLoginError('');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: loginUser, password: loginPass })
      });
      if (!res.ok) throw new Error('Invalid credentials');
      const data = await res.json();
      setToken(data.access);
      localStorage.setItem('jwtToken', data.access);
      setLoginUser('');
      setLoginPass('');
    } catch (err) {
      setLoginError('Login failed: ' + err.message);
    }
    setLoginLoading(false);
  };

  // Logout handler
  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('jwtToken');
  };

  // Fetch Top 10 Leaderboard (with JWT)
  const fetchLeaderboard = async () => {
    setLoadingLeaderboard(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/leaderboard/top/', {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
      });
      if (res.status === 401) throw new Error('Unauthorized');
      const data = await res.json();
      setLeaderboard(data);
    } catch (err) {
      setLeaderboard([]);
    }
    setLoadingLeaderboard(false);
  };

  // Fetch User Rank (with JWT)
  const fetchUserRank = async (e) => {
    e.preventDefault();
    setLoadingUser(true);
    setUserError('');
    setUserRank(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/leaderboard/rank/${userId}/`, {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
      });
      if (!res.ok) throw new Error('User not found or unauthorized');
      const data = await res.json();
      setUserRank(data);
    } catch (err) {
      setUserError('User not found or error fetching data');
    }
    setLoadingUser(false);
  };

  // Submit Score handler
  const handleSubmitScore = async (e) => {
    e.preventDefault();
    setScoreLoading(true);
    setScoreError('');
    setScoreResult(null);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/leaderboard/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
          user_id: scoreUserId,
          score: scoreValue,
          game_mode: scoreGameMode
        })
      });
      if (!res.ok) throw new Error('Failed to submit score');
      const data = await res.json();
      setScoreResult(data);
    } catch (err) {
      setScoreError('Error submitting score');
    }
    setScoreLoading(false);
  };

  React.useEffect(() => {
    if (token) fetchLeaderboard();
    else setLeaderboard([]);
  }, [token]);

  return (
    <div className="App">
      <h1>Game Leaderboard</h1>
      {!token ? (
        <section style={{ marginBottom: '2rem' }}>
          <h2>Login</h2>
          <form onSubmit={handleLogin} className="login-form">
            <input
              type="text"
              placeholder="Username"
              value={loginUser}
              onChange={e => setLoginUser(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={loginPass}
              onChange={e => setLoginPass(e.target.value)}
              required
            />
            <button type="submit" disabled={loginLoading}>Login</button>
          </form>
          {loginError && <p style={{ color: 'red' }}>{loginError}</p>}
        </section>
      ) : (
        <button onClick={handleLogout} style={{ float: 'right' }}>Logout</button>
      )}
      {token && (
        <>
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
          <section style={{ marginTop: '2rem' }}>
            <h2>Submit User Score</h2>
            <form onSubmit={handleSubmitScore} className="submit-score-form">
              <input
                type="number"
                placeholder="User ID"
                value={scoreUserId}
                onChange={e => setScoreUserId(e.target.value)}
                required
              />
              <input
                type="number"
                placeholder="Score"
                value={scoreValue}
                onChange={e => setScoreValue(e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="Game Mode"
                value={scoreGameMode}
                onChange={e => setScoreGameMode(e.target.value)}
                required
              />
              <button type="submit" disabled={scoreLoading}>Submit</button>
            </form>
            {scoreLoading && <p>Submitting...</p>}
            {scoreError && <p style={{ color: 'red' }}>{scoreError}</p>}
            {scoreResult && (
              <div className="score-result">
                <p><strong>User ID:</strong> {scoreResult.user_id}</p>
                <p><strong>New Total:</strong> {scoreResult.new_total}</p>
                <p><strong>Rank:</strong> {scoreResult.rank}</p>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}

export default App;
