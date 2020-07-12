const FIXER_API_KEY = 'ea7f5d9b33e8b3b0d242b9b773e60ccb'
const FIXER_URL = 'http://data.fixer.io/api/latest';

function collectRates() {
    let price_rub = $('.price__RUB')
    let price_usd = $('.price__USD')
    $.ajax({
        url: FIXER_URL,
        data: {'access_key': FIXER_API_KEY},
        method: 'GET',
        success: function(resp) {
            if (resp.success) {
                let _e = resp.rates.RUB.toFixed(2);
                let _d = resp.rates.USD.toFixed(2);
                let usd_rate = (_e / _d).toFixed(2);
                let formatter = new Intl.NumberFormat('en')
                let price = price_rub.text().replace(/,/g, '');
                price_usd.text(formatter.format((price / usd_rate).toFixed(2)));
            } else {
                console.log('FIXER ERROR (' + resp.error.code + '): ' + resp.error.info);
                price_usd.html('&mdash;');
            }
        },
        error: function(error) {
            price_usd.html('&mdash;');
            console.log(error);
        }
    });
}

$(function() {
    // alert('Welcome!');
});