import os

def create_flask_structure(base_dir="flask-app"):
    folders = [
        "app",
        "app/static/css",
        "app/static/js",
        "app/static/images",
        "app/templates",
        "app/utils",
        "dataset",
        "instance",
        "tests",
    ]

    files = {
        "run.py": "from app import create_app\n\napp = create_app()\n\nif __name__ == '__main__':\n    app.run(debug=True)",
        "app/__init__.py": "from flask import Flask\n\ndef create_app():\n    app = Flask(__name__)\n    app.config.from_pyfile('../instance/config.py')\n\n    # Register Blueprints\n    from app.routes import bp\n    app.register_blueprint(bp)\n\n    return app",
        "app/routes.py": "from flask import Blueprint, render_template, request\n\nbp = Blueprint('main', __name__)\n\n@bp.route('/')\ndef index():\n    return render_template('index.html')\n\n@bp.route('/recommend', methods=['POST'])\ndef recommend():\n    user_input = request.form.get('query')\n    # Add your recommendation logic\n    recommendations = []\n    return render_template('result.html', recommendations=recommendations)",
        "app/utils/data_loader.py": "# Add your dataset loading logic\nimport pandas as pd\n\ndef load_dataset(path):\n    return pd.read_csv(path)",
        "app/templates/index.html": "<!DOCTYPE html>\n<html>\n<head>\n    <title>Music Recommendation</title>\n</head>\n<body>\n    <h1>Welcome to Music Recommendation System</h1>\n    <form action='/recommend' method='POST'>\n        <input type='text' name='query' placeholder='Enter genre or track'>\n        <button type='submit'>Get Recommendations</button>\n    </form>\n</body>\n</html>",
        "instance/config.py": "SECRET_KEY = 'your-secret-key'\nDEBUG = True",
        "README.md": "# Flask App\n\nBasic Flask application structure.",
    }

    # Create folders
    for folder in folders:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

    # Create files
    for file_name, content in files.items():
        file_path = os.path.join(base_dir, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)

    print(f"Flask structure created at: {os.path.abspath(base_dir)}")


# Run the function
create_flask_structure()