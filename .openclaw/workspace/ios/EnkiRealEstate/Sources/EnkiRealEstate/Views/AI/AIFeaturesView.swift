import SwiftUI

struct AIChatView: View {
    @StateObject private var viewModel = AIChatViewModel()
    @State private var messageText = ""
    @Environment(\\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Chat messages
                ScrollView {
                    LazyVStack(spacing: 16) {
                        ForEach(viewModel.messages) { message in
                            ChatMessageView(message: message)
                        }
                        
                        if viewModel.isTyping {
                            HStack {
                                TypingIndicator()
                                Spacer()
                            }
                            .padding(.horizontal)
                        }
                    }
                    .padding()
                }
                
                // Quick suggestions
                if viewModel.suggestions.isEmpty == false {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            ForEach(viewModel.suggestions, id: \\.self) { suggestion in
                                Button(action: {
                                    messageText = suggestion
                                    sendMessage()
                                }) {
                                    Text(suggestion)
                                        .font(.caption)
                                        .padding(.horizontal, 12)
                                        .padding(.vertical, 8)
                                        .background(Color.enkiPrimary.opacity(0.1))
                                        .foregroundColor(.enkiPrimary)
                                        .cornerRadius(16)
                                }
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.vertical, 8)
                }
                
                // Input bar
                HStack(spacing: 12) {
                    TextField("Ask about properties...", text: $messageText)
                        .textFieldStyle(.roundedBorder)
                        .submitLabel(.send)
                        .onSubmit(sendMessage)
                    
                    Button(action: sendMessage) {
                        Image(systemName: "arrow.up.circle.fill")
                            .font(.title2)
                            .foregroundColor(messageText.isEmpty ? .gray : .enkiPrimary)
                    }
                    .disabled(messageText.isEmpty || viewModel.isTyping)
                }
                .padding()
                .background(.ultraThinMaterial)
            }
            .navigationTitle("Enki AI")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") {
                        dismiss()
                    }
                }
            }
        }
    }
    
    private func sendMessage() {
        guard !messageText.isEmpty else { return }
        let message = messageText
        messageText = ""
        Task {
            await viewModel.sendMessage(message)
        }
    }
}

struct ChatMessageView: View {
    let message: ChatMessage
    
    var isUser: Bool {
        message.role == .user
    }
    
    var body: some View {
        HStack {
            if isUser { Spacer() }
            
            VStack(alignment: isUser ? .trailing : .leading, spacing: 4) {
                HStack(spacing: 8) {
                    if !isUser {
                        Image(systemName: "brain.head.profile")
                            .foregroundColor(.enkiPrimary)
                    }
                    
                    Text(message.content)
                        .padding(12)
                        .background(isUser ? Color.enkiPrimary : Color(.secondarySystemBackground))
                        .foregroundColor(isUser ? .white : .primary)
                        .cornerRadius(16)
                    
                    if isUser {
                        Image(systemName: "person.circle.fill")
                            .foregroundColor(.enkiPrimary)
                    }
                }
                
                Text(message.timestamp, style: .time)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
            
            if !isUser { Spacer() }
        }
    }
}

struct TypingIndicator: View {
    @State private var animationPhase = 0
    
    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<3) { index in
                Circle()
                    .fill(Color.secondary)
                    .frame(width: 6, height: 6)
                    .offset(y: animationPhase == index ? -4 : 0)
                    .animation(.easeInOut(duration: 0.3).repeatForever(autoreverses: true), value: animationPhase)
            }
        }
        .padding(12)
        .background(Color(.secondarySystemBackground))
        .cornerRadius(16)
        .onAppear {
            withAnimation(.linear(duration: 0.6).repeatForever(autoreverses: false)) {
                animationPhase = 2
            }
        }
    }
}

struct ChatMessage: Identifiable {
    let id = UUID()
    let role: MessageRole
    let content: String
    let timestamp = Date()
    
