"""
HIT137 Assignment 3 - History Manager Class
Manages undo/redo history for image operations
Demonstrates encapsulation and stack-based operations
"""

import numpy as np


class HistoryManager:
    """
    HistoryManager class manages the undo/redo history stack.
    
    Demonstrates OOP Concepts:
    - Encapsulation: Private attributes for history stacks
    - Constructor: __init__ method to initialize empty stacks
    - Methods: push, undo, redo, reset operations
    - Class Interaction: Works with ImageEditorApp to manage state
    
    Uses two stacks:
    - _undo_stack: Stores previous states for undo operation
    - _redo_stack: Stores undone states for redo operation
    """
    
    def __init__(self, max_history=20):
        """
        Constructor: Initialize the HistoryManager with empty stacks.
        
        Args:
            max_history: Maximum number of states to keep in history (default: 20)
        """
        self._undo_stack = []  # Private attribute (encapsulation)
        self._redo_stack = []  # Private attribute (encapsulation)
        self._max_history = max_history  # Limit to prevent memory issues
    
    def push(self, image):
        """
        Push a new image state to the history.
        Clears the redo stack as new action invalidates redo history.
        
        Args:
            image: Image to add to history (numpy array)
        """
        if image is None:
            return
        
        # Add current state to undo stack (make a copy to avoid reference issues)
        self._undo_stack.append(image.copy())
        
        # Limit stack size to prevent memory overflow
        if len(self._undo_stack) > self._max_history:
            self._undo_stack.pop(0)  # Remove oldest entry
        
        # Clear redo stack when new action is performed
        self._redo_stack.clear()
    
    def undo(self):
        """
        Undo the last operation by returning the previous state.
        
        Returns:
            Previous image state or None if no undo available
        """
        # Need at least 2 states to undo (current + previous)
        if len(self._undo_stack) < 2:
            return None
        
        # Pop current state and move to redo stack
        current = self._undo_stack.pop()
        self._redo_stack.append(current)
        
        # Return previous state (but keep it in undo stack)
        return self._undo_stack[-1].copy()
    
    def redo(self):
        """
        Redo the last undone operation.
        
        Returns:
            Next image state or None if no redo available
        """
        if len(self._redo_stack) == 0:
            return None
        
        # Pop from redo stack and move back to undo stack
        next_state = self._redo_stack.pop()
        self._undo_stack.append(next_state)
        
        return next_state.copy()
    
    def reset(self):
        """
        Clear all history (both undo and redo stacks).
        Used when loading a new image.
        """
        self._undo_stack.clear()
        self._redo_stack.clear()
    
    def can_undo(self):
        """
        Check if undo operation is available.
        
        Returns:
            True if undo is possible, False otherwise
        """
        return len(self._undo_stack) >= 2
    
    def can_redo(self):
        """
        Check if redo operation is available.
        
        Returns:
            True if redo is possible, False otherwise
        """
        return len(self._redo_stack) > 0
    
    def get_history_size(self):
        """
        Get the current size of history stacks.
        
        Returns:
            Tuple of (undo_count, redo_count)
        """
        return (len(self._undo_stack), len(self._redo_stack))