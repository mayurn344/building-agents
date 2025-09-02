#
# A Python script to demonstrate a simple Agent class and multi-agent interaction,
# including a knowledge graph agent using the networkx and matplotlib libraries,
# and an assistant agent with a dynamic weather lookup feature.
#
# To run this script, you will need to install networkx, matplotlib, and python-weather:
# pip install networkx matplotlib python-weather
#

import networkx as nx
import matplotlib.pyplot as plt
import asyncio
import python_weather

class Agent:
    """
    Represents a simple agent with a name, a role, and a message inbox.

    An agent can perform an action based on its role and can send and
    receive messages from other agents.
    """
    def __init__(self, name: str, role: str):
        """
        Initializes a new Agent instance.

        Args:
            name (str): The name of the agent.
            role (str): The role or function of the agent.
        """
        self.name = name
        self.role = role
        self.message_inbox = []  # A list to store incoming messages

    async def act(self, prompt: str = "") -> str:
        """
        Performs a simple action and returns a response.
        The action is a basic print statement and a predefined response.

        Args:
            prompt (str): An optional prompt to guide the agent's action.

        Returns:
            str: A simple response string.
        """
        if prompt:
            response = f"Agent {self.name} ({self.role}) is acting on prompt: '{prompt}'."
        else:
            response = f"Agent {self.name} ({self.role}) is performing a generic action."

        print(response)
        return response

    def send_message(self, recipient: 'Agent', message: str):
        """
        Sends a message to another agent.

        Args:
            recipient (Agent): The Agent object to send the message to.
            message (str): The content of the message.
        """
        print(f"Agent {self.name} is sending a message to {recipient.name}: '{message}'")
        recipient.message_inbox.append(message)


class AssistantAgent(Agent):
    """
    An extension of the Agent class specifically designed to act as an assistant.

    This agent can take a user prompt and return a predefined answer or
    dynamically look up information like the weather.
    """
    def __init__(self, name: str, role: str = "assistant"):
        """
        Initializes a new AssistantAgent instance.

        Args:
            name (str): The name of the assistant agent.
            role (str): The role of the agent, defaults to "assistant".
        """
        super().__init__(name, role)
        # A dictionary for simple, predefined responses
        self.knowledge_base = {
            "hello": "Hello! How can I help you today?",
            "name": f"My name is {self.name}. What's yours?",
            "time": "I don't have access to real-time information, but it's a great time to code!",
            "help": "I can help you with questions about my name, the weather, and general greetings.",
        }
        # The weather client is created once for reuse
        self.weather_client = python_weather.Client(unit=python_weather.METRIC)

    async def get_weather_info(self, city: str = "Bangalore") -> str:
        """
        Fetches the current weather for a specified city asynchronously.

        Args:
            city (str): The name of the city to get weather for.

        Returns:
            str: A formatted string with the current temperature and condition.
        """
        try:
            weather = await self.weather_client.get(city)
            temperature = weather.current.temperature
            description = weather.current.description
            return f"The current temperature in {city} is {temperature}°C with {description}."
        except Exception as e:
            return f"Sorry, I couldn't get the weather for {city}. Error: {e}"

    async def act(self, prompt: str) -> str:
        """
        Takes a user prompt and returns a predefined answer or a dynamic response.

        Args:
            prompt (str): The user's prompt (e.g., "what's the weather?").

        Returns:
            str: The predefined or dynamically generated response.
        """
        # Normalize the prompt for case-insensitive lookup
        clean_prompt = prompt.lower().strip()

        # Handle dynamic weather request
        if "weather" in clean_prompt:
            response = await self.get_weather_info("Bangalore")
            print(f"Assistant Agent {self.name} received prompt: '{prompt}'")
            print(f"Assistant Agent {self.name} responding: '{response}'")
            return response
        
        # Handle other predefined responses
        response = self.knowledge_base.get(
            clean_prompt,
            "I'm sorry, I don't understand that request. Try asking for 'help'."
        )

        print(f"Assistant Agent {self.name} received prompt: '{prompt}'")
        print(f"Assistant Agent {self.name} responding: '{response}'")

        return response


