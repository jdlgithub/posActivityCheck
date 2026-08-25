import logging
import uuid

from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename

from services.validator import get_file_extension, is_allowed_extension, exceeds_max_size
from services.file_parser import parse_file
from services.statistics import calculate_statistics
from models.fichier_analyse import FichierAnalyse, SUPPORTED_FORMATS
from models.statistiques_globales import StatistiquesGlobales

logger = logging.getLogger('posactivity.routes')


def register_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload():
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400

        file = request.files['file']

        if not file.filename:
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400

        filename = secure_filename(file.filename)
        extension = get_file_extension(filename)

        if not is_allowed_extension(extension):
            formats_lisibles = ', '.join(f'.{f}' for f in sorted(SUPPORTED_FORMATS))
            return jsonify({
                'error': (
                    f"Format non supporté ('.{extension}'). "
                    f"Formats acceptés: {formats_lisibles}"
                )
            }), 400

        raw = file.read()
        size_bytes = len(raw)
        file.seek(0)

        if exceeds_max_size(size_bytes, app.config['MAX_CONTENT_LENGTH']):
            return jsonify({'error': 'Fichier trop volumineux (max 50 Mo)'}), 413

        try:
            fichier = FichierAnalyse.from_upload(filename, size_bytes)
        except ValueError as exc:
            logger.warning('Upload refusé: %s', exc)
            return jsonify({'error': str(exc)}), 400

        # Conservation du contenu en mémoire pour l'étape d'analyse (pas de stockage disque)
        app.config.setdefault('UPLOADED_FILES', {})[fichier.id] = {
            'fichier': fichier,
            'contenu': raw,
        }

        logger.info(
            "Fichier chargé: id=%s nom=%s format=%s taille=%d octets",
            fichier.id, fichier.nom_fichier, fichier.format, fichier.taille_bytes,
        )

        return jsonify({
            'success': True,
            **fichier.to_dict(),
        })

    @app.route('/analyze/<file_id>', methods=['POST'])
    def analyze(file_id):
        stored = app.config.get('UPLOADED_FILES', {}).get(file_id)
        if stored is None:
            return jsonify({'error': 'Fichier introuvable ou session expirée. Rechargez le fichier.'}), 404

        from io import BytesIO
        fichier = stored['fichier']
        stream = BytesIO(stored['contenu'])

        try:
            data = parse_file(stream, fichier.nom_fichier)
            stats = StatistiquesGlobales.from_dict(calculate_statistics(data))
        except ValueError as exc:
            # Erreur métier lisible : format/contenu invalide
            logger.warning("Analyse refusée pour %s: %s", fichier.nom_fichier, exc)
            return jsonify({'error': str(exc)}), 422
        except Exception as exc:  # noqa: BLE001 — erreur technique inattendue
            logger.exception("Erreur d'analyse pour %s", fichier.nom_fichier)
            return jsonify({'error': f"Erreur lors de l'analyse: {exc}"}), 500

        return jsonify({'success': True, 'statistics': stats.to_dict()})

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Page non trouvée'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Erreur interne du serveur'}), 500

    @app.errorhandler(413)
    def payload_too_large(error):
        return jsonify({'error': 'Fichier trop volumineux (max 50 Mo)'}), 413
