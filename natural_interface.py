#!/usr/bin/env python3
"""
ALLA v17.0 - Natural Language Interface
======================================

Natural conversation interface for ALLA without hardcoded translations.
ALLA learns language naturally through its existing learning mechanisms.
"""

from alla_engine import AllaEngine
import re

class NaturalALLA:
    def __init__(self):
        print("🧠 Initializing ALLA v17.0...")
        self.engine = AllaEngine()
        print("✅ ALLA is ready for natural conversation!")
        
    def start_conversation(self):
        """Start a natural conversation with ALLA."""
        print("\n" + "="*60)
        print("ALLA v17.0 - NATURAL CONVERSATION")
        print("="*60)
        print("Hello! I am ALLA. You can talk to me in natural language.")
        print("I will ask questions about words I don't understand.")
        print("You can teach me using: teach [type] \"word\" as \"expression\"")
        print("\nExamples you can try:")
        print("• 'take the mysterious_gadget' - I'll ask what it is")
        print("• 'what do you know about red' - I'll share my knowledge")
        print("• 'create big blue box as test_box' - I'll create an object")
        print("• 'do I have red box' - I'll check my inventory")
        print("\nType 'exit' to end our conversation.")
        print("-" * 60)
        
        while True:
            try:
                # Get user input
                user_input = input("\n🧑 You: ").strip()
                
                if not user_input:
                    continue
                    
                # Exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("ALLA: Goodbye! It was nice talking with you.")
                    break
                
                # Process input directly through ALLA's command processor
                response = self.process_natural_input(user_input)
                print(f"ALLA: {response}")
                
                # Let ALLA think if it has active goals
                if self.engine.active_goals:
                    print("💭 [ALLA is thinking...]")
                    self.engine.tick()
                
            except KeyboardInterrupt:
                print("\nALLA: Conversation interrupted.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("ALLA: Sorry, I had trouble processing that. Could you try again?")
        
        self.engine.shutdown()
    
    def process_natural_input(self, user_input: str) -> str:
        """Process natural language input using ALLA's existing systems."""
        # Process the command directly through ALLA's command processor
        feedback, result = self.engine.process_command(user_input)
        
        # Format the response naturally
        natural_response = self.format_response(feedback, result, user_input)
        
        return natural_response
    
    def format_response(self, feedback: str, result, original_input: str) -> str:
        """Format ALLA's response in a more natural way."""
        
        # If ALLA is asking a question (from curiosity system)
        if "[ALLA ASKS]" in feedback:
            return feedback.replace("[ALLA ASKS]", "I want to know:")
        
        # If ALLA is creating an inquiry goal
        if "inquiry goal created" in feedback.lower() or "understanding goal" in feedback.lower():
            return "I don't understand that word yet. Let me ask you about it..."
        
        # If ALLA doesn't understand and will learn
        if "I don't understand the word" in feedback and "I must learn" in feedback:
            unknown_word = feedback.split("'")[1] if "'" in feedback else "that"
            return f"Hmm, I don't know what '{unknown_word}' means. Could you help me understand?"
        
        # If result is a list of objects
        if isinstance(result, list):
            if len(result) == 0:
                return "I didn't find anything matching that description."
            elif len(result) == 1:
                obj = result[0]
                return f"I found: {obj.name} (color: {obj.color}, shape: {obj.shape})"
            else:
                items = [f"{obj.name}" for obj in result[:3]]
                more = "..." if len(result) > 3 else ""
                return f"I found {len(result)} objects: {', '.join(items)}{more}"
        
        # If result is boolean (yes/no questions)
        if isinstance(result, bool):
            if "checking if I have" in feedback.lower():
                return "Yes, I have it!" if result else "No, I don't have that."
            elif "checking if" in feedback.lower() or "verifying" in feedback.lower():
                return "Yes, that's correct!" if result else "No, that's not right."
            else:
                return "Yes" if result else "No"
        
        # If result contains knowledge information
        if isinstance(result, str):
            if "don't have abstract knowledge" in str(result):
                return "I don't know about that yet. Could you teach me?"
            elif "Known" in str(result) or "know about" in feedback.lower():
                return f"What I know: {result}"
            elif "Successfully" in str(result):
                return f"Done! {result}"
        
        # Handle parse errors gracefully
        if result is None and ("not understood" in feedback.lower() or "invalid" in feedback.lower()):
            return "I'm not sure what you mean. Could you try explaining it differently, or teach me new words if needed?"
        
        # Default: clean up ALLA's technical feedback
        clean_feedback = feedback
        clean_feedback = clean_feedback.replace("ALLA:", "").replace("[ALLA]", "").strip()
        clean_feedback = clean_feedback.replace("Checking if", "Let me check if")
        clean_feedback = clean_feedback.replace("Searching for", "Looking for")
        clean_feedback = clean_feedback.replace("Attempting to", "Trying to")
        clean_feedback = clean_feedback.replace("Planning to", "I plan to")
        
        return clean_feedback

def main():
    """Main function to run the natural interface."""
    try:
        natural_alla = NaturalALLA()
        natural_alla.start_conversation()
    except Exception as e:
        print(f"Failed to start ALLA: {e}")
        print("Please make sure alla_engine.py and world.py are available.")

if __name__ == "__main__":
    main()
