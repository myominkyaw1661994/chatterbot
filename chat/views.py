from django.shortcuts import render
from django.http import HttpResponse
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create your views here.

def index(request):
    return render(request, 'index.html')

def chatmsg(request):

    if request.method == 'POST':

        input = json.loads(request.body.decode('utf-8'))
        input_text = input['name']

        #handle bot message
        response = auto_reply(input_text)
        
        response_data = {}
        response_data['result'] = 'true'
        response_data['message'] = response

        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    
def auto_reply(input_text):
    bot = ChatBot('MedBot')


    bot = ChatBot('MedBot', read_only = True, 
                preprocessors=['chatterbot.preprocessors.convert_to_ascii', 
                                'chatterbot.preprocessors.unescape_html',
                                'chatterbot.preprocessors.clean_whitespace'],
                logic_adapters = [
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': 'Sorry, I am unable to process your request. Please try again, or contact us for help.',
                        'maximum_similarity_threshold': 0.90
                    }
                ],)

    trainer = ListTrainer(bot)

    trainer.train([
        "Hi",
        "Hello",
        "Hey", 
        "How is going...",
        "Hello",
        "Hello, What you like to order?"
    ])

    trainer.train([    
        "Hi, I'd like to order a pizza.",
        "Hello! Sure thing. What size pizza would you like? We have small, medium, and large.",
        "I'll go for a medium-sized pizza, please.",
        "Great choice! What type of crust would you prefer: thin crust, thick crust, or stuffed crust?",
        "I'll go for thin crust",
        "Excellent! Now, let's pick your toppings. What toppings would you like on your pizza?",
        "I want pepperoni, mushrooms, and green peppers.",
        "Perfect! Anything else? We also have options like olives, onions, and sausage.",
        "No, that's it for the toppings",
        "Got it. Would you like any extra cheese or any special instructions for your order?",
        "Yes, extra cheese, please.",
        "Noted! Your order is a medium pizza with thin crust, topped with pepperoni, mushrooms, green peppers, and extra cheese. Is that correct?",
        "Yes, that's correct.",
        "Wonderful! Your total comes to $14.99. May I have your delivery address, please?"
        "Sure, it's 123 Main Street",
        "Thank you! Your pizza will be delivered shortly."
    ])

    trainer.train([
        "I want to cancel my order.",
        "Okay, Your appointment has been cancelled.",
        "I want to cancel my booking.",
        "Okay, Your table has been cancelled.",
    ])


    trainer.train([
        "What is your phone number? How do I reach you? How do I contact you? How do I call you?",
        "Our number is 01**23**45",
        "What is your address? Where are you located?",
        "You can find us at No. 45, 8th Cross, Oakwood Street",
    ])

    trainer.train([
        "Which table is available to book?",
        "We have 3 table with amazing view",
        "One table please",
        "Sure, please select your time slot",
        "Afternoon",
        "Your appointment is confirmed. You can come between 12:00 and 16:00.",
        "Morning",
        "Your appointment is confirmed. You can come between 8:00 and 12:00.",
        "Evening",
        "Your appointment is confirmed. You can come between 16:00 and 20:00.",
    ])

    trainer.train([
        "Thank you!",
        "You're most welcome!",
        "Thanks!",
        "Of course!",
        ])

    value =bot.get_response(input_text)

    return str(value)

    