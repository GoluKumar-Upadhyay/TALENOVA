export function StatStrip() {
  const stats = [["15+", "Applied AI domains"], ["4", "Ways to build proof"], ["1:1", "Mentorship mindset"], ["100%", "Portfolio focused"]];
  return <div className="stat-strip">{stats.map(([value, label]) => <div key={label} className="stat-item"><strong>{value}</strong><span>{label}</span></div>)}</div>;
}

