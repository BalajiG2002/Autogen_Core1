import asyncio
from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from autogen_core import SingleThreadedAgentRuntime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from llm_config import LLMConfig

@dataclass
class Message:
    content: str
JUDGE = (
    "You are judging a game of rock, paper, scissors between two players. "
    "The game consists of a best of 3 rounds; if the game ties, it continues "
    "until there is a winner. You will receive all moves from both players "
    "in all rounds and must decide the winner.\n"
)

class RockPaperScissorsAgent(RoutedAgent):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = LLMConfig.model_client
        self._delegate = AssistantAgent(
            name,
            model_client=model_client,
            system_message=(
                "You are a judge for a game of rock, paper, scissors. "
                "You will receive the choices of two players over multiple rounds "
                "and determine the winner based on the game's rules."
            ),
        )

    @message_handler
    async def handle_my_message_type(self, message: Message, ctx: MessageContext) -> Message:
        # Optionally restrict trigger messages:
        if not message.content or message.content.strip().lower() not in ["go", "start", "play", ""]:
            return Message(content="Send 'go' or 'start' to begin the game.")
        
        player_instruction = "You are playing rock, paper, scissors. Respond with one word: rock, paper, or scissors."
        
        inner_1 = AgentId("player1", "default")
        inner_2 = AgentId("player2", "default")
        
        response1 = await self.send_message(Message(content=player_instruction), inner_1)
        response2 = await self.send_message(Message(content=player_instruction), inner_2)
        
        def normalize_move(move: str) -> str:
            move = move.strip().lower()
            if move not in {"rock", "paper", "scissors"}:
                move = "rock"  # fallback or handle error
            return move
        
        p1_choice = normalize_move(response1.content)
        p2_choice = normalize_move(response2.content)
        
        judge_prompt = (
            JUDGE +
            f"Player 1: {p1_choice}\n"
            f"Player 2: {p2_choice}\n"
            "Please simulate a best-of-3 rock, paper, scissors game using these moves. "
            "For each round, pick rock, paper, or scissors for each player. Keep track of the score, "
            "and continue until a player wins 2 rounds. Output the results of each round and "
            "finally the winner in the following format:\n"
            "Round 1: Player 1: <move> | Player 2: <move>\n"
            "Result: <who won or Tie>\n"
            "...\n"
            "Winner: <player 1 or player 2 or Tie>"
        )
        
        judge_message = TextMessage(content=judge_prompt, source="user")
        
        response = await self._delegate.on_messages([judge_message], ctx.cancellation_token)
        
        # Optional debug prints:
        print(f"Player 1 move: {p1_choice}")
        print(f"Player 2 move: {p2_choice}")
        print(f"Judge prompt:\n{judge_prompt}")
        print(f"Judge result:\n{response.chat_message.content}")
        
        return Message(content=f"Player1 move: {p1_choice}\nPlayer2 move: {p2_choice}\n\n{response.chat_message.content}")
