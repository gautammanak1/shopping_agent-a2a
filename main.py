import os
from threading import Thread
from typing import Dict, List
from adpter import SingleA2AAdapter, A2AAgentConfig, a2a_servers
from shopping_agent import ShoppingAgentExecutor
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info("🔧 Setting up Shopping Partner Agent")
        self.agent_configs = [
            A2AAgentConfig(
                name="shopping_partner_specialist",
                description="AI Agent for product recommendations and shopping assistance.",
                url="http://localhost:10020",
                port=10020,
                specialties=[
                    "product recommendations", "shopping", "e-commerce",
                    "fashion", "electronics", "home goods", "sports gear"
                ],
                priority=3
            )
        ]
        self.executors = {
            "shopping_partner_specialist": ShoppingAgentExecutor()
        }
        logger.info("✅ Shopping Partner Agent configuration created")

    def create_coordinator(self):
        """
        Creates the SingleA2AAdapter (uAgent coordinator) for the shopping partner.
        """
        logger.info("🤖 Creating Shopping Partner Coordinator...")
        shopping_executor = self.executors.get("shopping_partner_specialist")
        if shopping_executor is None:
            raise ValueError("ShoppingAgentExecutor not found in executors dictionary.")

        self.coordinator = SingleA2AAdapter(
            agent_executor=shopping_executor,
            name="shopping_partner_coordinator",
            description="Coordinator for routing shopping-related queries to the Shopping Partner Agent.",
            port=8200,
            a2a_port=10020,
            mailbox=True
        )
        logger.info("✅ Shopping Partner Coordinator created!")
        return self.coordinator

    def start_system(self):
        """
        Orchestrates the entire system startup process.
        """
        logger.info("🚀 Starting Shopping Partner System")
        try:
            self.setup_agents()
            coordinator = self.create_coordinator()
            self.running = True
            logger.info(f"🎯 Starting Shopping Partner coordinator on port {coordinator.port}...")
            coordinator.run()
        except KeyboardInterrupt:
            logger.info("👋 Shutting down Shopping Partner system...")
            self.running = False
        except Exception as e:
            logger.error(f"❌ Error during agent system startup: {e}", exc_info=True)
            self.running = False

def run_agent_system_in_thread():
    """
    Encapsulates the agent system startup to be run in a separate thread.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    os.environ["UAGENT_MESSAGE_TIMEOUT"] = os.getenv("UAGENT_MESSAGE_TIMEOUT", "120")

    try:
        system = ShoppingPartnerSystem()
        system.start_system()
    except KeyboardInterrupt:
        logger.info("👋 Shopping Partner system thread shutdown complete!")
    except Exception as e:
        logger.error(f"❌ An error occurred in agent system thread: {e}", exc_info=True)
        system.running = False
    finally:
        loop.close()

if __name__ == "__main__":
    logger.info("🚀 Starting FastAPI server on port 8000...")
    agent_thread = Thread(target=run_agent_system_in_thread, daemon=True)
    agent_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)