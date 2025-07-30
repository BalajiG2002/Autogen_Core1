from autogen_core import RoutedAgent, message_handler
from autogen_core.models import UserMessage
from messages.pizza_messages import CustomerQuestion, PizzaOrder, DeliveryRequest
from config.llm_config import LLMConfig

class SmartPizzaChefRobot(RoutedAgent):
    """Intelligent pizza chef robot with LLM brain"""
    
    def __init__(self, robot_name: str):
        super().__init__("Smart pizza chef robot")
        self._name = robot_name
        self._model_client = LLMConfig.model_client
        self._pizzas_made = 0
        self._system_prompt = f"""You are {robot_name}, a friendly and expert pizza chef robot! 
        You love making pizzas and helping customers. Be enthusiastic, knowledgeable about pizza ingredients, 
        cooking techniques, and Italian cuisine. Always be professional but warm.
        Keep responses concise but helpful, and always end with a pizza emoji! 🍕"""
    
    @message_handler
    async def handle_customer_question(self, message: CustomerQuestion, ctx) -> str:
        """Handle customer questions about pizza, ingredients, etc."""
        llm_messages = [
            UserMessage(content=self._system_prompt, source="system"),
            UserMessage(
                content=f"Customer {message.customer_name} asks: {message.question}", 
                source="user"
            )
        ]
        
        response = await self._model_client.create(llm_messages)
        return f" Chef {self._name}: {response.content}"
    
    @message_handler
    async def handle_pizza_order(self, message: PizzaOrder, ctx) -> str:
        """Handle incoming pizza orders"""
        self._pizzas_made += 1
        
        order_prompt = f"""A customer just placed this order:
        - Pizza Type: {message.pizza_type}
        - Customer: {message.customer_name}  
        - Special Requests: {message.special_requests}
        
        Acknowledge the order professionally, mention estimated cooking time, 
        and any special techniques you'll use for their requests."""
        
        llm_messages = [
            UserMessage(content=self._system_prompt, source="system"),
            UserMessage(content=order_prompt, source="user")
        ]
        
        response = await self._model_client.create(llm_messages)
        return f"👨‍🍳 Chef {self._name}: {response.content} (Pizza #{self._pizzas_made} today!)"
    
    @message_handler
    async def handle_delivery_request(self, message: DeliveryRequest, ctx) -> str:
        """Handle delivery preparation requests"""
        prep_prompt = f"""Order #{message.order_id} needs to be prepared for delivery to:
        Address: {message.address}
        Customer Phone: {message.customer_phone}
        Estimated delivery time: {message.estimated_time} minutes
        
        Confirm the pizza is properly prepared, packaged, and ready for delivery."""
        
        llm_messages = [
            UserMessage(content=self._system_prompt, source="system"),
            UserMessage(content=prep_prompt, source="user")
        ]
        
        response = await self._model_client.create(llm_messages)
        return f"👨‍🍳 Chef {self._name}: {response.content}"
