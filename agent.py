

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

    def act(self, prompt: str = "") -> str:
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

    This agent can take a user prompt and return a predefined answer from a
    dictionary lookup, demonstrating a simple task execution.
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
            "weather": "I can't check the current weather, but I can tell you it's always sunny in my code!",
            "name": f"My name is {self.name}. What's yours?",
            "time": "I don't have access to real-time information, but it's a great time to code!",
            "help": "I can help you with questions about my name, the weather, and general greetings.",
        }

    def act(self, prompt: str) -> str:
        """
        Takes a user prompt and returns a predefined answer.

        Args:
            prompt (str): The user's prompt (e.g., "what's the weather?").

        Returns:
            str: The predefined answer from the knowledge base or a default response.
        """
        # Normalize the prompt for case-insensitive lookup
        clean_prompt = prompt.lower().strip()

        # Look up the prompt in the knowledge base
        response = self.knowledge_base.get(
            clean_prompt,
            "I'm sorry, I don't understand that request. Try asking for 'help'."
        )

        print(f"Assistant Agent {self.name} received prompt: '{prompt}'")
        print(f"Assistant Agent {self.name} responding: '{response}'")

        return response


# --- Demonstration of Agents in Action ---
if __name__ == "__main__":
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
    agent_b.act("Begin report preparation.")

    print("\n" + "="*40 + "\n")

    print("--- Demonstrating Simple Task Execution with AssistantAgent ---")

    # Create an Assistant Agent instance
    assistant = AssistantAgent("Cody")

    # Simulate user prompts and get responses
    user_prompt_1 = "Hello"
    assistant.act(user_prompt_1)

    print("-" * 20)

    user_prompt_2 = "What's the weather like?"
    assistant.act(user_prompt_2)

    print("-" * 20)

    user_prompt_3 = "who are you?"
    assistant.act(user_prompt_3)

    print("-" * 20)

    # A prompt that is not in the knowledge base
    user_prompt_4 = "what's the capital of France?"
    assistant.act(user_prompt_4)

    print("\nDemonstration complete.")

