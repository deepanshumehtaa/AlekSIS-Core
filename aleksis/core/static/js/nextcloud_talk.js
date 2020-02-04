var POLL_INTERVAL = 500;
var w = null;

function poll() {
    $.ajax({
        url: Urls.pollNextcloudTalk(),
    }).done(function (data) {
        if (data.done) {
            console.log("Polling done");

            // Redirect to third-party services home view
            window.location.href = Urls.thirdPartyServices();
            w.close();
        } else {
            window.setTimeout(poll, POLL_INTERVAL);
        }
    }).fail(function () {
        window.setTimeout(poll, POLL_INTERVAL);
    })
}

$(document).ready(function () {
    // Open login URL
    var loginData = getJSONScript("login_data");
    w = window.open(loginData.login);

    console.log("Start polling");
    poll();
});
