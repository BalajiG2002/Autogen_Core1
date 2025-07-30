from autogen_core import RoutedAgent, message_handler
from autogen_core.models import UserMessage
from messages.pizza_messages import PizzaOrder
from config.llm_config import LLMConfig

class CreativePizzaNamerRobot(RoutedAgent):
    """Creative robot that names custom pizzas"""
    
    def __init__(self, robot_name: str = "Creative Namer Bot"):
        super().__init__("Creative pizza namer robot")
        self._name = robot_name
        # Use creative model with higher temperature
        self._model_client = LLMConfig.model_client
        self._pizzas_named = 0
        self._system_prompt = f"""You are {robot_name}, a creative pizza naming expert! 
        When given a pizza order, create a fun, catchy, memorable name for that specific combination.
        Be creative, use puns when appropriate, make it sound appetizing and unique!
        Keep names under 5 words. Examples: "Margherita Magic", "Pepperoni Paradise", "Veggie Victory"."""
    
    @message_handler
    async def handle_pizza_order(self, message: PizzaOrder, ctx) -> str:
        """Create creative names for pizza orders"""
        self._pizzas_named += 1
        
        naming_prompt = f"""Create a creative name for this pizza:
        - Type: {message.pizza_type}
        - Special requests: {message.special_requests}
        - Customer: {message.customer_name}
        
        Make it catchy, fun, and memorable! Consider the ingredients and special requests."""
        
        llm_messages = [
            UserMessage(content=self._system_prompt, source="system"),
            UserMessage(content=naming_prompt, source="user")
        ]
        
        response = await self._model_client.create(llm_messages)
        return f" {self._name}: I'll call this masterpiece '{response.content}' - Perfect for {message.customer_name}! (Pizza name #{self._pizzas_named})"
