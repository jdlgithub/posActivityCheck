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

    /* Seuils de couleur professionnels (T031) */
    var SEUILS = [
        { min: 80, classe: 'stat-good', libelle: 'bg-success' },
        { min: 50, classe: 'stat-warn', libelle: 'bg-warning' },
        { min: 0,  classe: 'stat-bad',  libelle: 'bg-danger' }
    ];

    function couleurPourTaux(valeur) {
        for (var i = 0; i < SEUILS.length; i++) {
            if (valeur >= SEUILS[i].min) {
                return SEUILS[i];
            }
        }
        return SEUILS[SEUILS.length - 1];
    }

    /* Popup toast "Analyse terminée" (T030) */
    function afficherPopupSucces() {
        var conteneur = document.getElementById('toast-container');
        if (!conteneur || typeof bootstrap === 'undefined') {
            return;
        }
        var element = document.createElement('div');
        element.className = 'toast align-items-center text-bg-success border-0';
        element.setAttribute('role', 'status');
        element.setAttribute('aria-live', 'polite');
        element.innerHTML =
            '<div class="d-flex">' +
            '<div class="toast-body fw-semibold"><i class="bi bi-check-circle-fill me-2"></i>Analyse termin\u00e9e</div>' +
            '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Fermer"></button>' +
            '</div>';
        conteneur.appendChild(element);
        var toast = new bootstrap.Toast(element, { delay: 3000 });
        toast.show();
        element.addEventListener('hidden.bs.toast', function () {
            element.remove();
        });
    }

    function appliquerCouleur(id, valeur) {
        var el = document.getElementById(id);
        if (!el) {
            return;
        }
        el.textContent = valeur.toFixed(1) + ' %';
        var info = couleurPourTaux(valeur);
        var carte = el.closest('.card');
        carte.classList.remove('border-success', 'border-warning', 'border-danger');
        carte.classList.add(info.libelle.replace('bg-', 'border-'));
        el.classList.remove('text-success', 'text-warning', 'text-danger');
        el.classList.add(info.libelle.replace('bg-', 'text-'));
    }

    function afficherStatistiques(stats) {
        appliquerCouleur('stat-attente', stats.taux_pos_attente);
        appliquerCouleur('stat-valides', stats.taux_pos_valides);
        appliquerCouleur('stat-conformes', stats.taux_pos_conformes);
        appliquerCouleur('stat-agents', stats.taux_agents_performants);
        document.getElementById('results-section').classList.remove('d-none');
        document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
    }

    /* Lancement de l'analyse */
    function lancerAnalyse() {
        if (!currentFileId) {
            showError("Aucun fichier chargé. Déposez d'abord un fichier.");
            return;
        }
        hideError();
        btnAnalyze.disabled = true;
        btnAnalyze.innerHTML =
            '<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>Analyse en cours...';

        fetch('/analyze/' + encodeURIComponent(currentFileId), { method: 'POST' })
            .then(function (resp) {
                return resp.json().then(function (body) {
                    return { ok: resp.ok, body: body };
                });
            })
            .then(function (result) {
                btnAnalyze.disabled = false;
                btnAnalyze.innerHTML =
                    '<i class="bi bi-play-fill me-2" aria-hidden="true"></i>Démarrer l\'analyse';
                if (result.ok && result.body.success) {
                    afficherStatistiques(result.body.statistics);
                    afficherPopupSucces();
                } else {
                    showError(result.body.error || "Erreur lors de l'analyse du fichier");
                }
            })
            .catch(function () {
                btnAnalyze.disabled = false;
                btnAnalyze.innerHTML =
                    '<i class="bi bi-play-fill me-2" aria-hidden="true"></i>Démarrer l\'analyse';
                showError('Erreur réseau : impossible de contacter le serveur');
            });
    }

    if (btnAnalyze) {
        btnAnalyze.addEventListener('click', lancerAnalyse);
    }

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

    window.posActivityCheck = {
        getCurrentFile: function () {
            return currentFile;
        },
        handleFile: handleFile,
        showError: showError,
        couleurPourTaux: couleurPourTaux,
        lancerAnalyse: lancerAnalyse
    };
})();
