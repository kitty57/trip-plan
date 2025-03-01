import streamlit as st
import google.generativeai as genai
import json
import random
from datetime import datetime
import time

# Page configuration with a custom theme
st.set_page_config(
    page_title="✈️ Adventure Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with animations and more vibrant design
st.markdown("""
<style>
    /* Main styling */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header styles */
    .main-header {
        font-size: 3.2rem;
        background: linear-gradient(90deg, #2196F3, #4CAF50, #FF9800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
        animation: gradient 6s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0% {background-position: 0% 50%}
        50% {background-position: 100% 50%}
        100% {background-position: 0% 50%}
    }
    
    .tagline {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .card {
        border-radius: 15px;
        padding: 1.5rem;
        background: white;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid #2196F3;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
    }
    
    .card-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2196F3;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Form styling */
    .stTextInput, .stSelectbox, .stSlider {
        margin-bottom: 1rem;
    }
    
    div[data-baseweb="base-input"] {
        border-radius: 10px !important;
    }
    
    input, select, textarea {
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    input:focus, select:focus, textarea:focus {
        border-color: #2196F3 !important;
        box-shadow: 0 0 0 2px rgba(33,150,243,0.2) !important;
    }
    
    /* Button styling */
    .primary-btn {
        background: linear-gradient(90deg, #2196F3, #4CAF50);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        display: inline-block;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(33,150,243,0.3);
    }
    
    .primary-btn:hover {
        background: linear-gradient(90deg, #1E88E5, #43A047);
        box-shadow: 0 6px 15px rgba(33,150,243,0.4);
        transform: translateY(-2px);
    }
    
    .secondary-btn {
        background: white;
        color: #2196F3;
        border: 2px solid #2196F3;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .secondary-btn:hover {
        background: #f0f8ff;
        transform: translateY(-2px);
    }
    
    /* Itinerary container */
    .plan-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        margin-top: 2rem;
        border-top: 5px solid #2196F3;
    }
    
    /* Day cards in itinerary */
    .day-card {
        background: #f9f9f9;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #FF9800;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #2196F3;
    }
    
    /* Loading animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        padding: 2rem;
        margin: 1rem 0;
        background: #f5f9ff;
        border-radius: 10px;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% {background-color: #f5f9ff;}
        50% {background-color: #e3f2fd;}
        100% {background-color: #f5f9ff;}
    }
    
    /* Customize selectbox */
    div[data-baseweb="select"] {
        border-radius: 10px !important;
    }
    
    /* Tips box */
    .tips-box {
        background: #e3f2fd;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .tips-header {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1565C0;
    }
    
    /* Progress bar */
    .progress-bar {
        height: 10px;
        background: #e0e0e0;
        border-radius: 5px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-value {
        height: 100%;
        background: linear-gradient(90deg, #2196F3, #4CAF50);
        border-radius: 5px;
        transition: width 0.5s ease;
    }
    
    /* Fade-in animation */
    .fade-in {
        animation: fadeIn 1s ease;
    }
    
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    
    /* Budget selector */
    .budget-option {
        cursor: pointer;
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
        transition: all 0.3s ease;
        background: #f5f5f5;
        margin: 0.25rem;
    }
    
    .budget-option:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .budget-selected {
        background: #bbdefb;
        border: 2px solid #2196F3;
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Emoji badge */
    .emoji-badge {
        display: inline-block;
        background: #f5f5f5;
        padding: 0.3rem 0.6rem;
        border-radius: 20px;
        margin-right: 0.5rem;
        font-size: 0.9rem;
    }
    
    /* Interests pills */
    .interest-pill {
        display: inline-block;
        background: #e3f2fd;
        color: #1565C0;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .interest-pill:hover, .interest-pill.selected {
        background: #2196F3;
        color: white;
        transform: scale(1.05);
    }
    
    /* Add some color classes */
    .text-primary { color: #2196F3; }
    .text-success { color: #4CAF50; }
    .text-warning { color: #FF9800; }
    .text-danger { color: #F44336; }
    
    .bg-light { background-color: #f5f7f9; }
    
    /* Footer style */
    .footer {
        text-align: center;
        padding: 2rem 0;
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Fun loading messages
LOADING_MESSAGES = [
    "Exploring hidden gems in {}...",
    "Finding the best local restaurants in {}...",
    "Crafting the perfect {} adventure...",
    "Calculating optimal routes around {}...",
    "Checking the weather in {} for your trip...",
    "Interviewing locals in {} for insider tips...",
    "Researching the most Instagram-worthy spots in {}...",
    "Finding the best viewpoints in {}...",
    "Discovering unique experiences in {}...",
    "Planning your perfect {} getaway..."
]

# Popular interest tags
POPULAR_INTERESTS = [
    "🏖️ Beaches", "🥾 Hiking", "🏛️ History", "🍴 Food", "🎭 Art",
    "🛍️ Shopping", "📸 Photography", "🎵 Music", "🏊 Swimming",
    "🚴 Cycling", "🧘 Wellness", "🍷 Wine", "🏞️ Nature", "🏙️ Urban",
    "⛰️ Mountains", "🌋 Adventure"
]

# Initialize session state variables if they don't exist
if 'interests_list' not in st.session_state:
    st.session_state.interests_list = []
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False
if 'budget_selection' not in st.session_state:
    st.session_state.budget_selection = "Moderate"
if 'itinerary_generated' not in st.session_state:
    st.session_state.itinerary_generated = False
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# App header with animated gradient
st.markdown("<h1 class='main-header'>✈️ Adventure Planner</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Craft your dream journey with our AI travel assistant</p>", unsafe_allow_html=True)

# Initialize Gemini API
def setup_gemini_api():
    # Hardcoded API key for demo (in a real app, use st.secrets)
    api_key = "AIzaSyC8DAChYdFPif4RgQSYVkneoMHKDvnjgrw"
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.session_state.api_key_valid = True
            return True
        except Exception as e:
            st.session_state.api_key_valid = False
            return False
    return False

# Sidebar with inspiration and tips
with st.sidebar:
    st.markdown("<div class='sidebar-header'>🧭 Travel Companion</div>", unsafe_allow_html=True)
    
    # API setup (now automatic)
    api_ready = setup_gemini_api()
    
    # Destination inspiration
    st.markdown("### ✨ Destination Inspiration")
    
    # Random destinations to inspire users
    inspirations = [
        {"place": "Kyoto, Japan", "highlight": "Cherry blossoms & temples"},
        {"place": "Santorini, Greece", "highlight": "White buildings & sunsets"},
        {"place": "Banff, Canada", "highlight": "Mountain lakes & wildlife"},
        {"place": "Marrakech, Morocco", "highlight": "Markets & architecture"},
        {"place": "Queenstown, New Zealand", "highlight": "Adventure & scenery"}
    ]
    
    # Display 3 random destinations
    for dest in random.sample(inspirations, 3):
        st.markdown(f"""
        <div style='background:#f5f9ff; padding:0.7rem; border-radius:10px; margin-bottom:0.7rem;'>
            <div style='font-weight:600;'>{dest['place']}</div>
            <div style='font-size:0.9rem; color:#666;'>{dest['highlight']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Travel tips that change when page refreshes
    tips = [
        "🧳 Roll clothes instead of folding to save space in your luggage",
        "💊 Keep medications in your carry-on, not checked baggage",
        "📱 Download offline maps before traveling to new cities",
        "💰 Notify your bank before traveling internationally",
        "📷 Back up photos daily while traveling",
        "🔌 Bring a universal power adapter for international trips",
        "💦 Stay hydrated during flights to reduce jet lag",
        "🔐 Make digital copies of important documents",
        "💴 Always carry some local currency for emergencies",
        "🗣️ Learn a few basic phrases in the local language"
    ]
    
    st.markdown("### 💡 Travel Tip of the Day")
    st.info(random.choice(tips))
    
    st.markdown("---")
    
    # Season recommendations
    current_month = datetime.now().month
    season_recommendations = {
        "Winter (Dec-Feb)": ["Swiss Alps", "Aspen", "Northern Lights in Iceland", "Christmas markets in Germany"],
        "Spring (Mar-May)": ["Japan for cherry blossoms", "Netherlands for tulips", "Paris", "Washington DC"],
        "Summer (Jun-Aug)": ["Greek Islands", "Barcelona", "Amalfi Coast", "Iceland"],
        "Fall (Sep-Nov)": ["New England", "Kyoto", "Bavaria", "Scotland"]
    }
    
    current_season = ""
    if 3 <= current_month <= 5:
        current_season = "Spring (Mar-May)"
    elif 6 <= current_month <= 8:
        current_season = "Summer (Jun-Aug)"
    elif 9 <= current_month <= 11:
        current_season = "Fall (Sep-Nov)"
    else:
        current_season = "Winter (Dec-Feb)"
    
    st.markdown(f"### 🗓️ Best Places This Season")
    
    for place in season_recommendations[current_season]:
        st.markdown(f"- {place}")
    
    st.markdown("---")
    st.caption("Adventure Planner © 2025 | AI-Powered Travel")

# Main form for user input with improved interactive UI
if api_ready:
    # Create a card-like container for the planner form
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>🗺️ Plan Your Adventure</div>", unsafe_allow_html=True)
    
    # Make a 2-column layout for the form
    col1, col2 = st.columns(2)
    
    with col1:
        # Destination with autocomplete feel
        location = st.text_input("Where would you like to go?", 
                                placeholder="Type a destination (e.g., Bali, Indonesia)",
                                help="Enter a city, country, or region")
        
        # Travel dates with a more intuitive label
        dates = st.text_input("When are you traveling?", 
                             placeholder="Duration or specific dates (e.g., 7 days in June 2025)",
                             help="Enter your travel duration or specific dates")
        
        # Group type with emoji indicators
        group_options = {
            "Solo traveler": "👤",
            "Couple": "💑",
            "Family with kids": "👨‍👩‍👧‍👦",
            "Group of friends": "👯‍♂️",
            "Business trip": "💼"
        }
        
        group_type = st.selectbox("Who's going on this trip?", 
                                 list(group_options.keys()),
                                 format_func=lambda x: f"{group_options[x]} {x}")
        
    with col2:
        # Travel style/preferences
        preferences = st.text_input("What's your travel style?", 
                                   placeholder="E.g., luxury, off-the-beaten-path, relaxed pace...",
                                   help="Tell us how you like to travel")
        
        # Interactive budget selector with visual indicators
        st.markdown("### What's your budget level?")
        budget_options = ["Budget-friendly", "Moderate", "Luxury", "Ultra-luxury"]
        budget_icons = ["💰", "💰💰", "💰💰💰", "💰💰💰💰"]
        budget_cols = st.columns(4)
        
        for i, (option, icon) in enumerate(zip(budget_options, budget_icons)):
            with budget_cols[i]:
                selected_class = "budget-selected" if st.session_state.budget_selection == option else ""
                st.markdown(f"""
                <div class='budget-option {selected_class}' onclick="budget_click('{option}')">
                    <div style='font-size: 1.5rem;'>{icon}</div>
                    <div>{option}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(option, key=f"budget_{i}", help=f"Select {option} budget"):
                    st.session_state.budget_selection = option
        
        budget = st.session_state.budget_selection
    
    # Interest tags with interactive pills
    st.markdown("### What are you interested in? (Select all that apply)")
    
    # Create a grid for interest tags
    interest_cols = st.columns(4)
    col_idx = 0
    
    for interest in POPULAR_INTERESTS:
        with interest_cols[col_idx]:
            if st.button(interest, key=f"int_{interest}"):
                if interest in st.session_state.interests_list:
                    st.session_state.interests_list.remove(interest)
                else:
                    st.session_state.interests_list.append(interest)
        col_idx = (col_idx + 1) % 4
    
    # Display selected interests
    if st.session_state.interests_list:
        st.markdown("#### Selected interests:")
        interest_display = " ".join([f"<span class='interest-pill selected'>{i}</span>" for i in st.session_state.interests_list])
        st.markdown(f"<div>{interest_display}</div>", unsafe_allow_html=True)
        
        # Convert interests list to string for the API
        interests = ", ".join([i.split(" ", 1)[1] for i in st.session_state.interests_list])
    else:
        interests = ""
    
    # Additional information with examples
    additional_info = st.text_area("Anything else we should know?", 
                                  placeholder="E.g., dietary restrictions, mobility needs, special occasions...",
                                  help="Any special requirements or preferences")
    
    # Generate button with improved styling
    st.markdown("""
    <button class='primary-btn' id='generate-btn'>
        🚀 Create My Travel Itinerary
    </button>
    """, unsafe_allow_html=True)
    
    generate_pressed = st.button("Generate Itinerary", key="hidden_generate", help="Create your personalized travel plan")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Generate itinerary logic
    if generate_pressed:
        if not location:
            st.error("Please enter a destination to continue.")
        else:
            st.session_state.itinerary_generated = False
            st.session_state.progress = 0
            
            # Create a container for the loading animation
            loading_container = st.container()
            
            with loading_container:
                st.markdown("<div class='loading-animation fade-in'>", unsafe_allow_html=True)
                
                # Random loading message specific to the destination
                loading_message = random.choice(LOADING_MESSAGES).format(location.split(',')[0])
                st.markdown(f"<h3>{loading_message}</h3>", unsafe_allow_html=True)
                
                # Progress bar
                st.markdown("<div class='progress-bar'>", unsafe_allow_html=True)
                progress_bar = st.markdown("<div class='progress-value' style='width: 0%;'></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Loading indicator
                loading_status = st.empty()
                
                # Simulate progress
                for i in range(1, 6):
                    time.sleep(0.7)  # Simulate API processing time
                    st.session_state.progress = i * 20
                    # Update progress bar
                    progress_bar.markdown(f"<div class='progress-value' style='width: {st.session_state.progress}%;'></div>", unsafe_allow_html=True)
                    status_messages = [
                        "Researching destinations...",
                        "Finding local experiences...",
                        "Optimizing your itinerary...",
                        "Adding insider tips...",
                        "Finalizing your perfect trip..."
                    ]
                    loading_status.markdown(f"<p>{status_messages[i-1]}</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            try:
                # Create prompt for the generative model
                prompt_parts = [f"""
                Role:
                You are an advanced AI-powered travel planner specializing in creating personalized, detailed, and optimized travel itineraries for users based on their location they are planning to travel to, preferences, budget, and constraints. You provide clear, structured, and engaging travel recommendations with practical insights.

                Objectives:
                * Personalization: Tailor recommendations to location: {location}, user preferences: {preferences}, including budget: {budget}, travel dates: {dates}, interests: {interests}, and group type: {group_type}. Additional information: {additional_info}
                * Itinerary Optimization: Provide well-structured travel itineraries with time-efficient plans, ensuring minimal transit time and maximum experience.
                * Local Insights: Include hidden gems, must-visit landmarks, cultural etiquette, local food recommendations, and transportation tips.
                * Budget Awareness: Offer options appropriate for the {budget} budget level and suggest cost-saving tips where applicable.
                * Real-time Considerations: Consider weather, seasonality, local events, and safety advisories when planning recommendations.

                Response Structure:
                1. Introduction:
                   * Summarize the travel plan briefly, highlighting key experiences.
                   * Mention the seasonality and why it's a good time to visit.

                2. Itinerary (Day-wise Plan)
                   For each day:
                   * Morning Activity: Start with breakfast recommendations (local dishes if applicable) and a morning activity.
                   * Afternoon Activity: A mix of sightseeing, local markets, or adventure experiences.
                   * Evening Activity: Relaxing experiences like sunset spots, cultural events, or fine dining.
                   * Nightlife & Accommodation: Suggest nightlife spots if applicable and provide accommodation options.
                   * Logistics: Include the best way to commute between places (walking, public transport, rental, etc.).

                3. Additional Recommendations:
                   * Packing Tips: Based on season and climate.
                   * Local Customs & Etiquette: Important cultural dos and don'ts.
                   * Food Guide: Must-try dishes and best restaurants.
                   * Safety Tips: Warnings about scams, unsafe areas, and emergency contact info.
                   * Cost Estimate: Approximate budget breakdown (transport, food, activities).

                Rules & Constraints:
                * Always provide clear travel times and distances between locations.
                * Optimize routes to reduce unnecessary travel.
                * Ensure food recommendations align with dietary restrictions if specified.
                * Balance tourist attractions with unique, offbeat experiences.
                * Default to safety-first recommendations.
                * Format your response using markdown to make it readable and structured.
                * Use emoji for visual appeal where appropriate.
                * Your response should be vibrant and exciting.
                """]
                
                # Get response from Gemini
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content(prompt_parts)
                
                # Clear the loading animation
                loading_container.empty()
                
                st.session_state.itinerary_generated = True
                
                # Display results in an attractive container
                st.markdown("<div class='sub-header fade-in'>🎉 Your Adventure Awaits</div>", unsafe_allow_html=True)
                st.markdown("<div class='plan-container fade-in'>", unsafe_allow_html=True)
                
                # Process and display the itinerary with enhanced formatting
                itinerary_text = response.text
                st.markdown(itinerary_text)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    st.download_button(
                        label="📥 Download Itinerary",
                        data=itinerary_text,
                        file_name=f"adventure_plan_{location.replace(', ', '_')}.md",
                        mime="text/markdown"
                    )
                
                with col2:
                    st.button("✏️ Edit This Itinerary", help="Make changes to your current plan")
                
                with col3:
                    st.button("✨ Create New Adventure", help="Start a fresh travel plan")
                
                # Feedback section
                st.markdown("<div class='card fade-in' style='margin-top: 2rem;'>", unsafe_allow_html=True)
                st.markdown("<div class='card-header'>📣 How did we do?</div>", unsafe_allow_html=True)
                
                feedback_cols = st.columns(5)
                with feedback_cols[0]:
                    st.button("😍 Love it!")
                with feedback_cols[1]:
                    st.button("👍 Good")
                with feedback_cols[2]:
                    st.button("😐 Okay")
                with feedback_cols[3]:
                    st.button("👎 Could be better")
                with feedback_cols[4]:
                    st.button("💬 Send feedback")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"There was an error generating your itinerary: {str(e)}")
                st.info("Please try again with different inputs or simplify your request.")
else:
    st.warning("⚠️ API connection issue. Please refresh the page to try again.")

# Interactive elements for JavaScript (not functional in Streamlit but shows intent)
st.markdown("""
<script>
function budget_click(option) {
    // This would update the budget selection if JavaScript were enabled
    console.log('Budget selected:', option);
}
</script>
""", unsafe_allow_html=True)

# Footer with social links
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("""
Adventure Planner © 2025 | AI-Powered Travel Experiences<br>
[Instagram](https://instagram.com) · [Twitter](https://twitter.com) · [Facebook](https://facebook.com) · [Pinterest](https://pinterest.com)
""")
st.markdown("</div>", unsafe_allow_html=True)
