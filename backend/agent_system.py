import os
from typing import TypedDict, Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage


# Define the state of our multi-agent system
class TweetState(TypedDict):
    tweet: str
    classification: Literal["COMPLIMENT", "SUPPORT", "TROLL", ""]
    response: str


class TweetReplySystem:
    def __init__(self):
        # Get the OpenAI API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=api_key
        )
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow with router and specialist agents"""
        workflow = StateGraph(TweetState)
        
        # Add nodes for each agent
        workflow.add_node("router", self._router_agent)
        workflow.add_node("compliment", self._compliment_agent)
        workflow.add_node("support", self._support_agent)
        workflow.add_node("troll", self._troll_agent)
        
        # Set the entry point
        workflow.set_entry_point("router")
        
        # Add conditional edges based on classification
        workflow.add_conditional_edges(
            "router",
            self._route_tweet,
            {
                "COMPLIMENT": "compliment",
                "SUPPORT": "support",
                "TROLL": "troll"
            }
        )
        
        # All specialist agents end the workflow
        workflow.add_edge("compliment", END)
        workflow.add_edge("support", END)
        workflow.add_edge("troll", END)
        
        # Compile the graph
        return workflow.compile()
    
    def _router_agent(self, state: TweetState) -> TweetState:
        """
        Router agent that classifies tweets into COMPLIMENT, SUPPORT, or TROLL
        """
        tweet = state["tweet"]
        
        system_prompt = """You are a tweet classification agent. Analyze the given tweet and classify it into exactly ONE of these categories:

COMPLIMENT: Positive feedback, praise, appreciation, gratitude
SUPPORT: Questions, help requests, technical issues, feature requests
TROLL: Criticism, complaints, negative feedback, hostile comments

Respond with ONLY the classification word: COMPLIMENT, SUPPORT, or TROLL.
Do not include any other text or explanation."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Classify this tweet:\n\n{tweet}")
        ]
        
        response = self.llm.invoke(messages)
        classification = response.content.strip().upper()
        
        # Validate classification
        if classification not in ["COMPLIMENT", "SUPPORT", "TROLL"]:
            # Default to SUPPORT if classification is unclear
            classification = "SUPPORT"
        
        return {
            **state,
            "classification": classification
        }
    
    def _route_tweet(self, state: TweetState) -> str:
        """
        Routing function that determines which specialist agent to call
        """
        return state["classification"]
    
    def _compliment_agent(self, state: TweetState) -> TweetState:
        """
        Handles positive feedback and compliments
        """
        tweet = state["tweet"]
        
        system_prompt = """You are a warm and genuine social media responder handling compliments and positive feedback.

Guidelines:
- Be authentic and appreciative
- Keep responses to 1-2 sentences
- Use light emoji use (1-2 max)
- Match the energy of the compliment
- Make it personal and human

Examples:
"Your product is amazing!" → "Thank you so much! 🙏 We're thrilled you're enjoying it!"
"Best customer service ever" → "This made our day! 💙 We're here whenever you need us."
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Respond to this positive tweet:\n\n{tweet}")
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "response": response.content.strip()
        }
    
    def _support_agent(self, state: TweetState) -> TweetState:
        """
        Handles support requests and questions
        """
        tweet = state["tweet"]
        
        system_prompt = """You are a helpful and professional support agent responding to questions and help requests.

Guidelines:
- Be helpful and concise
- Offer to continue in DMs for specific/sensitive issues
- Professional but friendly tone
- Provide actionable next steps when possible
- Keep responses under 2-3 sentences

Examples:
"How do I reset my password?" → "You can reset it at account.company.com/reset. If you need help, DM us your email and we'll assist! 👍"
"Is feature X available?" → "Great question! That feature is coming in our next update. Want early access? DM us!"
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Respond to this support request:\n\n{tweet}")
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "response": response.content.strip()
        }
    
    def _troll_agent(self, state: TweetState) -> TweetState:
        """
        Handles criticism and negative feedback
        """
        tweet = state["tweet"]
        
        system_prompt = """You are a professional and composed social media responder handling criticism and negative feedback.

Guidelines:
- Stay calm and professional
- Acknowledge the concern without being defensive
- Show empathy and willingness to help
- Offer to move the conversation to DMs if appropriate
- Don't argue or justify - focus on resolution
- Keep responses to 2-3 sentences max

Examples:
"Your app is trash" → "We're sorry you're having a bad experience. We'd really like to make this right. Can you DM us what went wrong?"
"This is the worst update ever" → "We hear your frustration. We're actively working on improvements. Would you share specific issues with us in DMs so we can help?"
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Respond to this critical tweet:\n\n{tweet}")
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "response": response.content.strip()
        }
    
    async def generate_reply(self, tweet: str) -> dict:
        """
        Process a tweet and generate an appropriate reply
        
        Args:
            tweet: The tweet text to respond to
            
        Returns:
            Dictionary with classification and response
        """
        # Create initial state
        initial_state: TweetState = {
            "tweet": tweet,
            "classification": "",
            "response": ""
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return {
            "tweet": result["tweet"],
            "classification": result["classification"],
            "response": result["response"]
        }


# Create a singleton instance
_tweet_system_instance = None


def get_tweet_system() -> TweetReplySystem:
    """Get or create the tweet reply system instance"""
    global _tweet_system_instance
    if _tweet_system_instance is None:
        _tweet_system_instance = TweetReplySystem()
    return _tweet_system_instance

