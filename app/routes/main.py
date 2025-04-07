"""Main routes for the translation web interface."""
import os
import logging
from flask import Blueprint, render_template, request, jsonify, current_app, Response, stream_with_context
from werkzeug.utils import secure_filename
import json
from app.utils.translator import TurkishToKazakhTranslator

bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'txt', 'docx', 'pdf'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@bp.route('/translate', methods=['POST'])
def translate():
    """Handle translation requests."""
    try:
        # Initialize translator
        translator = TurkishToKazakhTranslator()
        
        @stream_with_context
        def generate_progress():
            try:
                # Check for text input first
                if request.form.get('text'):
                    text = request.form['text'].strip()
                    if text:
                        # Create temporary files
                        temp_input = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_input.txt')
                        temp_output = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_output.txt')
                        
                        try:
                            # Write input text
                            with open(temp_input, 'w', encoding='utf-8') as f:
                                f.write(text)
                            
                            # Translate and stream progress
                            for progress_info in translator.translate(temp_input, temp_output):
                                yield f"data: {json.dumps(progress_info)}\n\n"
                            
                        except Exception as e:
                            logger.error(f"Translation error: {str(e)}")
                            yield f"data: {json.dumps({'error': 'Translation failed'})}\n\n"
                        finally:
                            # Clean up temporary files
                            if os.path.exists(temp_input):
                                os.remove(temp_input)
                            if os.path.exists(temp_output):
                                os.remove(temp_output)
                
                # Check for file upload
                elif request.files.get('file'):
                    file = request.files['file']
                    if file.filename == '':
                        yield f"data: {json.dumps({'error': 'No file selected'})}\n\n"
                        return
                    
                    if not allowed_file(file.filename):
                        yield f"data: {json.dumps({'error': 'Invalid file format'})}\n\n"
                        return
                    
                    try:
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        
                        # Create output path
                        output_filename = f"translated_{filename}"
                        output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], output_filename)
                        
                        # Translate and stream progress
                        for progress_info in translator.translate(filepath, output_path):
                            yield f"data: {json.dumps(progress_info)}\n\n"
                        
                    except Exception as e:
                        logger.error(f"Translation error: {str(e)}")
                        yield f"data: {json.dumps({'error': 'Translation failed'})}\n\n"
                    finally:
                        # Clean up files
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        if os.path.exists(output_path):
                            os.remove(output_path)
                
                else:
                    yield f"data: {json.dumps({'error': 'No input provided'})}\n\n"
            
            except Exception as e:
                logger.error(f"Translation error: {str(e)}")
                yield f"data: {json.dumps({'error': 'Translation failed'})}\n\n"
        
        return Response(generate_progress(), mimetype='text/event-stream')
    
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500 