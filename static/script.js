const canvas = document.getElementById('art-wall');
const ctx = canvas.getContext('2d');
const submitBtn = document.getElementById('submit-btn');
const messageInput = document.getElementById('message-input');

canvas.width = window.innerWidth - 50;
canvas.height = 500;

// Randomize properties for each message
function drawMessage(message) {
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    const fontSize = Math.floor(Math.random() * (11 - 6 + 1)) + 6;
    const angle = Math.random() * (Math.PI / 2) - (Math.PI / 4); // -45 to 45 degrees
    const colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF'];
    const color = colors[Math.floor(Math.random() * colors.length)];

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.font = `${fontSize}px Arial`;
    ctx.fillStyle = color;
    ctx.fillText(message, 0, 0);
    ctx.restore();
}

// Fetch messages from the backend and draw them
async function loadMessages() {
    const response = await fetch('/get-messages');
    const data = await response.json();

    if (data.messages) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        data.messages.forEach(message => drawMessage(message));
    }
}

// Add a new message to the wall
submitBtn.addEventListener('click', async () => {
    const message = messageInput.value.trim();
    if (!message) {
        alert('Message cannot be empty!');
        return;
    }

    await fetch('/add-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
    });

    messageInput.value = '';
    await loadMessages();
});

// Load existing messages when the page loads
loadMessages();
