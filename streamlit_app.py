import streamlit as st
import google.generativeai as genai
import textwrap
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Trip Planner Crew",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS to improve the look and feel
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #26A69A;
        font-weight: bold;
        margin-top: 2rem;
    }
    .stTextInput label, .stSelectBox label {
        color: #333;
        font-weight: bold;
    }
    .description {
        font-size: 1.1rem;
        color: #666;
        line-height: 1.5;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .plan-container {
        background-color: #f5f7f9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
    }
    .icon-text {
        font-size: 1.2rem;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<div class='main-header'>✈️ Trip Planner Crew 🌍</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>Generate a personalized travel itinerary with our AI-powered planner. Get detailed day-by-day plans tailored to your preferences, budget, and travel style.</p>", unsafe_allow_html=True)

# Initialize Gemini API
def setup_gemini_api():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    # If no API key in secrets, request it from user
    if not api_key:
        api_key = "AIzaSyC8DAChYdFPif4RgQSYVkneoMHKDvnjgrw"
    
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# Sidebar for API setup
with st.sidebar:
    st.title("🔑 API Configuration")
    api_ready = setup_gemini_api()
    
    if api_ready:
        st.success("✅ API Connected!")
    else:
        st.warning("⚠️ API Key Required")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - Be specific about your travel preferences
    - Include dietary restrictions if applicable
    - Specify if you prefer public transit or driving
    - Mention any mobility considerations
    """)
    
    st.markdown("---")
    st.markdown("### 📱 Connect")
    st.markdown("[GitHub Repo](https://github.com/yourusername/trip-planner-crew)")
    st.markdown("[Report Issues](mailto:youremail@example.com)")

# Main form for user input
if api_ready:
    st.markdown("<div class='sub-header'>🗺️ Plan Your Adventure</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input("🌎 Destination", placeholder="France, Paris")
        preferences = st.text_input("🎯 Travel Preferences", placeholder="Historical sites, museums, local cuisine")
        budget = st.select_slider("💰 Budget Range", 
                                 options=["Budget-friendly", "Moderate", "Luxury", "Ultra-luxury"],
                                 value="Moderate")
    
    with col2:
        dates = st.text_input("📅 Travel Dates/Duration", placeholder="7 days in June 2025")
        interests = st.text_input("🎭 Special Interests", placeholder="Art, photography, adventure sports")
        group_type = st.selectbox("👫 Travel Group", 
                                 ["Solo traveler", "Couple", "Family with kids", "Group of friends", "Business trip"])
    
    additional_info = st.text_area("📝 Additional Information", 
                                  placeholder="Any dietary restrictions, accessibility needs, or specific must-see attractions?")

    # Generate button
    generate_pressed = st.button("🚀 Generate Travel Itinerary", use_container_width=True)

    if generate_pressed:
        if not location:
            st.error("Please enter a destination to continue.")
        else:
            with st.spinner("✨ Creating your perfect travel itinerary. This may take a moment..."):
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
                    """]
                    
                    # Get response from Gemini
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    response = model.generate_content(prompt_parts)
                    
                    # Display results
                    st.markdown("<div class='sub-header'>🎉 Your Travel Itinerary</div>", unsafe_allow_html=True)
                    st.markdown("<div class='plan-container'>", unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add download buttons
                    st.download_button(
                        label="📥 Download Itinerary (TXT)",
                        data=response.text,
                        file_name=f"travel_plan_{location.replace(', ', '_')}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"There was an error generating your itinerary: {str(e)}")
                    st.info("Please check your API key and try again. If the problem persists, try simplifying your request or providing different inputs.")
else:
    st.info("👆 Please enter your Google Gemini API Key in the sidebar to get started.")

# Footer
st.markdown("---")
st.caption("Trip Planner Crew © 2025 | Powered by Google Gemini AI | Not a substitute for professional travel advice")
