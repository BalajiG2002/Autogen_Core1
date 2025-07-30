import asyncio
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from agents.player2Agent import Player2Agent  # import your custom agent class

async def main():
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    await Player2Agent.register(worker, "player2", lambda: Player2Agent("player2"))
    print("player2Agent started")
    try:
        while True:
            await asyncio.sleep(3600)
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("Shutdown requested; stopping workers")
        await worker.stop() 

if __name__ == "__main__":
    asyncio.run(main())
