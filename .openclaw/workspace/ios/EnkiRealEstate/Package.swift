// swift-tools-version:5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "EnkiRealEstate",
    platforms: [.iOS(.v16), .macOS(.v13)],
    products: [
        .library(
            name: "EnkiRealEstate",
            targets: ["EnkiRealEstate"]),
    ],
    dependencies: [
        // No external dependencies - using native frameworks
    ],
    targets: [
        .target(
            name: "EnkiRealEstate",
            dependencies: [],
            path: "Sources",
            exclude: [],
            resources: [
                .process("Resources")
            ]
        ),
        .testTarget(
            name: "EnkiRealEstateTests",
            dependencies: ["EnkiRealEstate"],
            path: "Tests"
        ),
    ]
)