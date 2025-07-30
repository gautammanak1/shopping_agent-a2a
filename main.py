import os
from threading import Thread
from typing import Dict, List
from  adpter import SingleA2AAdapter, A2AAgentConfig, a2a_servers
from shopping_agent import ShoppingAgentExecutor
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio # Import asyncio

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

@app.get("/ping")
def ping():
    """
    Health check endpoint for Render.
    """
    return {"status": "agent is running"}

class ShoppingPartnerSystem:
    """
    Manages the setup and execution of the A2A Shopping Partner agent.
    """
    def __init__(self):
        self.coordinator = None
        self.agent_configs: List[A2AAgentConfig] = []
        self.executors: Dict[str, any] = {}
        self.running = False

    def setup_agents(self):
        """
        Configures the A2AAgentConfig and AgentExecutor for the shopping partner.
        """
        print("🔧 Setting up Shopping Partner Agent")
        self.agent_configs = [
            A2AAgentConfig(
                name="shopping_partner_specialist",
                description="AI Agent for product recommendations and shopping assistance.",
                url="http://localhost:10020", # The URL where the A2A server for this agent will run
                port=10020, # The port for the A2A server
                specialties=[
                    "product recommendations", "shopping", "e-commerce",
                    "fashion", "electronics", "home goods", "sports gear"
                ],
                priority=3 # Priority can be useful in multi-agent setups
            )
        ]
        self.executors = {
            "shopping_partner_specialist": ShoppingAgentExecutor()
        }
        print("✅ Shopping Partner Agent configuration created")

    # Removed this function as SingleA2AAdapter handles its own A2A server
    # def start_individual_a2a_servers(self):
    #     """
    #     Starts the individual A2A server for the shopping partner agent.
    #     """
    #     print("🔄 Starting Shopping Partner server...")
    #     a2a_servers(self.agent_configs, self.executors)
    #     print("✅ Shopping Partner server started!")

    def create_coordinator(self):
        """
        Creates the SingleA2AAdapter (uAgent coordinator) for the shopping partner.
        """
        print("🤖 Creating Shopping Partner Coordinator...")
        # Get the executor instance
        shopping_executor = self.executors.get("shopping_partner_specialist")
        if shopping_executor is None:
            raise ValueError("ShoppingAgentExecutor not found in executors dictionary.")

        self.coordinator = SingleA2AAdapter(
            agent_executor=shopping_executor,
            name="shopping_partner_coordinator",
            description="Coordinator for routing shopping-related queries to the Shopping Partner Agent.",
            port=8200, # The port for the uAgent coordinator
            a2a_port=10020, # The port of the A2A server it coordinates
            mailbox=True
        )
        print("✅ Shopping Partner Coordinator created!")
        return self.coordinator

    def start_system(self):
        """
        Orchestrates the entire system startup process.
        """
        print("🚀 Starting Shopping Partner System")
        try:
            self.setup_agents()
            # Removed the call to start_individual_a2a_servers()
            coordinator = self.create_coordinator()
            self.running = True
            print(f"🎯 Starting Shopping Partner coordinator on port {coordinator.port}...")
            coordinator.run() # This is a blocking call
        except KeyboardInterrupt:
            print("👋 Shutting down Shopping Partner system...")
            self.running = False
        except Exception as e:
            print(f"❌ Error during agent system startup: {e}")
            self.running = False

# Function to run the agent system in a separate thread
def run_agent_system_in_thread():
    """
    Encapsulates the agent system startup to be run in a separate thread.
    """
    # Create a new event loop for this thread and set it as the current one
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Set the UAGENT_MESSAGE_TIMEOUT environment variable
    os.environ["UAGENT_MESSAGE_TIMEOUT"] = os.getenv("UAGENT_MESSAGE_TIMEOUT", "120") # Default to 120 seconds

    try:
        system = ShoppingPartnerSystem()
        system.start_system()
    except KeyboardInterrupt:
        print("👋 Shopping Partner system thread shutdown complete!")
    except Exception as e:
        print(f"❌ An error occurred in agent system thread: {e}")
        system.running = False
    finally:
        # Close the event loop when the thread finishes
        loop.close()

if __name__ == "__main__":
    # Start the agent system in a separate daemon thread
    agent_thread = Thread(target=run_agent_system_in_thread, daemon=True)
    agent_thread.start()

    # Start the FastAPI application on the main thread
    print("🚀 Starting FastAPI server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
