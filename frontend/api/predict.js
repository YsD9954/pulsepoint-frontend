export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const backendRes = await fetch('https://pulsepoint-backend.onrender.com/predict', {
        method: 'POST',
        headers: {
          'Content-Type': req.headers['content-type']
        },
        body: req.body,
      });

      const data = await backendRes.json();
      res.status(backendRes.status).json(data);
    } catch (error) {
      console.error("Proxy Error:", error);
      res.status(500).json({ error: 'Failed to connect to backend' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
