/* POS Activity Check — logique UI */
(function () {
    'use strict';

    var dropzone = document.getElementById('dropzone');
    var fileInput = document.getElementById('file-input');
    var fileInfo = document.getElementById('file-info');
    var fileNameEl = document.getElementById('file-name');
    var errorBox = document.getElementById('error-message');
    var errorText = document.getElementById('error-text');
    var analyzeAction = document.getElementById('analyze-action');
    var btnAnalyze = document.getElementById('btn-analyze');

    if (!dropzone) {
        return;
    }

    var currentFile = null;
    var currentFileId = null;

    function showError(message) {
        errorText.textContent = message;
        errorBox.classList.remove('d-none');
    }

    function hideError() {
        errorBox.classList.add('d-none');
        errorText.textContent = '';
    }

    function showFileLoaded(file) {
        fileNameEl.textContent = file.name;
        fileInfo.classList.remove('d-none');
        analyzeAction.classList.remove('d-none');
    }

    function resetState() {
        fileInfo.classList.add('d-none');
        analyzeAction.classList.add('d-none');
        hideError();
    }

    /* Dépose un fichier : validation côté client puis envoi vers /upload */
    function handleFile(file) {
        resetState();

        var ext = file.name.split('.').pop().toLowerCase();
        var allowed = ['xlsx', 'xls', 'pdf', 'csv'];
        if (allowed.indexOf(ext) === -1) {
            showError(
                'Format non supporté (".' + ext + '"). Formats acceptés : .xlsx, .xls, .pdf, .csv'
            );
            return;
        }
        if (file.size > 50 * 1024 * 1024) {
            showError('Fichier trop volumineux (max 50 Mo)');
            return;
        }

        currentFile = file;

        var formData = new FormData();
        formData.append('file', file);

        fetch('/upload', { method: 'POST', body: formData })
            .then(function (resp) {
                return resp.json().then(function (body) {
                    return { ok: resp.ok, body: body };
                });
            })
            .then(function (result) {
                if (result.ok && result.body.success) {
                    currentFileId = result.body.id;
                    showFileLoaded(file);
                } else {
                    currentFile = null;
                    currentFileId = null;
                    showError(result.body.error || 'Erreur lors du chargement du fichier');
                }
            })
            .catch(function () {
                currentFile = null;
                currentFileId = null;
                showError('Erreur réseau : impossible de contacter le serveur');
            });
    }

    /* Événements drag-and-drop */
    ['dragenter', 'dragover'].forEach(function (evtName) {
        dropzone.addEventListener(evtName, function (e) {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(function (evtName) {
        dropzone.addEventListener(evtName, function (e) {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', function (e) {
        var files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    /* Clic / clavier pour parcourir */
    dropzone.addEventListener('click', function () {
        fileInput.click();
    });

    dropzone.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            handleFile(fileInput.files[0]);
        }
    });

    /* Point d'extension utilisé par la phase analyse (US2) */
    window.analyzeCurrentFile = window.analyzeCurrentFile || function () {};

    window.posActivityCheck = {
        getCurrentFile: function () {
            return currentFile;
        },
        handleFile: handleFile,
        showError: showError
    };
})();
