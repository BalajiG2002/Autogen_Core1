import asyncio
from messages.pizza_messages import CustomerQuestion, PizzaOrder, PaymentRequest
from utils.runtime_helpers import PizzaShopRuntime
from config.llm_config import LLMConfig
from autogen_core.models import UserMessage
async def demo_pizza_shop():
    """Demo the smart pizza shop with all agents"""
    print("🧠 Welcome to the Smart AI Pizza Shop!")
    print("Our robots have advanced AI brains and work together!")
    
    # Initialize pizza shop
    pizza_shop = PizzaShopRuntime()
    
    try:
        await pizza_shop.start()
        
        print("\n" + "="*50)
        print("🎉 All robots are online and ready to serve!")
        print("="*50)
        
        # Demo interactions
        interactions = [
            # Customer questions
            ("What's the difference between your margherita and pepperoni?", "Alice"),
            ("Do you have vegan options?", "Bob"),
            ("How long does delivery take?", "Charlie"),
        ]
        
        print("\n CUSTOMER QUESTIONS:")
        for question, customer in interactions:
            print(f"\n👤 {customer}: {question}")
            
            # Ask both chef and service robots
            chef_response = await pizza_shop.send_message(
                CustomerQuestion(question, customer), "chef"
            )
            service_response = await pizza_shop.send_message(
                CustomerQuestion(question, customer), "service"  
            )
            
            print(chef_response)
            print(service_response)
        
        # Demo pizza orders
        print(f"\n PIZZA ORDERS:")
        orders = [
            ("Hawaiian Large", "David", "extra pineapple, thin crust, light cheese"),
            ("Veggie Supreme Medium", "Emma", "no mushrooms, extra peppers, gluten-free crust"),
            ("Meat Lovers Small", "Frank", "extra spicy, thick crust")
        ]

        for pizza_type, customer, special_requests in orders:
            print(f"\n Order from {customer}: {pizza_type}")
            print(f"   Special requests: {special_requests}")

            order = PizzaOrder(pizza_type, customer, special_requests)
            
            # Get responses from all relevant robots
            chef_response = await pizza_shop.send_message(order, "chef")
            service_response = await pizza_shop.send_message(order, "service")
            name_response = await pizza_shop.send_message(order, "namer")
            
            print(chef_response)
            print(service_response)
            print(name_response)
            print("-" * 40)
        
        # Demo payment processing
        print(f"\n PAYMENT PROCESSING:")
        payment = PaymentRequest(20.0, "credit card", "David")
        payment_response = await pizza_shop.send_message(payment, "service")
        print(payment_response)
        
    except Exception as e:
        print(f" Error: {e}")
    finally:
        await pizza_shop.stop()

async def smart_interactive_mode():
    """Smart mode that uses LLM to classify user intent"""
    pizza_shop = PizzaShopRuntime()
    
    intent_classifier = LLMConfig.model_client
    
    try:
        await pizza_shop.start()
        
        while True:
            customer_name = input("\nYour name: ")
            if customer_name.lower() == 'quit':
                break
                
            user_input = input("What can we help you with? ")
            if user_input.lower() == 'quit':
                break
            
            # Use LLM to classify intent
            classification_prompt = f"""
            Classify this customer message as either "question" or "order":
            Message: "{user_input}"
            
            Return only one word: "question" or "order"
            """
            
            llm_messages = [
                UserMessage(content=classification_prompt, source="user")
            ]
            
            intent_response = await intent_classifier.create(llm_messages)
            intent = intent_response.content.strip().lower()
            
            if "order" in intent:
                # Handle as order - extract details with LLM
                extraction_prompt = f"""
                Extract pizza order details from: "{user_input}"
                
                Return in format:
                Pizza Type: [type]
                Special Requests: [requests]
                """
                
                extract_messages = [
                    UserMessage(content=extraction_prompt, source="user")
                ]
                
                extract_response = await intent_classifier.create(extract_messages)
                # Simple parsing (you could make this more robust)
                lines = extract_response.content.split('\n')
                pizza_type = "Custom Pizza"
                special_requests = user_input
                
                for line in lines:
                    if "Pizza Type:" in line:
                        pizza_type = line.split(":", 1)[1].strip()
                    elif "Special Requests:" in line:
                        special_requests = line.split(":", 1)[1].strip()
                
                # Create and send order
                order = PizzaOrder(pizza_type, customer_name, special_requests)
                responses = []
                
                for agent_type in ["chef", "service", "namer"]:
                    response = await pizza_shop.send_message(order, agent_type)
                    responses.append(response)
                    print(f"\n{response}")
            
            else:
                # Handle as question
                question = CustomerQuestion(user_input, customer_name)
                
                for agent_type in ["chef", "service"]:
                    response = await pizza_shop.send_message(question, agent_type)
                    print(f"\n{response}")
            
    finally:
        await pizza_shop.stop()

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Demo mode")
    print("2. Interactive mode")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "2":
        asyncio.run(smart_interactive_mode())
    else:
        asyncio.run(demo_pizza_shop())
