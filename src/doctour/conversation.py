"""Conversation management for Doctour.

Handles conversation history, context, and session state
for the medieval medical consultation experience.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """Single turn in a conversation."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationTurn':
        """Create from dictionary."""
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )


class ConversationHistory:
    """Manages conversation history and context."""
    
    def __init__(
        self,
        session_id: Optional[str] = None,
        max_turns: int = 50,
        max_context_length: int = 4000
    ):
        """
        Initialize conversation history.
        
        Args:
            session_id: Unique session identifier
            max_turns: Maximum number of turns to keep
            max_context_length: Maximum context length in tokens (approx)
        """
        self.session_id = session_id or self._generate_session_id()
        self.max_turns = max_turns
        self.max_context_length = max_context_length
        self.turns: List[ConversationTurn] = []
        self.created_at = datetime.now()
        self.metadata: Dict[str, Any] = {}
        
        logger.info(f"Created conversation session: {self.session_id}")
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        from uuid import uuid4
        return f"session_{uuid4().hex[:16]}"
    
    def add_turn(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ConversationTurn:
        """
        Add a turn to the conversation.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            metadata: Additional metadata
            
        Returns:
            The created turn
        """
        turn = ConversationTurn(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        
        self.turns.append(turn)
        
        # Trim if exceeding max turns
        if len(self.turns) > self.max_turns:
            removed = self.turns.pop(0)
            logger.debug(f"Removed oldest turn from session {self.session_id}")
        
        logger.debug(f"Added {role} turn to session {self.session_id}")
        return turn
    
    def get_recent_turns(self, n: int = 10) -> List[ConversationTurn]:
        """
        Get the n most recent turns.
        
        Args:
            n: Number of turns to retrieve
            
        Returns:
            List of recent turns
        """
        return self.turns[-n:] if self.turns else []
    
    def get_context_for_llm(
        self,
        max_tokens: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Get conversation context formatted for LLM.
        
        Args:
            max_tokens: Maximum tokens to include (approximate)
            
        Returns:
            List of message dicts for LLM
        """
        max_tokens = max_tokens or self.max_context_length
        
        # Simple token approximation: ~4 chars per token
        messages = []
        total_chars = 0
        
        # Add turns in reverse order until we hit the limit
        for turn in reversed(self.turns):
            turn_chars = len(turn.content)
            if total_chars + turn_chars > (max_tokens * 4):
                break
            
            messages.insert(0, {
                "role": turn.role,
                "content": turn.content
            })
            total_chars += turn_chars
        
        return messages
    
    def clear(self):
        """Clear conversation history."""
        self.turns = []
        logger.info(f"Cleared conversation session: {self.session_id}")
    
    def save_to_file(self, filepath: Path):
        """
        Save conversation to JSON file.
        
        Args:
            filepath: Path to save file
        """
        data = {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "max_turns": self.max_turns,
            "max_context_length": self.max_context_length,
            "metadata": self.metadata,
            "turns": [turn.to_dict() for turn in self.turns]
        }
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved conversation to {filepath}")
    
    @classmethod
    def load_from_file(cls, filepath: Path) -> 'ConversationHistory':
        """
        Load conversation from JSON file.
        
        Args:
            filepath: Path to load from
            
        Returns:
            Loaded conversation history
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversation = cls(
            session_id=data["session_id"],
            max_turns=data["max_turns"],
            max_context_length=data["max_context_length"]
        )
        
        conversation.created_at = datetime.fromisoformat(data["created_at"])
        conversation.metadata = data.get("metadata", {})
        conversation.turns = [
            ConversationTurn.from_dict(turn_data)
            for turn_data in data["turns"]
        ]
        
        logger.info(f"Loaded conversation from {filepath}")
        return conversation
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the conversation.
        
        Returns:
            Summary dictionary
        """
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "turn_count": len(self.turns),
            "duration_minutes": (
                datetime.now() - self.created_at
            ).total_seconds() / 60,
            "metadata": self.metadata
        }


class ConversationManager:
    """Manages multiple conversation sessions."""
    
    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize conversation manager.
        
        Args:
            storage_dir: Directory for storing conversations
        """
        self.storage_dir = storage_dir or Path("./conversations")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.active_sessions: Dict[str, ConversationHistory] = {}
        
        logger.info(f"ConversationManager initialized with storage: {self.storage_dir}")
    
    def create_session(
        self,
        session_id: Optional[str] = None,
        **kwargs
    ) -> ConversationHistory:
        """
        Create a new conversation session.
        
        Args:
            session_id: Optional session ID
            **kwargs: Additional arguments for ConversationHistory
            
        Returns:
            New conversation history
        """
        conversation = ConversationHistory(session_id=session_id, **kwargs)
        self.active_sessions[conversation.session_id] = conversation
        return conversation
    
    def get_session(self, session_id: str) -> Optional[ConversationHistory]:
        """
        Get an active session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Conversation history or None
        """
        return self.active_sessions.get(session_id)
    
    def save_session(self, session_id: str):
        """
        Save a session to disk.
        
        Args:
            session_id: Session to save
        """
        conversation = self.active_sessions.get(session_id)
        if not conversation:
            logger.warning(f"Session {session_id} not found")
            return
        
        filepath = self.storage_dir / f"{session_id}.json"
        conversation.save_to_file(filepath)
    
    def load_session(self, session_id: str) -> Optional[ConversationHistory]:
        """
        Load a session from disk.
        
        Args:
            session_id: Session to load
            
        Returns:
            Loaded conversation history or None
        """
        filepath = self.storage_dir / f"{session_id}.json"
        if not filepath.exists():
            logger.warning(f"Session file not found: {filepath}")
            return None
        
        conversation = ConversationHistory.load_from_file(filepath)
        self.active_sessions[conversation.session_id] = conversation
        return conversation
    
    def close_session(self, session_id: str, save: bool = True):
        """
        Close and optionally save a session.
        
        Args:
            session_id: Session to close
            save: Whether to save before closing
        """
        if save:
            self.save_session(session_id)
        
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logger.info(f"Closed session: {session_id}")
    
    def list_saved_sessions(self) -> List[str]:
        """
        List all saved session IDs.
        
        Returns:
            List of session IDs
        """
        return [
            f.stem for f in self.storage_dir.glob("*.json")
        ]
