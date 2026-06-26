let pollingInterval = null;

async function startCamera() {
    await fetch('/api/start', { method: 'POST' });

    setTimeout(() => {
        const feed = document.getElementById('videoFeed');
        feed.src = '/video_feed?' + new Date().getTime();
        document.getElementById('videoOverlay').classList.add('hidden');
    }, 2000);  // tunggu 2 detik

    document.getElementById('btnStart').disabled = true;
    document.getElementById('btnStop').disabled = false;
    pollingInterval = setInterval(updateDetection, 300);
}


async function stopCamera() {
    await fetch('/api/stop', { method: 'POST' });

    document.getElementById('videoFeed').src = '';
    document.getElementById('videoOverlay').classList.remove('hidden');
    document.getElementById('btnStart').disabled = false;
    document.getElementById('btnStop').disabled = true;

    clearInterval(pollingInterval);
    document.getElementById('currentChar').textContent = '-';
    document.getElementById('confText').textContent = 'Confidence: 0%';
}

async function updateDetection() {
    try {
        const res = await fetch('/api/detection');
        const data = await res.json();

        document.getElementById('currentChar').textContent = data.char || '-';

        const conf = data.conf || 0;
        const confEl = document.getElementById('confText');
        confEl.textContent = `Confidence: ${conf}%`;
        confEl.style.color = '#818cf8';  // satu warna saja

        document.getElementById('kalimat').textContent = data.kalimat || '-';

    } catch (err) {
        console.error('Error:', err);
    }
}

async function clearKalimat() {
    await fetch('/api/clear', { method: 'POST' });
    document.getElementById('kalimat').textContent = '-';
    document.getElementById('currentChar').textContent = '-';
    document.getElementById('confText').textContent = 'Confidence: 0%';
}

async function hapusHuruf() {
    await fetch('/api/hapus', { method: 'POST' });
    const res = await fetch('/api/detection');
    const data = await res.json();
    document.getElementById('kalimat').textContent = data.kalimat || '-';
}

async function tambahSpasi() {
    await fetch('/api/spasi', { method: 'POST' });
    const res = await fetch('/api/detection');
    const data = await res.json();
    document.getElementById('kalimat').textContent = data.kalimat || '-';
}