    enum MessageRole {
        case user
        case assistant
    }
}

@MainActor
class AIChatViewModel: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var isTyping = false
    @Published var suggestions: [String] = [
        "Find homes under $500k",
        "Show me 3 bedroom houses",
        "What's the market like?",
        "Help me get pre-approved"
    ]
    
    init() {
        // Welcome message
        messages.append(ChatMessage(
            role: .assistant,
            content: "Hi! I'm Enki, your AI real estate assistant. I can help you find properties, estimate values, answer questions about the market, and more. What can I help you with today?"
        ))
    }
    
    func sendMessage(_ text: String) async {
        // Add user message
        messages.append(ChatMessage(role: .user, content: text))
        isTyping = true
        
        do {
            let context = messages.prefix(10).map { "\($0.role == .user ? "User" : "Assistant"): \($0.content)" }.joined(separator: "\n")
            let response = try await NetworkManager.shared.chatWithAI(message: text, context: context)
            
            messages.append(ChatMessage(role: .assistant, content: response.message))
            
            if let newSuggestions = response.suggestions {
                suggestions = newSuggestions
            }
        } catch {
            messages.append(ChatMessage(
                role: .assistant,
                content: "I'm sorry, I encountered an error. Please try again later."
            ))
        }
        
        isTyping = false
    }
}

// MARK: - AI Valuation View

struct AIVAluationView: View {
    @StateObject private var viewModel = ValuationViewModel()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Header
                    VStack(spacing: 8) {
                        Image(systemName: "chart.line.uptrend.xyaxis")
                            .font(.system(size: 60))
                            .foregroundColor(.enkiPrimary)
                        
                        Text("AI Property Valuation")
                            .font(.title2.weight(.bold))
                        
                        Text("Get an instant estimate powered by our AI")
                            .foregroundColor(.secondary)
                    }
                    .padding(.top, 20)
                    
                    // Input form
                    ValuationForm(viewModel: viewModel)
                    
                    // Results
                    if let result = viewModel.result {
                        ValuationResultView(result: result)
                    }
                }
                .padding()
            }
            .navigationTitle("Valuation")
        }
    }
}

struct ValuationForm: View {
    @ObservedObject var viewModel: ValuationViewModel
    
    var body: some View {
        VStack(spacing: 16) {
            TextField("Property Address", text: $viewModel.address)
                .textFieldStyle(EnkiTextFieldStyle())
            
            Picker("Property Type", selection: $viewModel.propertyType) {
                ForEach(PropertyType.allCases, id: \\.self) { type in
                    Text(type.displayName).tag(type)
                }
            }
            .pickerStyle(.segmented)
            
            HStack {
                TextField("Bedrooms", value: $viewModel.bedrooms, format: .number)
                    .textFieldStyle(EnkiTextFieldStyle())
                    .keyboardType(.numberPad)
                
                TextField("Bathrooms", value: $viewModel.bathrooms, format: .number)
                    .textFieldStyle(EnkiTextFieldStyle())
                    .keyboardType(.decimalPad)
            }
            
            TextField("Square Feet", value: $viewModel.squareFeet, format: .number)
                .textFieldStyle(EnkiTextFieldStyle())
                .keyboardType(.numberPad)
            
            TextField("Year Built (optional)", value: $viewModel.yearBuilt, format: .number)
                .textFieldStyle(EnkiTextFieldStyle())
                .keyboardType(.numberPad)
            
            Button(action: { Task { await viewModel.getValuation() } }) {
                if viewModel.isLoading {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                } else {
                    Text("Get Valuation")
                        .fontWeight(.semibold)
                }
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color.enkiPrimary)
            .foregroundColor(.white)
            .cornerRadius(12)
            .disabled(viewModel.isLoading || viewModel.address.isEmpty)
        }
    }
}

struct ValuationResultView: View {
    let result: ValuationResult
    
