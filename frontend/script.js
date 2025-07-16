document.getElementById('uploadForm').addEventListener('submit', async e => {
  e.preventDefault();
  const form = new FormData();
  form.append('csv_file', document.getElementById('csvFile').files[0]);
  document.getElementById('loader').style.display = 'block';
  document.getElementById('resultContainer').style.display = 'none';

  try {
    const res = await fetch('https://pulsepoint-backend.onrender.com/predict', {
      method: 'POST',
      body: form
    });
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();
    if (!Array.isArray(data)) throw new Error('Invalid response');

    const tbody = document.querySelector('#resultsTable tbody');
    tbody.innerHTML = '';
    data.forEach((r,i) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${r.date||i+1}</td>
        <td>${r.commits}</td>
        <td>${r.messages}</td>
        <td>${r.tickets_closed}</td>
        <td class="${r.at_risk===1?'at-risk':'stable'}">
          ${r.at_risk===1?'🔴 At-Risk':'🟢 Stable'}
        </td>`;
      tbody.appendChild(tr);
    });

    const labels = data.map(r=>r.date||'');
    const commits = data.map(r=>r.commits);
    const messages = data.map(r=>r.messages);
    const ctx = document.getElementById('activityChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels, datasets: [
          {label:'Commits', data: commits, backgroundColor:'#3498db'},
          {label:'Messages', data: messages, backgroundColor:'#2ecc71'}
        ]
      }
    });

    document.getElementById('resultContainer').style.display = 'block';
  } catch (err) {
    alert('Something went wrong: ' + err);
  } finally {
    document.getElementById('loader').style.display = 'none';
  }
});

document.getElementById('downloadBtn').onclick = () => {
  const rows = [
    ["Date","Commits","Messages","Tickets Closed","Status"],
    ...Array.from(document.querySelectorAll('#resultsTable tbody tr'))
      .map(tr => Array.from(tr.children).map(td => td.textContent))
  ];
  const csv = rows.map(r=>r.join(',')).join('\n');
  const a = document.createElement('a');
  a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
  a.download = 'results.csv';
  a.click();
};
