from autogen_core import RoutedAgent, message_handler
from autogen_core.models import UserMessage
from messages.pizza_messages import CustomerQuestion, PizzaOrder, PaymentRequest
from config.llm_config import LLMConfig

class SmartCustomerServiceRobot(RoutedAgent):
    """Intelligent customer service robot"""
    
    def __init__(self, robot_name: str):
        super().__init__("Smart customer service robot")
        self._name = robot_name
        self._model_client = LLMConfig.model_client
        self._customers_helped = 0
        self._total_revenue = 0.0
        self._system_prompt = f"""You are {robot_name}, a super helpful customer service robot for a pizza shop!
        You know everything about pizza orders, ingredients, pricing ($12 for small, $16 for medium, $20 for large), 
        delivery (30-45 minutes), and store policies. Be warm, professional, solve problems quickly, 
        and always maintain a positive, upbeat attitude! Use appropriate emojis to be friendly."""
    
    @message_handler
    async def handle_customer_question(self, message: CustomerQuestion, ctx) -> str:
        """Handle general customer inquiries"""
        self._customers_helped += 1
        
        llm_messages = [
            UserMessage(content=self._system_prompt, source="system"),
            UserMessage(
                content=f"{message.customer_name} asks: {message.question}", 
                source="user"
            )
        ]
        
        response = await self._model_client.create(llm_messages)
        return f"{self._name}: {response.content} (Customer #{self._customers_helped} today!)"
    
    @message_handler
    async def handle_pizza_order(self, message: PizzaOrder, ctx) -> str:
        """Handle order confirmation and pricing"""
        # Simple pricing logic
        price = 16.0  # Default medium pizza price
        if "large" in message.pizza_type.lower():
            price = 20.0
        elif "small" in message.pizza_type.lower():
            price = 12.0
            
        self._total_revenue += price
        
        order_summary = f"""Customer {message.customer_name} ordered:
        - Pizza: {message.pizza_type}
        - Special requests: {message.special_requests}
        - Price: ${price}
        
        Confirm the order, provide the total cost, estimated delivery time, 
        and thank them warmly for their business."""
        
        llm_messages = [
            UserMessage(content=self._system_prompt, source="system"),
            UserMessage(content=order_summary, source="user")
        ]
        
        response = await self._model_client.create(llm_messages)
        return f" {self._name}: {response.content} (Total revenue today: ${self._total_revenue})"
    
    @message_handler
    async def handle_payment_request(self, message: PaymentRequest, ctx) -> str:
        """Handle payment processing"""
        payment_prompt = f"""Process payment for {message.customer_name}:
        - Amount: ${message.amount}
        - Payment method: {message.payment_method}
        
        Confirm payment processed successfully and provide a friendly receipt confirmation."""
        
        llm_messages = [
            UserMessage(content=self._system_prompt, source="system"),
            UserMessage(content=payment_prompt, source="user")
        ]
        
        response = await self._model_client.create(llm_messages)
        return f"{self._name}: {response.content}"
