import asyncio
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from agents.RockPaperScissorsAgent import RockPaperScissorsAgent ,Message
from autogen_core import AgentId

async def main():
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    await RockPaperScissorsAgent.register(worker, "rock_paper_scissors", lambda: RockPaperScissorsAgent("rock_paper_scissors"))
    print("rock_paper_scissorsAgent started")

    # Optionally send a "go" message to start the game:
    start_message = Message(content="go")
    agent_id = AgentId("rock_paper_scissors", "default")
    response = await worker.send_message(start_message, agent_id)
    print("Game result:\n", response.content)
    try:
        while True:
            await asyncio.sleep(3600)
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("Shutdown requested; stopping workers")
        await worker.stop()

if __name__ == "__main__":
    asyncio.run(main())