    var body: some View {
        VStack(spacing: 20) {
            // Estimated value
            VStack(spacing: 8) {
                Text("Estimated Value")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                Text("\(result.estimatedValue.formatted(.currency(code: "USD")))")
                    .font(.system(size: 48, weight: .bold))
                    .foregroundColor(.enkiPrimary)
                
                HStack {
                    Text("Range: \(result.valueRange.low.formatted(.currency(code: "USD"))) - \(result.valueRange.high.formatted(.currency(code: "USD")))")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                
                ConfidenceBadge(score: result.confidenceScore)
            }
            .padding()
            .background(Color(.secondarySystemBackground))
            .cornerRadius(16)
            
            // Market trends
            VStack(alignment: .leading, spacing: 12) {
                Text("Market Trends")
                    .font(.headline)
                
                HStack {
                    TrendItem(
                        title: "Appreciation",
                        value: "+\(String(format: "%.1f", result.marketTrends.appreciationRate * 100))%",
                        isPositive: result.marketTrends.appreciationRate > 0
                    )
                    
                    TrendItem(
                        title: "Days on Market",
                        value: "\(result.marketTrends.daysOnMarket)",
                        isPositive: result.marketTrends.daysOnMarket < 30
                    )
                }
            }
            .padding()
            .background(Color(.secondarySystemBackground))
            .cornerRadius(16)
            
            // Comparables
            if !result.comparableProperties.isEmpty {
                VStack(alignment: .leading, spacing: 12) {
                    Text("Comparable Properties")
                        .font(.headline)
                    
                    ForEach(result.comparableProperties.prefix(3)) { property in
                        ComparableRow(property: property)
                    }
                }
                .padding()
                .background(Color(.secondarySystemBackground))
                .cornerRadius(16)
            }
        }
    }
}

struct ConfidenceBadge: View {
    let score: Double
    
    var color: Color {
        if score >= 0.8 { return .green }
        if score >= 0.6 { return .orange }
        return .red
    }
    
    var label: String {
        if score >= 0.8 { return "High Confidence" }
        if score >= 0.6 { return "Medium Confidence" }
        return "Low Confidence"
    }
    
    var body: some View {
        Text(label)
            .font(.caption.weight(.medium))
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(color.opacity(0.1))
            .foregroundColor(color)
            .cornerRadius(12)
    }
}

struct TrendItem: View {
    let title: String
    let value: String
    let isPositive: Bool
    
    var body: some View {
        VStack(spacing: 4) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            Text(value)
                .font(.title3.weight(.bold))
                .foregroundColor(isPositive ? .green : .orange)
        }
        .frame(maxWidth: .infinity)
    }
}

struct ComparableRow: View {
    let property: Property
    
    var body: some View {
        HStack {
            RoundedRectangle(cornerRadius: 8)
                .fill(Color.gray.opacity(0.2))
                .frame(width: 60, height: 60)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(property.formattedPrice)
                    .font(.subheadline.weight(.semibold))
                Text(property.address.city)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Text("\(property.bedrooms)bd \n\(property.bathrooms)ba")
                .font(.caption)
                .multilineTextAlignment(.trailing)
        }
    }
}

@MainActor
class ValuationViewModel: ObservableObject {
    @Published var address = ""
    @Published var propertyType: PropertyType = .house
    @Published var bedrooms = 3
    @Published var bathrooms = 2.0
    @Published var squareFeet = 1500.0
    @Published var yearBuilt: Int?
    
    @Published var isLoading = false
    @Published var result: ValuationResult?
    
    func getValuation() async {
        isLoading = true
        
        let request = ValuationRequest(
            address: address,
            propertyType: propertyType,
            bedrooms: bedrooms,
            bathrooms: bathrooms,
            squareFeet: squareFeet,
            yearBuilt: yearBuilt
        )
        
        do {
            result = try await NetworkManager.shared.getPropertyValuation(request: request)
        } catch {
            print("Valuation failed: \(error)")
        }
        
        isLoading = false
    }
}