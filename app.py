from project import app
import os

false_in_production = os.environ.get('ENV') != 'production'
port = os.environ.get('PORT') or 5000

if __name__ == '__main__':
    app.run(port=port, debug=false_in_production,threaded=false_in_production)
