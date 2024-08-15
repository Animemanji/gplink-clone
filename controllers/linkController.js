const { saveUrl, getUrl } = require('./database');

// Function to handle the creation of a shortened URL
function createShortLink(req, res) {
    const originalUrl = req.body.url;

    if (!originalUrl) {
        return res.status(400).send('URL is required');
    }

    // Save the original URL and get the short code
    const shortCode = saveUrl(originalUrl);

    // Generate the short link using the current domain and short code
    const shortLink = `${req.protocol}://${req.get('host')}/ad/${shortCode}`;

    res.status(201).json({ shortLink });
}

// Function to handle the redirection to the original URL
function redirectToOriginalUrl(req, res) {
    const shortCode = req.params.shortCode;

    // Retrieve the original URL using the short code
    const originalUrl = getUrl(shortCode);

    if (!originalUrl) {
        return res.status(404).send('URL not found');
    }

    // Redirect the user to the original URL
    res.redirect(originalUrl);
}

module.exports = {
    createShortLink,
    redirectToOriginalUrl
};