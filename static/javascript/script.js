$(document).ready(function () {
    const socket = io.connect('http://127.0.0.1:5000/chat');

    let currentResponseEl = null;  // stores reference to latest <p> to append text to

    $('#submit-message-btn').on('click', function () {
        const text = $('#text-input').val().trim();

        if (text !== '') {
            // 1. Clear input
            $('#text-input').val('');

            var newTextArea = $('<div class="text-area user"></div>');
            const newQueryBox = $('<p class="query-line"></p>').text(text);
            newTextArea.append(newQueryBox);
            $('#response-container').append(newTextArea);

            var newTextArea = $('<div class="text-area server"></div>');
            const newResponse = $('<p class="response-line"></p>').text('Thinking...');;
            newTextArea.append(newResponse);
            $('#response-container').append(newTextArea);

            // 4. Save reference for streaming chunks
            currentResponseEl = newResponse;

            // 5. Emit to server
            socket.emit('QuerySubmitted', { data: text });
        }
    });

    socket.on('ResponseReady', function (data) {
        // Append new chunk to the latest <p> element
        if (currentResponseEl) {
            const existingText = currentResponseEl.text();
            if (existingText === 'Thinking...')
                currentResponseEl.text('');
            currentResponseEl.text(existingText + data.data);
        }
    });
});
