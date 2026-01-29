#!/usr/bin/env python3
"""Script to run the Doctour medieval medical AI.

This script initializes and runs the Doctour system,
providing a simple command-line interface for consultations.
"""

import sys
import logging
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from doctour.config import Config
from doctour.safety import SafetyValidator
from doctour.rag import RAGSystem
from doctour.model import DoctourModel
from doctour.conversation import ConversationManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print welcome banner."""
    print("="*60)
    print("  DOCTOUR - Medieval Medical AI Consultation")
    print("  Based on pre-1410 historical texts")
    print("="*60)
    print()
    print("IMPORTANT: This is for educational purposes only.")
    print("Always consult qualified healthcare professionals.")
    print()
    print("Type 'quit' or 'exit' to end the consultation.")
    print("="*60)
    print()


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Run Doctour medieval medical AI"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model name to use"
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize components
    logger.info("Initializing Doctour...")
    
    config = Config(
        model_name=args.model if args.model else None
    )
    
    safety_validator = SafetyValidator(config)
    rag_system = RAGSystem(config)
    model = DoctourModel(config, safety_validator, rag_system)
    conversation_manager = ConversationManager()
    
    # Load model
    logger.info("Loading model...")
    if not model.load_model():
        logger.error("Failed to load model")
        return 1
    
    # Create conversation session
    session = conversation_manager.create_session()
    logger.info(f"Created session: {session.session_id}")
    
    # Print welcome banner
    print_banner()
    
    # Main interaction loop
    try:
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\nFarewell! May your health be good.")
                    break
                
                # Add user turn to conversation
                session.add_turn('user', user_input)
                
                # Generate response
                response_data = model.generate_response(
                    user_input,
                    conversation_history=session.get_context_for_llm()
                )
                
                # Add assistant turn to conversation
                session.add_turn(
                    'assistant',
                    response_data['response'],
                    metadata=response_data.get('metadata', {})
                )
                
                # Display response
                print(f"\nDoctour: {response_data['response']}")
                
                # Show sources if available
                if response_data.get('sources'):
                    print(f"\n[{len(response_data['sources'])} historical sources consulted]")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Ending consultation...")
                break
            except Exception as e:
                logger.error(f"Error in conversation loop: {e}")
                print("\nAn error occurred. Please try again.\n")
        
    finally:
        # Save conversation
        logger.info("Saving conversation...")
        conversation_manager.save_session(session.session_id)
        
        # Cleanup
        model.unload_model()
        logger.info("Doctour shutdown complete")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
