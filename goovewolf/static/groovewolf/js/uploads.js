/**
     * StackOverflow Snippet
     */
    function getCookie(name) {

        var value = '; ' + document.cookie,
            parts = value.split('; ' + name + '=');

        if (parts.length == 2) {
            return parts.pop().split(';').shift();
        }
    }
    /**
     * Neto's Snippet
     */
    function getSize(bytes, inmebibites) {
        var ui = 0, units, factor;

        units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        factor = 1000;

        if (inmebibites) {
            units = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
            factor = 1024;
        }

        if (bytes > factor) ui = Math.floor(Math.log(bytes) / Math.log(factor));

        return {
            value: Math.round((bytes / Math.pow(factor, ui) + 0.00001) * 100) / 100,
            unit: units[ui]
        };
    }

    (function($) {
        var input = document.getElementById('musicfiles'),
            submitter = $('#submitter'),
            templates = $($('template').html()),
            uploadstable = $('.uploads tbody'),
            uploadStack = [],
            list = $('#list'),
            uploadsCount = 0,
            maxConcurrentUploads = 3,
            currentlyUploading = 0;

        console.log('que sueño');

        submitter.click(startUpload);
        $(input).change(quequefiles);

        function newMusicUploadRequest(file, filenode) {
            var request = new XMLHttpRequest(),
                form = new FormData(),
                progress = filenode.find('.progress'),
                response;

            form.append('song', file);

            request.upload.onprogress = function(e) {
                if (e.lengthComputable) {
                    progress.css({width: (e.loaded/e.total * 100) + '%'});
                } else {
                    console.log('The file size is not computable =(...');
                }
            };

            request.upload.onabort = function(e) {
                console.log('File upload aborted');
            };
            request.upload.onerror = function(e) {
                console.log('File upload error');
            };

            request.upload.onloadend = function(e) {
                console.log('File upload terminated');
            };

            request.upload.onloadstart = function(e) {
                currentlyUploading += 1;
                console.log(currentlyUploading, maxConcurrentUploads);
                if (currentlyUploading < maxConcurrentUploads) {
                    startUpload();
                }
            };

            request.onreadystatechange = function() {
                console.log(request.readyState);
                if (request.readyState == 2) {
                    currentlyUploading--;
                    if (currentlyUploading < maxConcurrentUploads) {
                        startUpload();
                    }
                }
                if (request.readyState == 4) {
                    try {
                        response = JSON.parse(request.response);
                    } catch (e) {
                        response = {
                            success: false,
                            reason: 'Unknown error occurred: [' + request.responseText + ']'
                        };
                    }
                    if (response.success) {
                        filenode.find('.action').html('<i class="fa fa-check"></i>');
                    } else {
                        filenode.find('.action').html('<i class="fa fa-exclamation-circle"></i>').attr('title', 'Algo salió mal =(...');
                    }
                }
            };

            request.open('POST', window['musicupload_url'], true);
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            uploadStack.push({
                request: request,
                form: form,
                filenode: filenode
            });
        }

        function startUpload() {

            var udata = uploadStack.shift(),
                filenode;

            if (udata) {
                console.log('Satrting upload ' + udata.form);
                filenode = udata.filenode;
                if (filenode.hasClass('hidden')) {
                    startUpload();
                    return;
                }
                udata.form.append('name', filenode.find('.song-name').val());
                udata.form.append('artist', filenode.find('.artist-id').val());

                filenode.find('.song-name').attr('disabled', true);
                filenode.find('.ui-autocomplete-input').attr('disabled', true);
                udata.request.send(udata.form);
            } else {
                console.log('No había cola');
            }
        }

        function quequefiles() {
            var files = input.files,
                template = templates.find('.upload-feedback'),
                regex = /mp3|m4a|audio\/mpeg/i,
                fi = 0,
                file, filenode, size, songartistID, songname;

            for (; fi < files.length; fi++) {
                file = files[fi];
                size = getSize(file.size, false);
                filenode = template.clone();
                songartistID = 'song-artist' + uploadsCount;
                uploadsCount++;

                filenode.data({
                    songID: false,
                    artistID: songartistID,
                    uploadN: uploadsCount
                });

                if (!regex.test(file.type)) {
                    // TODO: Alert/show some feedback here
                    console.log('Saltando archivo: ' + file.type);
                    continue;
                }

                songname = file.name.split('.');
                songname.pop();
                songname = songname[0].split(/-/);
                songname = songname[songname.length - 1].trim();
                songname = songname.split('_').join(' ');

                filenode.find('.filename').text(file.name);
                filenode.find('.size').text(size.value + size.unit);
                filenode.find('.song-name').val(songname);

                filenode.find('.ui-autocomplete-input').attr('id', songartistID + '_text');
                filenode.find('.ui-autocomplete-value').attr('id', songartistID);

                filenode.find('.action button').click(function() {
                    $(this).closest('tr').addClass('hidden');
                });

                newMusicUploadRequest(file, filenode);
                uploadstable.append(filenode);
            }
        }
    })(jQuery);