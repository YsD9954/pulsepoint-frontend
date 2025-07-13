export const config = {
  api: {
    bodyParser: false, // ⛔ Disable default body parsing to handle FormData manually
  },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const backendRes = await fetch('https://pulsepoint-backend.onrender.com/predict', {
      method: 'POST',
      headers: {
        'Content-Type': req.headers['content-type'], // maintain boundary info
      },
      body: req, // ✅ pipe raw request stream
    });

    const data = await backendRes.json();
    res.status(backendRes.status).json(data);
  } catch (error) {
    console.error("Proxy Error:", error);
    res.status(500).json({ error: 'Failed to connect to backend' });
  }
}
