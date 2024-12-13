package tree_sitter_git_msg_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_git_msg "github.com/tree-sitter/tree-sitter-git_msg/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_git_msg.Language())
	if language == nil {
		t.Errorf("Error loading GitMsg grammar")
	}
}
