import SwiftUI

struct AuthView: View {
    @State private var showLogin = true
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Logo and branding
                VStack(spacing: 16) {
                    Image(systemName: "house.circle.fill")
                        .resizable()
                        .frame(width: 100, height: 100)
                        .foregroundColor(.enkiPrimary)
                    
                    Text("Enki Real Estate")
                        .font(.largeTitle.weight(.bold))
                    
                    Text("Your AI-Powered Property Partner")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                .padding(.top, 60)
                .padding(.bottom, 40)
                
                // Auth forms
                VStack {
                    if showLogin {
                        LoginView()
                    } else {
                        RegisterView()
                    }
                }
                
                Spacer()
                
                // Toggle between login/register
                Button(action: { showLogin.toggle() }) {
                    Text(showLogin ? "Don't have an account? Sign up" : "Already have an account? Log in")
                        .font(.subheadline)
                        .foregroundColor(.enkiPrimary)
                }
                .padding(.bottom, 30)
            }
            .padding()
        }
    }
}

struct LoginView: View {
    @EnvironmentObject var appState: AppState
    @State private var email = ""
    @State private var password = ""
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        VStack(spacing: 20) {
            TextField("Email", text: $email)
                .textContentType(.emailAddress)
                .keyboardType(.emailAddress)
                .autocapitalization(.none)
                .textFieldStyle(EnkiTextFieldStyle())
            
            SecureField("Password", text: $password)
                .textContentType(.password)
                .textFieldStyle(EnkiTextFieldStyle())
            
            if let error = errorMessage {
                Text(error)
                    .font(.caption)
                    .foregroundColor(.red)
            }
            
            Button(action: login) {
                HStack {
                    if isLoading {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    } else {
                        Text("Log In")
                            .fontWeight(.semibold)
                    }
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.enkiPrimary)
                .foregroundColor(.white)
                .cornerRadius(12)
            }
            .disabled(isLoading || email.isEmpty || password.isEmpty)
        }
    }
    
    private func login() {
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                let response = try await NetworkManager.shared.login(email: email, password: password)
                KeychainManager.shared.saveToken(response.token)
                await MainActor.run {
                    appState.isAuthenticated = true
                    appState.user = response.user
                    isLoading = false
                }
            } catch {
                await MainActor.run {
                    errorMessage = "Login failed. Please check your credentials."
                    isLoading = false
                }
            }
        }
    }
}

struct RegisterView: View {
    @EnvironmentObject var appState: AppState
    @State private var firstName = ""
    @State private var lastName = ""
    @State private var email = ""
    @State private var phone = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                TextField("First Name", text: $firstName)
                    .textContentType(.givenName)
                    .textFieldStyle(EnkiTextFieldStyle())
                
                TextField("Last Name", text: $lastName)
                    .textContentType(.familyName)
                    .textFieldStyle(EnkiTextFieldStyle())
                
                TextField("Email", text: $email)
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
                    .textFieldStyle(EnkiTextFieldStyle())
                
                TextField("Phone (optional)", text: $phone)
                    .textContentType(.telephoneNumber)
                    .keyboardType(.phonePad)
                    .textFieldStyle(EnkiTextFieldStyle())
                
                SecureField("Password", text: $password)
                    .textContentType(.newPassword)
                    .textFieldStyle(EnkiTextFieldStyle())
                
                SecureField("Confirm Password", text: $confirmPassword)
                    .textContentType(.newPassword)
                    .textFieldStyle(EnkiTextFieldStyle())
                
                if let error = errorMessage {
                    Text(error)
                        .font(.caption)
                        .foregroundColor(.red)
                }
                
                Button(action: register) {
                    HStack {
                        if isLoading {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        } else {
                            Text("Create Account")
                                .fontWeight(.semibold)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.enkiPrimary)
                    .foregroundColor(.white)
                    .cornerRadius(12)
                }
                .disabled(isLoading || !isValid)
            }
        }
    }
    
    private var isValid: Bool {
        !firstName.isEmpty && !lastName.isEmpty && !email.isEmpty &&
        password.count >= 8 && password == confirmPassword
    }
    
    private func register() {
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                let response = try await NetworkManager.shared.register(
                    email: email,
                    password: password,
                    firstName: firstName,
                    lastName: lastName,
                    phone: phone.isEmpty ? nil : phone
                )
                KeychainManager.shared.saveToken(response.token)
                await MainActor.run {
                    appState.isAuthenticated = true
                    appState.user = response.user
                    isLoading = false
                }
            } catch {
                await MainActor.run {
                    errorMessage = "Registration failed. Please try again."
                    isLoading = false
                }
            }
        }
    }
}

struct EnkiTextFieldStyle: TextFieldStyle {
    func _body(configuration: TextField<Self._Label>) -> some View {
        configuration
            .padding()
            .background(Color(.secondarySystemBackground))
            .cornerRadius(10)
    }
}