from unittest import TestCase

import tree_sitter, tree_sitter_git_msg


class TestLanguage(TestCase):
    def test_can_load_grammar(self):
        try:
            tree_sitter.Language(tree_sitter_git_msg.language())
        except Exception:
            self.fail("Error loading GitMsg grammar")
