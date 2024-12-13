import XCTest
import SwiftTreeSitter
import TreeSitterGitMsg

final class TreeSitterGitMsgTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_git_msg())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading GitMsg grammar")
    }
}
