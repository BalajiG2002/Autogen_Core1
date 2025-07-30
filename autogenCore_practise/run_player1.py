import asyncio
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from agents.player1Agent import Player1Agent
async def main():
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    await Player1Agent.register(worker, "player1", lambda: Player1Agent("player1"))
    print("player1Agent started")
    try:
        while True:
            await asyncio.sleep(3600)
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("Shutdown requested; stopping workers")
        await worker.stop()

if __name__ == "__main__":
    asyncio.run(main())
