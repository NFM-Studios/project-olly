(function () {
    'use strict';

    var badge = document.getElementById('notification-badge');
    if (!badge || !window.WebSocket) {
        return;
    }

    var scheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    var ws = new WebSocket(scheme + window.location.host + '/ws/notifications/');

    ws.onmessage = function (event) {
        var data;
        try {
            data = JSON.parse(event.data);
        } catch (e) {
            return;
        }
        if (data.action === 'notification') {
            var count = parseInt(badge.dataset.count || '0', 10) + 1;
            badge.dataset.count = String(count);
            badge.textContent = String(count);
            badge.classList.remove('d-none');
        }
    };
})();