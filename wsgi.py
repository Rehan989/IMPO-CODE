from main import app  # Adjust the import to match your Flask application's module name

if __name__ == "_main_":
    # Running the Flask app in debug mode is not recommended for production.
    app.run()  # You can specify host and port if needed, default is localhost and port 5000
