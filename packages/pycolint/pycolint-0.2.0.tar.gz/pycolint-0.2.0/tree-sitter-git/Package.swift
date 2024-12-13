// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "TreeSitterGitMsg",
    products: [
        .library(name: "TreeSitterGitMsg", targets: ["TreeSitterGitMsg"]),
    ],
    dependencies: [
        .package(url: "https://github.com/ChimeHQ/SwiftTreeSitter", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "TreeSitterGitMsg",
            dependencies: [],
            path: ".",
            sources: [
                "src/parser.c",
                // NOTE: if your language has an external scanner, add it here.
            ],
            resources: [
                .copy("queries")
            ],
            publicHeadersPath: "bindings/swift",
            cSettings: [.headerSearchPath("src")]
        ),
        .testTarget(
            name: "TreeSitterGitMsgTests",
            dependencies: [
                "SwiftTreeSitter",
                "TreeSitterGitMsg",
            ],
            path: "bindings/swift/TreeSitterGitMsgTests"
        )
    ],
    cLanguageStandard: .c11
)
