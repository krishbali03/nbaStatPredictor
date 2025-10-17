import { useState } from "react";

function App() {
  const [player, setPlayer] = useState("");
  const [stats, setStats] = useState({ points: true, rebounds: true, assists: true });
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ player, stats }),
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div>
      <h1>NBA Stat Predictor</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Player Name" value={player} onChange={(e) => setPlayer(e.target.value)} />
        <label>
          <input type="checkbox" checked={stats.points} onChange={(e) => setStats({ ...stats, points: e.target.checked })} />
          Points
        </label>
        <label>
          <input type="checkbox" checked={stats.rebounds} onChange={(e) => setStats({ ...stats, rebounds: e.target.checked })} />
          Rebounds
        </label>
        <label>
          <input type="checkbox" checked={stats.assists} onChange={(e) => setStats({ ...stats, assists: e.target.checked })} />
          Assists
        </label>
        <button type="submit">Predict</button>
      </form>
      {result && (
        <div>
          <h2>Results for {result.player}</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
