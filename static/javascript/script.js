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
            let mode = document.querySelector('input[name="mode"]:checked').value;
            socket.emit('QuerySubmitted', { data: text, mode: mode});
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

    function fetch_collections() {
        $.get('/collections', function(items) {
            var $dropdown = $("#dropdown-list");
            $dropdown.empty();
            if (!items || items.length === 0) {
                $dropdown.append('<option value="">(No collections found)</option>');
            } else {
                items.forEach(function(item) {
                    $dropdown.append('<option value=' + item.name + '>' + item.name + '</option>');
                });
            }
        }).fail(function() {
            $("#dropdown-list").html('<option value="">Error loading collections</option>');
        });
    }

    function fetch_files(collection) {
        $.get('/files', {name: collection}, function(files) {
            var $list = $("#file-list");
            $list.empty();
            if(files.length === 0){
                $list.append("<li>(No files loaded)</li>");
            } else {
                files.forEach(function(file){
                    $list.append("<li>"+file+"</li>");
                });
            }
        }).fail(function() {
            $("#file-list").html("<li>Error fetching files.</li>");
        });
    }
    fetch_collections();
    $("#dropdown-list").on("change", function() {
        var selected = $(this).val();
        fetch_files(selected);
    });
    
});
