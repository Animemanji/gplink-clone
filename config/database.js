const urls = {};

// Generate a random string for the short URL
function generateShortCode(length = 6) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

// Save a new URL with a generated short code
function saveUrl(originalUrl) {
    const shortCode = generateShortCode();
    urls[shortCode] = originalUrl;
    return shortCode;
}

// Retrieve the original URL by its short code
function getUrl(shortCode) {
    return urls[shortCode];
}

// Delete a URL by its short code
function deleteUrl(shortCode) {
    delete urls[shortCode];
}

module.exports = {
    saveUrl,
    getUrl,
    deleteUrl
};