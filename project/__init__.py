from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from project.email_providers import SendGridEmail, SparkPostEmail

app = Flask(__name__)
CORS(app)

@app.route('/api')
def root():
    # Confirmation app is running, for testing or admin
    return ('The application is up and running! You should probabally be trying to send your JSON to /send!')

@app.route('/api/send', methods=['POST', 'GET'])
def send_email():
    # Simple prompt to POST
    if request.method == 'GET':
        return 'POST your JSON here in the form of a dicionary with the keys to, from, cc, bcc, subject, and body. To, cc, and bcc should be arrays of email addresses.'
    # Creating JSON dict of request data 
    request_json = request.get_json()
    # Send back 400 with error if POSTing without from or to emails
    if not request_json.get("to") or not request_json.get("from"):
        error = {'error': 'Must have a sending and receiving address.'}
        return jsonify(error), 400
    # Setup vars for dict objects to easily call if an email provider fails
    from_email = request_json['from']
    to_email_list = request_json['to']
    cc_email_list = request_json.get('cc') or []
    bcc_email_list = request_json.get('bcc') or []
    subject = request_json.get('subject') or "No Subject"
    content = request_json.get('content') or "No body text"
     # Try SparkPost email provider
    email = SparkPostEmail(
        from_email=from_email, 
        to_email_list=to_email_list, 
        cc_email_list=cc_email_list, 
        bcc_email_list=bcc_email_list, 
        subject=subject, 
        content=content
        )
    res = email.send_email()
    # Upon failure, try SendGRid
    if res.status_code is not 200 or 201 or 202:
        email = SendGridEmail(
        from_email=from_email, 
        to_email_list=to_email_list, 
        cc_email_list=cc_email_list, 
        bcc_email_list=bcc_email_list, 
        subject=subject, 
        content=content
        )
        res = email.send_email()
        return Response(status=res.status_code)
    else:
        # If original callback succeeded, return 200 response
        return res

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # NEED TO GET API KEYS OUT OF FILE