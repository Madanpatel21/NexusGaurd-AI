import http from 'k6/http';
export default function() {
  const res = http.post('http://localhost:8080/api/v1/telemetry', JSON.stringify({...}));
  if (res.status !== 200) throw new Error('Failed');
}
