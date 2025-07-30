from autogen_core import SingleThreadedAgentRuntime, AgentId
from agents.pizza_chef import SmartPizzaChefRobot
from agents.customer_service import SmartCustomerServiceRobot
from agents.creative_namer import CreativePizzaNamerRobot
from typing import Dict

class PizzaShopRuntime:
    """Manages the pizza shop runtime and agent lifecycle"""
    
    def __init__(self):
        self.runtime = SingleThreadedAgentRuntime()
        self.is_running = False
        self.agent_ids: Dict[str, AgentId] = {}
    
    async def setup_agents(self):
        """Register all agent types with the runtime"""
        # Register pizza chef
        await SmartPizzaChefRobot.register(
            self.runtime, 
            "smart_chef", 
            lambda: SmartPizzaChefRobot("Chef Mario AI")
        )
        
        # Register customer service
        await SmartCustomerServiceRobot.register(
            self.runtime,
            "smart_service", 
            lambda: SmartCustomerServiceRobot("Sarah AI")
        )
        
        # Register creative namer
        await CreativePizzaNamerRobot.register(
            self.runtime,
            "creative_namer",
            lambda: CreativePizzaNamerRobot("Pablo the Namer")
        )
        
        # Create agent addresses
        self.agent_ids = {
            "chef": AgentId("smart_chef", "kitchen_ai"),
            "service": AgentId("smart_service", "front_desk"),
            "namer": AgentId("creative_namer", "creativity_corner")
        }
    
    async def start(self):
        """Start the pizza shop runtime"""
        if not self.is_running:
            await self.setup_agents()
            self.runtime.start()
            self.is_running = True
            print(" Pizza shop is now open for business!")
    
    async def stop(self):
        """Stop the pizza shop runtime"""
        if self.is_running:
            await self.runtime.stop()
            self.is_running = False
            print(" Pizza shop is closed. Good night!")
    
    def get_agent_id(self, agent_type: str) -> AgentId:
        """Get agent ID by type"""
        return self.agent_ids.get(agent_type)
    
    async def send_message(self, message, agent_type: str):
        """Helper method to send messages to agents"""
        if not self.is_running:
            raise RuntimeError("Pizza shop is not running! Call start() first.")
        
        agent_id = self.get_agent_id(agent_type)
        if not agent_id:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return await self.runtime.send_message(message, agent_id)
