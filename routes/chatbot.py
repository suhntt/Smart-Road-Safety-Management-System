from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    if not data:
        return jsonify({"response": "I didn't receive any message."})
        
    message = data.get('message', '').lower()

    # Highly forgiving keyword matching
    if any(word in message for word in ['ambulance', 'emergency', 'hospital', 'doctor', 'medical', 'hurt', 'injury']):
        response = "🚨 For emergencies, please dial **108** for Ambulance or **104** for Medical Helpline immediately. The nearest major hospital is Assam Medical College (AMC), Dibrugarh."
    elif any(word in message for word in ['police', 'station', 'cop', 'traffic', '100', '112', 'crime']):
        response = "👮 For Police assistance, please dial **100** or **112**. Dibrugarh Traffic Police control room is active 24/7."
    elif any(word in message for word in ['accident', 'crash', 'collision', 'hit', 'report']):
        response = "⚠️ If you witnessed an accident, please ensure your safety first. Call 108 for medical help, then 100 for police. You can also report the exact location via our Public Feedback form on the homepage."
    elif any(word in message for word in ['helmet', 'seatbelt', 'rule', 'fine', 'challan', 'speed', 'drink', 'drunk']):
        response = "📜 Road Safety Rules: Wearing a helmet (both rider & pillion) and seatbelts are mandatory in Dibrugarh. Drink & Drive fines are severe. Minimum helmet fine starts at ₹1,000."
    elif any(word in message for word in ['weather', 'rain', 'fog', 'climate', 'sun']):
        response = "🌧️ Weather conditions heavily impact road safety. Please drive slowly and keep headlights on during rain or fog!"
    elif any(word in message for word in ['who are you', 'what are you', 'creator', 'made you', 'b.tech', 'project']):
        response = "🤖 I am an AI assistant designed by B.Tech students to help citizens of Dibrugarh with road safety information, emergency contacts, and traffic rules."
    elif any(word in message for word in ['thank', 'thx', 'ok', 'good', 'great', 'awesome']):
        response = "You're very welcome! Stay safe on the roads!"
    elif any(word in message for word in ['hello', 'hi', 'hey', 'greetings', 'namaste', 'morning', 'evening']):
        response = "Hello! I am the Dibrugarh Road Safety AI. How can I assist you today? You can ask me about emergency numbers or traffic rules."
    else:
        response = "I'm sorry, I didn't quite catch that. You can try asking me: 'What is the ambulance number?', 'What are the helmet rules?', or 'How to report an accident?'"

    return jsonify({"response": response})
