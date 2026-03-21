import SwiftUI

// MARK: - App Colors

extension Color {
    static let enkiPrimary = Color(red: 0.2, green: 0.4, blue: 0.8)
    static let enkiSecondary = Color(red: 0.4, green: 0.6, blue: 0.9)
    static let enkiAccent = Color(red: 0.9, green: 0.5, blue: 0.2)
    
    // Semantic colors
    static let success = Color.green
    static let warning = Color.orange
    static let error = Color.red
    static let info = Color.blue
}

// MARK: - App Fonts

extension Font {
    static let enkiLargeTitle = Font.system(size: 34, weight: .bold, design: .rounded)
    static let enkiTitle1 = Font.system(size: 28, weight: .bold, design: .rounded)
    static let enkiTitle2 = Font.system(size: 22, weight: .bold, design: .rounded)
    static let enkiTitle3 = Font.system(size: 20, weight: .semibold, design: .rounded)
    static let enkiHeadline = Font.system(size: 17, weight: .semibold, design: .default)
    static let enkiBody = Font.system(size: 17, weight: .regular, design: .default)
    static let enkiCallout = Font.system(size: 16, weight: .regular, design: .default)
    static let enkiSubheadline = Font.system(size: 15, weight: .regular, design: .default)
    static let enkiCaption = Font.system(size: 12, weight: .regular, design: .default)
}

// MARK: - App Theme

struct EnkiTheme {
    // Corner radii
    static let smallRadius: CGFloat = 8
    static let mediumRadius: CGFloat = 12
    static let largeRadius: CGFloat = 16
    
    // Spacing
    static let smallSpacing: CGFloat = 8
    static let mediumSpacing: CGFloat = 16
    static let largeSpacing: CGFloat = 24
    
    // Shadows
    static let shadowSmall = ShadowStyle(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
    static let shadowMedium = ShadowStyle(color: .black.opacity(0.15), radius: 8, x: 0, y: 4)
    static let shadowLarge = ShadowStyle(color: .black.opacity(0.2), radius: 16, x: 0, y: 8)
}

struct ShadowStyle {
    let color: Color
    let radius: CGFloat
    let x: CGFloat
    let y: CGFloat
}

// MARK: - Button Styles

struct EnkiPrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headline.weight(.semibold))
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color.enkiPrimary)
            .cornerRadius(12)
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .opacity(configuration.isPressed ? 0.9 : 1.0)
    }
}

struct EnkiSecondaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headline.weight(.semibold))
            .foregroundColor(.enkiPrimary)
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color.enkiPrimary.opacity(0.1))
            .cornerRadius(12)
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
    }
}

// MARK: - View Modifiers

extension View {
    func enkiCard() -> some View {
        self
            .padding()
            .background(Color(.secondarySystemBackground))
            .cornerRadius(EnkiTheme.mediumRadius)
    }
    
    func enkiShadow(_ style: ShadowStyle = EnkiTheme.shadowSmall) -> some View {
        self
            .shadow(color: style.color, radius: style.radius, x: style.x, y: style.y)
    }
}

// MARK: - Animation Standards

extension Animation {
    static let enkiSpring = Animation.spring(response: 0.3, dampingFraction: 0.8)
    static let enkiEase = Animation.easeInOut(duration: 0.2)
}