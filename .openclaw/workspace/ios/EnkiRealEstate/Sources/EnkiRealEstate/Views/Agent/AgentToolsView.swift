import SwiftUI

struct AgentToolsView: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    if appState.user?.role == .agent {
                        AgentDashboardSection()
                        LeadManagementSection()
                        CalendarSection()
                        MarketingToolsSection()
                    } else {
                        BecomeAgentSection()
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("Agent Tools")
        }
    }
}

struct AgentDashboardSection: View {
    @StateObject private var viewModel = AgentDashboardViewModel()
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Dashboard")
                .font(.title2.weight(.bold))
                .padding(.horizontal)
            
            LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 16) {
                DashboardCard(
                    title: "Active Leads",
                    value: "\(viewModel.dashboard?.totalLeads ?? 0)",
                    icon: "person.2.fill",
                    color: .blue
                )
                
                DashboardCard(
                    title: "Closed This Month",
                    value: "\(viewModel.dashboard?.closedDealsThisMonth ?? 0)",
                    icon: "checkmark.circle.fill",
                    color: .green
                )
                
                DashboardCard(
                    title: "Pipeline Value",
                    value: (viewModel.dashboard?.pipelineValue ?? 0).formatted(.currency(code: "USD")),
                    icon: "dollarsign.circle.fill",
                    color: .purple
                )
                
                DashboardCard(
                    title: "New This Week",
                    value: "\(viewModel.dashboard?.newLeadsThisWeek ?? 0)",
                    icon: "sparkles",
                    color: .orange
                )
            }
            .padding(.horizontal)
        }
    }
}

struct DashboardCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                Spacer()
            }
            
            Text(value)
                .font(.title2.weight(.bold))
                .lineLimit(1)
                .minimumScaleFactor(0.5)
            
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, minHeight: 100, alignment: .leading)
        .background(Color(.secondarySystemBackground))
        .cornerRadius(16)
    }
}

struct LeadManagementSection: View {
    @StateObject private var viewModel = LeadManagementViewModel()
    @State private var showingLeadForm = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Text("Lead Management")
                    .font(.title2.weight(.bold))
                
                Spacer()
                
                Button(action: { showingLeadForm = true }) {
                    Image(systemName: "plus.circle.fill")
                        .font(.title3)
                        .foregroundColor(.enkiPrimary)
                }
            }
            .padding(.horizontal)
            
            // Lead filters
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(LeadStatus.allCases, id: \.self) { status in
                        FilterStatusChip(
                            status: status,
                            isSelected: viewModel.selectedStatus == status,
                            count: viewModel.leadCounts[status] ?? 0
                        ) {
                            viewModel.selectedStatus = status
                            Task { await viewModel.loadLeads() }
                        }
                    }
                }
                .padding(.horizontal)
            }
            
            // Lead list
            if viewModel.leads.isEmpty {
                ContentUnavailableView {
                    Label("No Leads", systemImage: "person.2.slash")
                } description: {
                    Text("No leads match the selected filter")
                }
                .frame(height: 150)
            } else {
                VStack(spacing: 12) {
                    ForEach(viewModel.leads.prefix(5)) { lead in
                        LeadRow(lead: lead)
                    }
                }
                .padding(.horizontal)
            }
            
            NavigationLink("View All Leads") {
                AllLeadsView()
            }
            .padding(.horizontal)
        }
        .sheet(isPresented: $showingLeadForm) {
            LeadFormView()
        }
    }
}

struct FilterStatusChip: View {
    let status: LeadStatus
    let isSelected: Bool
    let count: Int
    let action: () -> Void
    
    var color: Color {
        switch status {
        case .new: return .blue
        case .contacted: return .orange
        case .qualified: return .green
        case .negotiation: return .purple
        case .closed: return .green
        case .lost: return .red
        }
    }
    
    var body: some View {
        Button(action: action) {
            HStack(spacing: 6) {
                Circle()
                    .fill(color)
                    .frame(width: 8, height: 8)
                
                Text(status.rawValue.capitalized)
                    .font(.subheadline.weight(.medium))
                
                Text("\(count)")
                    .font(.caption.weight(.bold))
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(color.opacity(0.2))
                    .foregroundColor(color)
                    .cornerRadius(10)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(isSelected ? color.opacity(0.1) : Color(.secondarySystemBackground))
            .foregroundColor(isSelected ? color : .primary)
            .cornerRadius(20)
            .overlay(
                RoundedRectangle(cornerRadius: 20)
                    .stroke(isSelected ? color : Color.clear, lineWidth: 1)
            )
        }
    }
}

struct LeadRow: View {
    let lead: Lead
    
    var body: some View {
        HStack(spacing: 12) {
            // Avatar
            ZStack {
                Circle()
                    .fill(Color.enkiPrimary.opacity(0.1))
                    .frame(width: 50, height: 50)
                
                Text(initials)
                    .font(.headline.weight(.semibold))
                    .foregroundColor(.enkiPrimary)
            }
            
            VStack(alignment: .leading, spacing: 4) {
                Text("\(lead.firstName) \(lead.lastName)")
                    .font(.subheadline.weight(.semibold))
                
                Text(lead.email)
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                HStack(spacing: 8) {
                    StatusBadge(status: lead.status)
                    
                    if let source = lead.source {
                        Text(source)
                            .font(.caption2)
                            .foregroundColor(.secondary)
                    }
                }
            }
            
            Spacer()
            
            Button(action: {}) {
                Image(systemName: "phone.fill")
                    .foregroundColor(.enkiPrimary)
                    .padding(8)
                    .background(Color.enkiPrimary.opacity(0.1))
                    .clipShape(Circle())
            }
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(12)
    }
    
    private var initials: String {
        let first = String(lead.firstName.prefix(1))
        let last = String(lead.lastName.prefix(1))
        return first + last
    }
}

extension LeadStatus: CaseIterable {
    public static var allCases: [LeadStatus] {
        [.new, .contacted, .qualified, .negotiation, .closed, .lost]
    }
}

struct CalendarSection: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Text("Upcoming")
                    .font(.title2.weight(.bold))
                
