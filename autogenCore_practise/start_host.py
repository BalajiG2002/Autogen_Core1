import asyncio
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost

async def start_host():
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start()
    print("Host started at localhost:50051")
    try:
        while True:
            await asyncio.sleep(3600)  # Non-blocking, so the loop runs
    except KeyboardInterrupt:
        host.stop()

if __name__ == "__main__":
    asyncio.run(start_host())