class KnowledgeGraphAgent(Agent):
    """
    An agent that queries a NetworkX graph to find relationships.
    """
    def __init__(self, name: str, graph: nx.Graph, role: str = "graph_query_agent"):
        """
        Initializes the KnowledgeGraphAgent.

        Args:
            name (str): The name of the agent.
            graph (nx.Graph): The NetworkX graph to be queried.
            role (str): The role of the agent.
        """
        super().__init__(name, role)
        self.graph = graph

    async def act(self, query: str) -> str:
        """
        Queries the internal graph for connections based on a prompt.

        Args:
            query (str): The query string, expected in the format "Who is connected to X?".

        Returns:
            str: A formatted string showing the connections, or an error message.
        """
        print(f"\nKnowledge Graph Agent {self.name} received query: '{query}'")

        # A simple way to parse the query to find the target node
        parts = query.lower().split("to ")
        if len(parts) < 2:
            return "Query format not understood. Please use 'Who is connected to [Node Name]?''"

        target_node = parts[1].strip("? ")
        
        # Check if the target node exists in the graph
        if target_node not in self.graph:
            return f"The node '{target_node}' does not exist in the graph."

        # Find the neighbors of the target node
        neighbors = list(self.graph.neighbors(target_node))

        if not neighbors:
            response = f"'{target_node}' has no connections in the graph."
        else:
            connections_str = ", ".join(neighbors)
            response = f"The following are connected to '{target_node}': {connections_str}."

        print(f"Knowledge Graph Agent {self.name} responding: '{response}'")
        return response


async def main():
    """
    Main asynchronous function to run all demonstrations.
    """
    print("--- Demonstrating Agent Interaction ---")

    # Create two agent instances
    agent_a = Agent("Alice", "coordinator")
    agent_b = Agent("Bob", "analyst")

    # Have Agent A send a message to Agent B
    agent_a.send_message(agent_b, "Please prepare the weekly report.")

    # Check if Agent B received the message
    print(f"\nAgent {agent_b.name}'s inbox: {agent_b.message_inbox}")

    # Have Agent B perform an action
    print("")
    await agent_b.act("Begin report preparation.")

    print("\n" + "="*40 + "\n")

    print("--- Demonstrating Simple Task Execution with AssistantAgent ---")

    # Create an Assistant Agent instance
    assistant = AssistantAgent("Cody")

    # Simulate user prompts and get responses
    user_prompt_1 = "Hello"
    await assistant.act(user_prompt_1)

    print("-" * 20)

    # The new weather request
    user_prompt_2 = "What's the weather like?"
    await assistant.act(user_prompt_2)

    print("-" * 20)

    user_prompt_3 = "who are you?"
    await assistant.act(user_prompt_3)

    print("-" * 20)

    # A prompt that is not in the knowledge base
    user_prompt_4 = "what's the capital of France?"
    await assistant.act(user_prompt_4)

    print("\n" + "="*40 + "\n")

    print("--- Demonstrating Knowledge Graph Agent and Visualization ---")

    # Create a simple knowledge graph using NetworkX
    G = nx.Graph()
    G.add_edge("Hospital", "Doctor")
    G.add_edge("Doctor", "Patient A")
    G.add_edge("Doctor", "Patient B")
    G.add_edge("Doctor", "Nurse")
    G.add_edge("Hospital", "Clinic")

    # Create a KnowledgeGraphAgent instance
    graph_agent = KnowledgeGraphAgent("GraphBot", graph=G)

    # Query the graph for "Doctor"
    query_1 = "Who is connected to Doctor?"
    await graph_agent.act(query_1)

    # Query the graph for "Hospital"
    query_2 = "Who is connected to Hospital?"
    await graph_agent.act(query_2)
    
    # Query for a non-existent node
    query_3 = "Who is connected to Janitor?"
    await graph_agent.act(query_3)

    # Visualize the graph
    print("\nAttempting to display the graph...")
    plt.figure(figsize=(8, 6)) # Set the figure size for better display
    pos = nx.spring_layout(G, seed=42) # Set a fixed seed for reproducible layout
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', font_size=12, font_weight='bold')
    plt.title("Hospital Knowledge Graph")
    plt.show()

    print("\nDemonstration complete.")

if __name__ == "__main__":
    asyncio.run(main())
