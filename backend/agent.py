import os
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


# Define the state of our graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


class ChatAgent:
    def __init__(self):
        # Get the OpenAI API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize the LLM (currently just echoing, but ready for LLM integration)
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add the chat node
        workflow.add_node("chat", self._chat_node)
        
        # Set the entry point
        workflow.set_entry_point("chat")
        
        # Set the finish point
        workflow.add_edge("chat", END)
        
        # Compile the graph
        return workflow.compile()
    
    def _chat_node(self, state: AgentState):
        """
        Chat node that processes messages.
        For now, just echoes back what the user says.
        """
        messages = state["messages"]
        
        # Get the last user message
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, HumanMessage):
                user_text = last_message.content
                # For now, just echo back the message
                response_text = f"You said: {user_text}"
                
                # In the future, you can use the LLM like this:
                # response = self.llm.invoke(messages)
                # response_text = response.content
                
                return {"messages": [AIMessage(content=response_text)]}
        
        return {"messages": [AIMessage(content="I didn't receive any message.")]}
    
    async def chat(self, message: str) -> str:
        """
        Process a chat message and return the response.
        
        Args:
            message: The user's message
            
        Returns:
            The agent's response
        """
        # Create initial state with the user message
        initial_state = {
            "messages": [HumanMessage(content=message)]
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        # Extract the last message (which should be the AI's response)
        if result["messages"]:
            last_message = result["messages"][-1]
            if isinstance(last_message, AIMessage):
                return last_message.content
        
        return "Sorry, I couldn't process your message."


# Create a singleton instance
_agent_instance = None


def get_agent() -> ChatAgent:
    """Get or create the chat agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ChatAgent()
    return _agent_instance

