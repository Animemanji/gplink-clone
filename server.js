const express = require('express');
const path = require('path');
const dotenv = require('dotenv');

// Initialize dotenv to manage environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/ad_page', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'ad_page.html'));
});

app.get('/redirect', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'redirect_page.html'));
});

// Handle 404 errors
app.use((req, res, next) => {
    res.status(404).sendFile(path.join(__dirname, 'public', '404.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});