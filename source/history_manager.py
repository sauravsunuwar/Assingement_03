class HistoryManager:
    def __init__(self, max_states=30):
        self.max_states = max_states
        self.undo_stack = []
        self.redo_stack = []

    def reset(self):
        self.undo_stack.clear()
        self.redo_stack.clear()

    def push(self, image_bgr):
        self.undo_stack.append(image_bgr.copy())
        if len(self.undo_stack) > self.max_states:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if len(self.undo_stack) <= 1:
            return None
        current = self.undo_stack.pop()
        self.redo_stack.append(current)
        return self.undo_stack[-1].copy()

    def redo(self):
        if not self.redo_stack:
            return None
        img = self.redo_stack.pop()
        self.undo_stack.append(img.copy())
        return img.copy()
