const { getUrl } = require('./database');

// Function to display the ad page with the countdown
function showAdPage(req, res) {
    const shortCode = req.params.shortCode;
    const originalUrl = getUrl(shortCode);

    if (!originalUrl) {
        return res.status(404).send('URL not found');
    }

    // Render the ad page, passing the original URL to be used after the countdown
    res.render('ad_page', {
        redirect_url: `/redirect/${shortCode}`,
        shortCode: shortCode
    });
}

// Function to handle the final redirection after the ad is displayed
function handleRedirect(req, res) {
    const shortCode = req.params.shortCode;
    const originalUrl = getUrl(shortCode);

    if (!originalUrl) {
        return res.status(404).send('URL not found');
    }

    // Redirect the user to the original URL
    res.redirect(originalUrl);
}

module.exports = {
    showAdPage,
    handleRedirect
};