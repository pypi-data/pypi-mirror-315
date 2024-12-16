import unittest
from standalone.memory import get_conversation_memory

class TestMemory(unittest.TestCase):
    def test_memory_initialization(self):
        memory = get_conversation_memory()
        self.assertIsNotNone(memory)

if __name__ == "__main__":
    unittest.main()
