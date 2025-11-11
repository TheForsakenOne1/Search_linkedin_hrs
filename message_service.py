#!/usr/bin/env python3
"""
Flask API service for message generation
Used by n8n workflow to generate personalized LinkedIn messages
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from message_generator import MessageGenerator
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for n8n integration

# Initialize message generator
generator = MessageGenerator()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'LinkedIn Message Generator API',
        'version': '1.0.0'
    })


@app.route('/generate-message', methods=['POST'])
def generate_message():
    """
    Generate a single personalized message

    Request body:
    {
        "profile": {
            "name": "John Doe",
            "title": "HR Manager at Google",
            "location": "San Francisco",
            "profile_url": "https://linkedin.com/in/johndoe"
        },
        "scenario": "job_seeker",
        "custom_data": {
            "your_role": "Software Engineer",
            "years": "5",
            "skills": "Python, React",
            "industry": "technology"
        }
    }
    """
    try:
        data = request.get_json()

        if not data or 'profile' not in data:
            return jsonify({'error': 'Missing profile data'}), 400

        profile = data['profile']
        scenario = data.get('scenario', 'job_seeker')
        custom_data = data.get('custom_data', {})

        # Generate message
        message_data = generator.generate_message(profile, scenario, custom_data)

        return jsonify({
            'success': True,
            'data': message_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/generate-bulk', methods=['POST'])
def generate_bulk():
    """
    Generate messages for multiple profiles

    Request body:
    {
        "profiles": [...],
        "scenario": "job_seeker",
        "custom_data": {...}
    }
    """
    try:
        data = request.get_json()

        if not data or 'profiles' not in data:
            return jsonify({'error': 'Missing profiles data'}), 400

        profiles = data['profiles']
        scenario = data.get('scenario', 'job_seeker')
        custom_data = data.get('custom_data', {})

        # Generate messages
        messages = generator.generate_bulk_messages(profiles, scenario, custom_data)

        # Get statistics
        stats = generator.get_message_statistics(messages)

        return jsonify({
            'success': True,
            'data': {
                'messages': messages,
                'statistics': stats
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/scenarios', methods=['GET'])
def get_scenarios():
    """Get available message scenarios"""
    return jsonify({
        'scenarios': list(generator.templates.keys()),
        'default': 'job_seeker'
    })


@app.route('/generate-from-file', methods=['POST'])
def generate_from_file():
    """
    Generate messages from scraped data file

    Request body:
    {
        "file_path": "/path/to/linkedin_hr_results.json",
        "scenario": "job_seeker",
        "custom_data": {...},
        "output_file": "/path/to/output.json"
    }
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path')

        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Invalid file path'}), 400

        # Read profiles from file
        import json
        with open(file_path, 'r') as f:
            file_data = json.load(f)
            profiles = file_data.get('profiles', [])

        scenario = data.get('scenario', 'job_seeker')
        custom_data = data.get('custom_data', {})

        # Generate messages
        messages = generator.generate_bulk_messages(profiles, scenario, custom_data)

        # Save to output file if specified
        output_file = data.get('output_file')
        if output_file:
            generator.export_messages(messages, output_file)

        # Get statistics
        stats = generator.get_message_statistics(messages)

        return jsonify({
            'success': True,
            'data': {
                'total_generated': len(messages),
                'statistics': stats,
                'output_file': output_file
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('MESSAGE_SERVICE_PORT', 5000))
    print(f"""
╔══════════════════════════════════════════════════════════╗
║     LinkedIn Message Generator API Service              ║
║                                                          ║
║  Running on http://localhost:{port}                    ║
║                                                          ║
║  Endpoints:                                              ║
║    GET  /health              - Health check             ║
║    GET  /scenarios           - List scenarios           ║
║    POST /generate-message    - Generate single message  ║
║    POST /generate-bulk       - Generate bulk messages   ║
║    POST /generate-from-file  - Generate from file       ║
╚══════════════════════════════════════════════════════════╝
""")

    app.run(host='0.0.0.0', port=port, debug=True)