                Spacer()
                
                NavigationLink("View Calendar") {
                    CalendarView()
                }
                .font(.subheadline)
                .foregroundColor(.enkiPrimary)
            }
            .padding(.horizontal)
            
            VStack(spacing: 12) {
                CalendarEventRow(
                    title: "Property Tour - 123 Main St",
                    time: "10:00 AM",
                    type: .tour
                )
                
                CalendarEventRow(
                    title: "Client Meeting - Johnson Family",
                    time: "2:00 PM",
                    type: .meeting
                )
                
                CalendarEventRow(
                    title: "Open House - 456 Oak Ave",
                    time: "4:00 PM",
                    type: .openHouse
                )
            }
            .padding(.horizontal)
        }
    }
}

struct CalendarEventRow: View {
    let title: String
    let time: String
    let type: EventType
    
    enum EventType {
        case tour, meeting, openHouse
        
        var color: Color {
            switch self {
            case .tour: return .blue
            case .meeting: return .green
            case .openHouse: return .purple
            }
        }
        
        var icon: String {
            switch self {
            case .tour: return "house.fill"
            case .meeting: return "person.2.fill"
            case .openHouse: return "door.left.hand.open"
            }
        }
    }
    
    var body: some View {
        HStack(spacing: 12) {
            VStack(alignment: .center, spacing: 4) {
                Image(systemName: type.icon)
                    .font(.title3)
                    .foregroundColor(type.color)
            }
            .frame(width: 50, height: 50)
            .background(type.color.opacity(0.1))
            .cornerRadius(10)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.subheadline.weight(.semibold))
                Text(time)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(12)
    }
}

struct MarketingToolsSection: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Marketing Tools")
                .font(.title2.weight(.bold))
                .padding(.horizontal)
            
            VStack(spacing: 12) {
                MarketingToolRow(
                    title: "Create Listing",
                    icon: "plus.square.fill",
                    color: .blue
                )
                
                MarketingToolRow(
                    title: "Social Media Posts",
                    icon: "shareplay",
                    color: .purple
                )
                
                MarketingToolRow(
                    title: "Email Campaigns",
                    icon: "envelope.fill",
                    color: .green
                )
                
                MarketingToolRow(
                    title: "Lead Qualification",
                    icon: "checkmark.shield.fill",
                    color: .orange
                )
            }
            .padding(.horizontal)
        }
    }
}

struct MarketingToolRow: View {
    let title: String
    let icon: String
    let color: Color
    
    var body: some View {
        Button(action: {}) {
            HStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.title3)
                    .foregroundColor(color)
                    .frame(width: 40)
                
                Text(title)
                    .font(.subheadline.weight(.medium))
                    .foregroundColor(.primary)
                
                Spacer()
                
                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding()
            .background(Color(.secondarySystemBackground))
            .cornerRadius(12)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct BecomeAgentSection: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "briefcase.fill")
                .font(.system(size: 60))
                .foregroundColor(.enkiPrimary)
            
            Text("Become an Agent")
                .font(.title2.weight(.bold))
            
            Text("Join our network of real estate professionals and get access to powerful AI tools")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
            
            Button(action: {}) {
                Text("Apply Now")
                    .fontWeight(.semibold)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.enkiPrimary)
                    .foregroundColor(.white)
                    .cornerRadius(12)
            }
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(16)
        .padding(.horizontal)
    }
}

// Additional views for navigation
struct AllLeadsView: View {
    var body: some View {
        Text("All Leads")
            .navigationTitle("All Leads")
    }
}

struct CalendarView: View {
    var body: some View {
        Text("Calendar")
            .navigationTitle("Calendar")
    }
}

struct LeadFormView: View {
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            Text("Lead Form")
                .navigationTitle("New Lead")
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Cancel") { dismiss() }
                    }
                }
        }
    }
}

@MainActor
class AgentDashboardViewModel: ObservableObject {
    @Published var dashboard: DashboardData?
    
    init() {
        Task { await loadDashboard() }
    }
    
    func loadDashboard() async {
        do {
            dashboard = try await NetworkManager.shared.getAgentDashboard()
        } catch {
            print("Failed to load dashboard: \(error)")
        }
    }
}

@MainActor
class LeadManagementViewModel: ObservableObject {
    @Published var leads: [Lead] = []
    @Published var selectedStatus: LeadStatus = .new
    @Published var leadCounts: [LeadStatus: Int] = [:]
    
    init() {
        Task { await loadLeads() }
    }
    
    func loadLeads() async {
        do {
            leads = try await NetworkManager.shared.getLeads(status: selectedStatus)
            
            // Load counts for all statuses
            for status in LeadStatus.allCases {
                let statusLeads = try? await NetworkManager.shared.getLeads(status: status)
                leadCounts[status] = statusLeads?.count ?? 0
            }
        } catch {
            print("Failed to load leads: \(error)")
        }
    }
}