"""
Comprehensive mock data for the AI-powered trip planner.
Contains destinations, hotels, activities, events, and user preferences.
Updated for 2025 with current market trends and pricing.
"""

from typing import Dict, List, Any
import random
from datetime import datetime, timedelta

# Destination categories and interests
DESTINATION_CATEGORIES = [
    "adventure", "cultural", "relaxation", "historical", "nature", 
    "urban", "beach", "mountain", "spiritual", "culinary"
]

ACTIVITY_TYPES = [
    "sightseeing", "adventure", "cultural", "food", "shopping", 
    "entertainment", "nature", "sports", "wellness", "educational"
]

# Mock destinations with detailed information - India Specific (Updated 2025)
DESTINATIONS = {
    "delhi": {
        "name": "New Delhi, India",
        "country": "India",
        "categories": ["cultural", "historical", "urban", "culinary"],
        "best_months": [10, 11, 12, 1, 2, 3],
        "avg_temp_range": {"min": 5, "max": 45},
        "currency": "INR",
        "avg_daily_budget": {"budget": 2140, "mid": 4320, "luxury": 8800},
        "description": "India's capital city, rich in Mughal architecture, street food, and political heritage",
        "popular_areas": ["Connaught Place", "Chandni Chowk", "Khan Market", "Hauz Khas"],
        "coordinates": {"lat": 28.6139, "lng": 77.2090}
    },
    "mumbai": {
        "name": "Mumbai, India",
        "country": "India",
        "categories": ["urban", "entertainment", "culinary", "cultural"],
        "best_months": [10, 11, 12, 1, 2, 3],
        "avg_temp_range": {"min": 16, "max": 36},
        "currency": "INR",
        "avg_daily_budget": {"budget": 2675, "mid": 5400, "luxury": 11000},
        "description": "Financial capital of India, Bollywood hub, and city of dreams",
        "popular_areas": ["Marine Drive", "Bandra", "Colaba", "Juhu"],
        "coordinates": {"lat": 19.0760, "lng": 72.8777}
    },
    "goa": {
        "name": "Goa, India",
        "country": "India",
        "categories": ["beach", "relaxation", "adventure", "culinary"],
        "best_months": [11, 12, 1, 2, 3, 4],
        "avg_temp_range": {"min": 20, "max": 35},
        "currency": "INR",
        "avg_daily_budget": {"budget": 1926, "mid": 3780, "luxury": 7700},
        "description": "Coastal paradise with Portuguese heritage, beaches, and vibrant nightlife",
        "popular_areas": ["North Goa", "South Goa", "Panaji", "Old Goa"],
        "coordinates": {"lat": 15.2993, "lng": 74.1240}
    },
    "rajasthan": {
        "name": "Jaipur, Rajasthan",
        "country": "India",
        "categories": ["historical", "cultural", "adventure", "luxury"],
        "best_months": [10, 11, 12, 1, 2, 3],
        "avg_temp_range": {"min": 2, "max": 47},
        "currency": "INR",
        "avg_daily_budget": {"budget": 1605, "mid": 3240, "luxury": 6600},
        "description": "Pink City with magnificent palaces, forts, and royal heritage",
        "popular_areas": ["City Palace", "Amber Fort", "Hawa Mahal", "Johari Bazaar"],
        "coordinates": {"lat": 26.9124, "lng": 75.7873}
    },
    "kerala": {
        "name": "Kerala, India",
        "country": "India",
        "categories": ["nature", "relaxation", "cultural", "wellness"],
        "best_months": [9, 10, 11, 12, 1, 2, 3, 4],
        "avg_temp_range": {"min": 18, "max": 36},
        "currency": "INR",
        "avg_daily_budget": {"budget": 1284, "mid": 2700, "luxury": 5500},
        "description": "God's Own Country with backwaters, hill stations, and Ayurvedic treatments",
        "popular_areas": ["Alleppey", "Munnar", "Kochi", "Thekkady"],
        "coordinates": {"lat": 10.8505, "lng": 76.2711}
    },
    "himachal": {
        "name": "Himachal Pradesh, India",
        "country": "India",
        "categories": ["adventure", "nature", "mountain", "spiritual"],
        "best_months": [3, 4, 5, 6, 9, 10, 11],
        "avg_temp_range": {"min": -5, "max": 30},
        "currency": "INR",
        "avg_daily_budget": {"budget": 1070, "mid": 2160, "luxury": 4400},
        "description": "Himalayan paradise with snow-capped peaks, adventure sports, and hill stations",
        "popular_areas": ["Manali", "Shimla", "Dharamshala", "Kasol"],
        "coordinates": {"lat": 31.1048, "lng": 77.1734}
    },
    "ladakh": {
        "name": "Leh-Ladakh, India",
        "country": "India",
        "categories": ["adventure", "nature", "mountain", "spiritual", "cultural"],
        "best_months": [5, 6, 7, 8, 9],
        "avg_temp_range": {"min": -20, "max": 25},
        "currency": "INR",
        "avg_daily_budget": {"budget": 1500, "mid": 3000, "luxury": 6000},
        "description": "Little Tibet with high-altitude deserts, Buddhist monasteries, and adventure activities",
        "popular_areas": ["Leh", "Nubra Valley", "Pangong Lake", "Tso Moriri"],
        "coordinates": {"lat": 34.1526, "lng": 77.5770}
    },
    "andaman": {
        "name": "Andaman and Nicobar Islands, India",
        "country": "India",
        "categories": ["beach", "adventure", "nature", "relaxation"],
        "best_months": [10, 11, 12, 1, 2, 3, 4],
        "avg_temp_range": {"min": 23, "max": 31},
        "currency": "INR",
        "avg_daily_budget": {"budget": 2000, "mid": 4000, "luxury": 8000},
        "description": "Pristine islands with crystal-clear waters, coral reefs, and marine life",
        "popular_areas": ["Port Blair", "Havelock Island", "Neil Island", "Ross Island"],
        "coordinates": {"lat": 11.7401, "lng": 92.6586}
    }
}

# Mock hotels with detailed information - India Specific (Updated 2025 Pricing)
HOTELS = {
    "delhi": [
        {
            "name": "The Imperial New Delhi",
            "category": "luxury",
            "rating": 4.8,
            "price_per_night": {"budget": 8560, "mid": 12960, "luxury": 22000},
            "amenities": ["wifi", "breakfast", "gym", "spa", "pool", "restaurant", "concierge"],
            "location": "Connaught Place",
            "description": "Heritage luxury hotel with colonial architecture and modern amenities"
        },
        {
            "name": "Hotel Tara Palace Chandni Chowk",
            "category": "mid",
            "rating": 4.2,
            "price_per_night": {"budget": 3210, "mid": 4860, "luxury": 6600},
            "amenities": ["wifi", "breakfast", "restaurant", "room service"],
            "location": "Chandni Chowk",
            "description": "Traditional hotel in the heart of Old Delhi"
        },
        {
            "name": "Zostel Delhi",
            "category": "budget",
            "rating": 4.0,
            "price_per_night": {"budget": 856, "mid": 1296, "luxury": 1980},
            "amenities": ["wifi", "common area", "kitchen"],
            "location": "Paharganj",
            "description": "Modern hostel with vibrant backpacker community"
        }
    ],
    "mumbai": [
        {
            "name": "The Taj Mahal Palace Mumbai",
            "category": "luxury",
            "rating": 4.9,
            "price_per_night": {"budget": 16050, "mid": 27000, "luxury": 44000},
            "amenities": ["wifi", "breakfast", "gym", "spa", "pool", "restaurant", "heritage"],
            "location": "Colaba",
            "description": "Iconic heritage hotel overlooking the Gateway of India"
        },
        {
            "name": "Hotel Suba Palace",
            "category": "mid",
            "rating": 4.1,
            "price_per_night": {"budget": 4280, "mid": 6480, "luxury": 8800},
            "amenities": ["wifi", "breakfast", "restaurant", "business center"],
            "location": "Colaba",
            "description": "Comfortable hotel near major attractions"
        },
        {
            "name": "Backpacker Panda Colaba",
            "category": "budget",
            "rating": 3.9,
            "price_per_night": {"budget": 1070, "mid": 1620, "luxury": 2200},
            "amenities": ["wifi", "common area", "lockers"],
            "location": "Colaba",
            "description": "Budget-friendly hostel for young travelers"
        }
    ],
    "goa": [
        {
            "name": "Taj Exotica Resort & Spa Goa",
            "category": "luxury",
            "rating": 4.7,
            "price_per_night": {"budget": 12840, "mid": 19440, "luxury": 33000},
            "amenities": ["wifi", "breakfast", "spa", "pool", "beach access", "restaurant"],
            "location": "Benaulim Beach",
            "description": "Luxury beach resort with pristine coastline views"
        },
        {
            "name": "Lemon Tree Hotel Candolim",
            "category": "mid",
            "rating": 4.3,
            "price_per_night": {"budget": 3745, "mid": 5400, "luxury": 7700},
            "amenities": ["wifi", "breakfast", "pool", "restaurant", "beach shuttle"],
            "location": "Candolim",
            "description": "Modern hotel near popular beaches"
        },
        {
            "name": "Zostel Goa",
            "category": "budget",
            "rating": 4.2,
            "price_per_night": {"budget": 856, "mid": 1296, "luxury": 1760},
            "amenities": ["wifi", "common area", "bike rental", "beach access"],
            "location": "Anjuna",
            "description": "Vibrant hostel near famous beaches and nightlife"
        }
    ],
    "rajasthan": [
        {
            "name": "Rambagh Palace Jaipur",
            "category": "luxury",
            "rating": 4.8,
            "price_per_night": {"budget": 21400, "mid": 37800, "luxury": 66000},
            "amenities": ["wifi", "breakfast", "spa", "pool", "heritage", "restaurant", "palace"],
            "location": "Bhawani Singh Road",
            "description": "Former royal palace turned luxury heritage hotel"
        },
        {
            "name": "Hotel Pearl Palace",
            "category": "mid",
            "rating": 4.4,
            "price_per_night": {"budget": 2140, "mid": 3240, "luxury": 4950},
            "amenities": ["wifi", "breakfast", "restaurant", "rooftop"],
            "location": "Hathroi Fort",
            "description": "Family-run heritage hotel with traditional Rajasthani hospitality"
        },
        {
            "name": "Moustache Hostel Jaipur",
            "category": "budget",
            "rating": 4.1,
            "price_per_night": {"budget": 642, "mid": 972, "luxury": 1320},
            "amenities": ["wifi", "common area", "kitchen", "cultural activities"],
            "location": "Bani Park",
            "description": "Backpacker hostel with cultural immersion programs"
        }
    ],
    "kerala": [
        {
            "name": "Kumarakom Lake Resort",
            "category": "luxury",
            "rating": 4.6,
            "price_per_night": {"budget": 8560, "mid": 16200, "luxury": 27500},
            "amenities": ["wifi", "breakfast", "spa", "ayurveda", "backwater", "restaurant"],
            "location": "Kumarakom",
            "description": "Luxury backwater resort with traditional Kerala architecture"
        },
        {
            "name": "Spice Tree Munnar",
            "category": "mid",
            "rating": 4.3,
            "price_per_night": {"budget": 2675, "mid": 4320, "luxury": 6600},
            "amenities": ["wifi", "breakfast", "mountain view", "restaurant", "trekking"],
            "location": "Munnar",
            "description": "Hill station resort surrounded by tea plantations"
        },
        {
            "name": "Backwater Hostel Alleppey",
            "category": "budget",
            "rating": 4.0,
            "price_per_night": {"budget": 749, "mid": 1080, "luxury": 1540},
            "amenities": ["wifi", "common area", "houseboat tours", "kitchen"],
            "location": "Alleppey",
            "description": "Budget accommodation with easy access to backwater tours"
        }
    ],
    "himachal": [
        {
            "name": "The Oberoi Cecil Shimla",
            "category": "luxury",
            "rating": 4.7,
            "price_per_night": {"budget": 8560, "mid": 12960, "luxury": 22000},
            "amenities": ["wifi", "breakfast", "spa", "mountain view", "heritage", "restaurant"],
            "location": "Shimla Mall Road",
            "description": "Colonial heritage hotel with panoramic Himalayan views"
        },
        {
            "name": "Hotel Snow Valley Manali",
            "category": "mid",
            "rating": 4.2,
            "price_per_night": {"budget": 2140, "mid": 3780, "luxury": 5500},
            "amenities": ["wifi", "breakfast", "mountain view", "restaurant", "adventure sports"],
            "location": "Manali",
            "description": "Mountain resort perfect for adventure enthusiasts"
        },
        {
            "name": "Zostel Kasol",
            "category": "budget",
            "rating": 4.3,
            "price_per_night": {"budget": 856, "mid": 1296, "luxury": 1760},
            "amenities": ["wifi", "common area", "trekking", "bonfire", "mountain view"],
            "location": "Kasol",
            "description": "Backpacker paradise in the Parvati Valley"
        }
    ],
    "ladakh": [
        {
            "name": "The Grand Dragon Ladakh",
            "category": "luxury",
            "rating": 4.6,
            "price_per_night": {"budget": 10700, "mid": 16200, "luxury": 27500},
            "amenities": ["wifi", "breakfast", "spa", "mountain view", "restaurant", "oxygen support"],
            "location": "Leh",
            "description": "Luxury hotel with traditional Ladakhi architecture and modern amenities"
        },
        {
            "name": "Hotel Singge Palace",
            "category": "mid",
            "rating": 4.3,
            "price_per_night": {"budget": 3210, "mid": 4860, "luxury": 7150},
            "amenities": ["wifi", "breakfast", "mountain view", "restaurant", "garden"],
            "location": "Leh",
            "description": "Traditional Ladakhi palace hotel with stunning mountain views"
        },
        {
            "name": "Zostel Leh",
            "category": "budget",
            "rating": 4.2,
            "price_per_night": {"budget": 1070, "mid": 1620, "luxury": 2200},
            "amenities": ["wifi", "common area", "trekking", "cultural activities"],
            "location": "Leh",
            "description": "Adventure hostel for high-altitude trekkers and bikers"
        }
    ],
    "andaman": [
        {
            "name": "Taj Exotica Resort & Spa Andamans",
            "category": "luxury",
            "rating": 4.8,
            "price_per_night": {"budget": 17130, "mid": 25920, "luxury": 44000},
            "amenities": ["wifi", "breakfast", "spa", "pool", "beach access", "water sports"],
            "location": "Radhanagar Beach",
            "description": "Exclusive island resort with pristine beaches and marine activities"
        },
        {
            "name": "SeaShell Havelock",
            "category": "mid",
            "rating": 4.4,
            "price_per_night": {"budget": 4280, "mid": 6480, "luxury": 8800},
            "amenities": ["wifi", "breakfast", "beach access", "restaurant", "diving center"],
            "location": "Havelock Island",
            "description": "Beachfront resort perfect for diving and snorkeling"
        },
        {
            "name": "Emerald Gecko Resort",
            "category": "budget",
            "rating": 4.1,
            "price_per_night": {"budget": 1284, "mid": 1944, "luxury": 2640},
            "amenities": ["wifi", "common area", "beach access", "bicycle rental"],
            "location": "Neil Island",
            "description": "Eco-friendly budget resort with island charm"
        }
    ]
}

# Mock activities and events - India Specific (Enhanced for 2025)
ACTIVITIES = {
    "delhi": [
        {
            "name": "Red Fort (Lal Qila)",
            "type": "historical",
            "duration": 3,
            "cost": {"budget": 55, "mid": 110, "luxury": 220},
            "rating": 4.5,
            "description": "Magnificent Mughal fortress and UNESCO World Heritage Site",
            "best_time": "morning",
            "location": "Chandni Chowk",
            "categories": ["historical", "cultural", "architecture"]
        },
        {
            "name": "India Gate & Rajpath",
            "type": "sightseeing",
            "duration": 2,
            "cost": {"budget": 0, "mid": 55, "luxury": 165},
            "rating": 4.3,
            "description": "War memorial and ceremonial boulevard",
            "best_time": "evening",
            "location": "Rajpath",
            "categories": ["historical", "sightseeing"]
        },
        {
            "name": "Chandni Chowk Food Walk",
            "type": "culinary",
            "duration": 4,
            "cost": {"budget": 320, "mid": 540, "luxury": 880},
            "rating": 4.7,
            "description": "Explore Old Delhi's famous street food scene",
            "best_time": "evening",
            "location": "Chandni Chowk",
            "categories": ["culinary", "cultural"]
        },
        {
            "name": "Lotus Temple",
            "type": "spiritual",
            "duration": 2,
            "cost": {"budget": 0, "mid": 55, "luxury": 110},
            "rating": 4.4,
            "description": "Bahai House of Worship with lotus-shaped architecture",
            "best_time": "morning",
            "location": "Kalkaji",
            "categories": ["spiritual", "architecture"]
        },
        {
            "name": "Akshardham Temple",
            "type": "spiritual",
            "duration": 4,
            "cost": {"budget": 170, "mid": 320, "luxury": 550},
            "rating": 4.6,
            "description": "Modern Hindu temple complex with cultural exhibitions",
            "best_time": "morning",
            "location": "Akshardham",
            "categories": ["spiritual", "cultural", "architecture"]
        }
    ],
    "mumbai": [
        {
            "name": "Gateway of India",
            "type": "historical",
            "duration": 2,
            "cost": {"budget": 0, "mid": 110, "luxury": 330},
            "rating": 4.2,
            "description": "Iconic colonial monument overlooking the Arabian Sea",
            "best_time": "evening",
            "location": "Colaba",
            "categories": ["historical", "sightseeing"]
        },
        {
            "name": "Bollywood Studio Tour",
            "type": "entertainment",
            "duration": 6,
            "cost": {"budget": 1605, "mid": 2700, "luxury": 4400},
            "rating": 4.6,
            "description": "Behind-the-scenes tour of Bollywood film studios",
            "best_time": "morning",
            "location": "Film City",
            "categories": ["entertainment", "cultural"]
        },
        {
            "name": "Marine Drive Evening Walk",
            "type": "sightseeing",
            "duration": 2,
            "cost": {"budget": 0, "mid": 220, "luxury": 550},
            "rating": 4.4,
            "description": "Scenic waterfront promenade known as Queen's Necklace",
            "best_time": "evening",
            "location": "Marine Drive",
            "categories": ["sightseeing", "relaxation"]
        },
        {
            "name": "Dharavi Slum Tour",
            "type": "cultural",
            "duration": 3,
            "cost": {"budget": 860, "mid": 1300, "luxury": 2200},
            "rating": 4.5,
            "description": "Educational tour of Asia's largest slum community",
            "best_time": "morning",
            "location": "Dharavi",
            "categories": ["cultural", "educational"]
        },
        {
            "name": "Elephanta Caves",
            "type": "historical",
            "duration": 5,
            "cost": {"budget": 300, "mid": 550, "luxury": 1100},
            "rating": 4.3,
            "description": "Ancient rock-cut caves dedicated to Lord Shiva",
            "best_time": "morning",
            "location": "Elephanta Island",
            "categories": ["historical", "cultural", "spiritual"]
        }
    ],
    "goa": [
        {
            "name": "Beach Hopping Tour",
            "type": "beach",
            "duration": 8,
            "cost": {"budget": 1070, "mid": 1950, "luxury": 3300},
            "rating": 4.6,
            "description": "Visit multiple beaches from Baga to Anjuna",
            "best_time": "morning",
            "location": "North Goa",
            "categories": ["beach", "adventure"]
        },
        {
            "name": "Spice Plantation Tour",
            "type": "nature",
            "duration": 4,
            "cost": {"budget": 640, "mid": 1080, "luxury": 1650},
            "rating": 4.3,
            "description": "Explore organic spice farms with traditional lunch",
            "best_time": "morning",
            "location": "Ponda",
            "categories": ["nature", "culinary"]
        },
        {
            "name": "Old Goa Churches Tour",
            "type": "historical",
            "duration": 3,
            "cost": {"budget": 220, "mid": 430, "luxury": 880},
            "rating": 4.4,
            "description": "UNESCO World Heritage Portuguese churches",
            "best_time": "morning",
            "location": "Old Goa",
            "categories": ["historical", "cultural"]
        },
        {
            "name": "Sunset Cruise",
            "type": "adventure",
            "duration": 3,
            "cost": {"budget": 860, "mid": 1300, "luxury": 2200},
            "rating": 4.7,
            "description": "Romantic sunset cruise on Mandovi River",
            "best_time": "evening",
            "location": "Panaji",
            "categories": ["adventure", "relaxation"]
        },
        {
            "name": "Dudhsagar Waterfalls Trek",
            "type": "adventure",
            "duration": 8,
            "cost": {"budget": 1280, "mid": 2160, "luxury": 3300},
            "rating": 4.8,
            "description": "Trek to India's fourth-highest waterfalls",
            "best_time": "morning",
            "location": "Mollem National Park",
            "categories": ["adventure", "nature"]
        }
    ],
    "rajasthan": [
        {
            "name": "Amber Fort & Palace",
            "type": "historical",
            "duration": 4,
            "cost": {"budget": 220, "mid": 430, "luxury": 880},
            "rating": 4.8,
            "description": "Magnificent hilltop fort with elephant rides",
            "best_time": "morning",
            "location": "Amer",
            "categories": ["historical", "cultural", "adventure"]
        },
        {
            "name": "City Palace Jaipur",
            "type": "cultural",
            "duration": 3,
            "cost": {"budget": 165, "mid": 320, "luxury": 660},
            "rating": 4.6,
            "description": "Royal palace complex with museums and courtyards",
            "best_time": "morning",
            "location": "City Palace",
            "categories": ["cultural", "historical"]
        },
        {
            "name": "Desert Safari Pushkar",
            "type": "adventure",
            "duration": 6,
            "cost": {"budget": 1605, "mid": 2700, "luxury": 4400},
            "rating": 4.7,
            "description": "Camel safari with desert camping experience",
            "best_time": "evening",
            "location": "Pushkar",
            "categories": ["adventure", "nature"]
        },
        {
            "name": "Rajasthani Folk Dance Show",
            "type": "cultural",
            "duration": 2,
            "cost": {"budget": 320, "mid": 540, "luxury": 1100},
            "rating": 4.5,
            "description": "Traditional Rajasthani music and dance performance",
            "best_time": "evening",
            "location": "Chokhi Dhani",
            "categories": ["cultural", "entertainment"]
        },
        {
            "name": "Hawa Mahal Photography Tour",
            "type": "sightseeing",
            "duration": 2,
            "cost": {"budget": 110, "mid": 220, "luxury": 440},
            "rating": 4.4,
            "description": "Iconic Palace of Winds with unique architecture",
            "best_time": "morning",
            "location": "Hawa Mahal",
            "categories": ["historical", "architecture", "sightseeing"]
        }
    ],
    "kerala": [
        {
            "name": "Backwater Houseboat Cruise",
            "type": "nature",
            "duration": 8,
            "cost": {"budget": 2140, "mid": 3780, "luxury": 6600},
            "rating": 4.8,
            "description": "Overnight cruise through Kerala's famous backwaters",
            "best_time": "morning",
            "location": "Alleppey",
            "categories": ["nature", "relaxation"]
        },
        {
            "name": "Tea Plantation Tour Munnar",
            "type": "nature",
            "duration": 4,
            "cost": {"budget": 535, "mid": 860, "luxury": 1320},
            "rating": 4.6,
            "description": "Explore lush tea gardens with tasting sessions",
            "best_time": "morning",
            "location": "Munnar",
            "categories": ["nature", "educational"]
        },
        {
            "name": "Ayurvedic Spa Treatment",
            "type": "wellness",
            "duration": 3,
            "cost": {"budget": 1070, "mid": 2160, "luxury": 4400},
            "rating": 4.7,
            "description": "Traditional Ayurvedic massage and treatments",
            "best_time": "afternoon",
            "location": "Kumarakom",
            "categories": ["wellness", "cultural"]
        },
        {
            "name": "Kathakali Dance Performance",
            "type": "cultural",
            "duration": 2,
            "cost": {"budget": 220, "mid": 430, "luxury": 880},
            "rating": 4.5,
            "description": "Classical Kerala dance drama performance",
            "best_time": "evening",
            "location": "Kochi",
            "categories": ["cultural", "entertainment"]
        },
        {
            "name": "Periyar Wildlife Safari",
            "type": "nature",
            "duration": 4,
            "cost": {"budget": 430, "mid": 750, "luxury": 1320},
            "rating": 4.4,
            "description": "Wildlife spotting in Periyar National Park",
            "best_time": "morning",
            "location": "Thekkady",
            "categories": ["nature", "wildlife", "adventure"]
        }
    ],
    "himachal": [
        {
            "name": "Rohtang Pass Adventure",
            "type": "adventure",
            "duration": 8,
            "cost": {"budget": 1284, "mid": 2160, "luxury": 3850},
            "rating": 4.6,
            "description": "High-altitude mountain pass with snow activities",
            "best_time": "morning",
            "location": "Manali",
            "categories": ["adventure", "mountain"]
        },
        {
            "name": "Paragliding in Bir Billing",
            "type": "adventure",
            "duration": 4,
            "cost": {"budget": 2140, "mid": 3240, "luxury": 5500},
            "rating": 4.8,
            "description": "World-class paragliding with Himalayan views",
            "best_time": "morning",
            "location": "Bir Billing",
            "categories": ["adventure", "sports"]
        },
        {
            "name": "Shimla Heritage Walk",
            "type": "cultural",
            "duration": 3,
            "cost": {"budget": 320, "mid": 540, "luxury": 880},
            "rating": 4.3,
            "description": "Colonial architecture tour on Mall Road",
            "best_time": "morning",
            "location": "Shimla",
            "categories": ["cultural", "historical"]
        },
        {
            "name": "Trekking in Kasol",
            "type": "adventure",
            "duration": 6,
            "cost": {"budget": 860, "mid": 1620, "luxury": 2750},
            "rating": 4.7,
            "description": "Scenic trek through Parvati Valley",
            "best_time": "morning",
            "location": "Kasol",
            "categories": ["adventure", "nature"]
        },
        {
            "name": "Toy Train Ride Shimla",
            "type": "sightseeing",
            "duration": 5,
            "cost": {"budget": 640, "mid": 1080, "luxury": 1760},
            "rating": 4.5,
            "description": "UNESCO World Heritage mountain railway experience",
            "best_time": "morning",
            "location": "Shimla",
            "categories": ["cultural", "heritage", "sightseeing"]
        }
    ],
    "ladakh": [
        {
            "name": "Pangong Lake Expedition",
            "type": "adventure",
            "duration": 12,
            "cost": {"budget": 3210, "mid": 5400, "luxury": 8800},
            "rating": 4.9,
            "description": "Journey to the pristine high-altitude lake",
            "best_time": "morning",
            "location": "Pangong Tso",
            "categories": ["adventure", "nature", "photography"]
        },
        {
            "name": "Nubra Valley Desert Safari",
            "type": "adventure",
            "duration": 10,
            "cost": {"budget": 2675, "mid": 4320, "luxury": 7150},
            "rating": 4.8,
            "description": "Double-humped camel ride in high-altitude desert",
            "best_time": "morning",
            "location": "Nubra Valley",
            "categories": ["adventure", "cultural", "nature"]
        },
        {
            "name": "Monastery Circuit Tour",
            "type": "cultural",
            "duration": 6,
            "cost": {"budget": 1070, "mid": 1940, "luxury": 3300},
            "rating": 4.7,
            "description": "Visit ancient Buddhist monasteries and gompas",
            "best_time": "morning",
            "location": "Leh",
            "categories": ["cultural", "spiritual", "historical"]
        },
        {
            "name": "Leh Palace Heritage Walk",
            "type": "historical",
            "duration": 3,
            "cost": {"budget": 320, "mid": 540, "luxury": 880},
            "rating": 4.4,
            "description": "Explore the ruins of the former royal palace",
            "best_time": "afternoon",
            "location": "Leh",
            "categories": ["historical", "cultural", "architecture"]
        },
        {
            "name": "Khardung La Pass Adventure",
            "type": "adventure",
            "duration": 8,
            "cost": {"budget": 2140, "mid": 3780, "luxury": 6050},
            "rating": 4.6,
            "description": "World's highest motorable road pass experience",
            "best_time": "morning",
            "location": "Khardung La",
            "categories": ["adventure", "mountain", "photography"]
        }
    ],
    "andaman": [
        {
            "name": "Scuba Diving at Havelock",
            "type": "adventure",
            "duration": 4,
            "cost": {"budget": 3210, "mid": 5400, "luxury": 8800},
            "rating": 4.8,
            "description": "Explore vibrant coral reefs and marine life",
            "best_time": "morning",
            "location": "Havelock Island",
            "categories": ["adventure", "nature", "marine"]
        },
        {
            "name": "Radhanagar Beach Sunset",
            "type": "relaxation",
            "duration": 3,
            "cost": {"budget": 220, "mid": 430, "luxury": 880},
            "rating": 4.9,
            "description": "Asia's best beach with pristine white sand",
            "best_time": "evening",
            "location": "Havelock Island",
            "categories": ["beach", "relaxation", "photography"]
        },
        {
            "name": "Cellular Jail Sound & Light Show",
            "type": "historical",
            "duration": 2,
            "cost": {"budget": 160, "mid": 320, "luxury": 640},
            "rating": 4.5,
            "description": "Historic prison's story through multimedia show",
            "best_time": "evening",
            "location": "Port Blair",
            "categories": ["historical", "educational", "cultural"]
        },
        {
            "name": "Sea Walking at North Bay",
            "type": "adventure",
            "duration": 2,
            "cost": {"budget": 2140, "mid": 3240, "luxury": 5500},
            "rating": 4.6,
            "description": "Walk underwater with special helmet breathing system",
            "best_time": "morning",
            "location": "North Bay Island",
            "categories": ["adventure", "marine", "unique"]
        },
        {
            "name": "Mangrove Creek Safari",
            "type": "nature",
            "duration": 4,
            "cost": {"budget": 860, "mid": 1620, "luxury": 2750},
            "rating": 4.4,
            "description": "Boat safari through mangrove forests and creeks",
            "best_time": "morning",
            "location": "Baratang Island",
            "categories": ["nature", "wildlife", "boat safari"]
        }
    ]
}

# User preference templates (Updated for 2025 trends)
USER_PREFERENCE_TEMPLATES = [
    {
        "profile_type": "adventure_seeker",
        "interests": ["adventure", "nature", "sports"],
        "budget_preference": "mid",
        "accommodation_type": "mid",
        "activity_intensity": "high",
        "group_size_preference": "small"
    },
    {
        "profile_type": "culture_enthusiast",
        "interests": ["cultural", "historical", "educational"],
        "budget_preference": "mid",
        "accommodation_type": "boutique",
        "activity_intensity": "medium",
        "group_size_preference": "any"
    },
    {
        "profile_type": "luxury_traveler",
        "interests": ["luxury", "culinary", "wellness"],
        "budget_preference": "luxury",
        "accommodation_type": "luxury",
        "activity_intensity": "low",
        "group_size_preference": "private"
    },
    {
        "profile_type": "budget_backpacker",
        "interests": ["cultural", "nature", "adventure"],
        "budget_preference": "budget",
        "accommodation_type": "budget",
        "activity_intensity": "high",
        "group_size_preference": "large"
    },
    {
        "profile_type": "wellness_seeker",
        "interests": ["wellness", "spiritual", "nature", "relaxation"],
        "budget_preference": "mid",
        "accommodation_type": "wellness",
        "activity_intensity": "low",
        "group_size_preference": "small"
    },
    {
        "profile_type": "family_explorer",
        "interests": ["cultural", "nature", "educational", "relaxation"],
        "budget_preference": "mid",
        "accommodation_type": "family",
        "activity_intensity": "medium",
        "group_size_preference": "family"
    }
]

def get_destination_data(destination_key: str) -> Dict[str, Any]:
    """Get comprehensive destination data."""
    return DESTINATIONS.get(destination_key.lower(), {})

def get_hotels_for_destination(destination_key: str, budget_type: str = "mid") -> List[Dict[str, Any]]:
    """Get filtered hotels for a destination based on budget."""
    hotels = HOTELS.get(destination_key.lower(), [])
    return [hotel for hotel in hotels if budget_type in hotel["price_per_night"]]

def get_activities_for_destination(destination_key: str, interests: List[str] = None) -> List[Dict[str, Any]]:
    """Get filtered activities for a destination based on interests."""
    activities = ACTIVITIES.get(destination_key.lower(), [])
    
    if not interests:
        return activities
    
    # Filter activities based on user interests
    filtered_activities = []
    for activity in activities:
        activity_categories = activity.get("categories", [])
        if any(interest in activity_categories for interest in interests):
            filtered_activities.append(activity)
    
    return filtered_activities if filtered_activities else activities

def get_weather_conditions(destination_key: str, travel_month: int) -> Dict[str, Any]:
    """Simulate real-time weather conditions."""
    dest_data = DESTINATIONS.get(destination_key.lower(), {})
    temp_range = dest_data.get("avg_temp_range", {"min": 15, "max": 25})
    best_months = dest_data.get("best_months", [])
    
    # Simulate weather based on month
    is_good_weather = travel_month in best_months
    temp = random.randint(temp_range["min"], temp_range["max"])
    
    conditions = ["sunny", "partly_cloudy", "cloudy", "rainy"]
    weather_condition = random.choice(conditions[:2] if is_good_weather else conditions)
    
    return {
        "temperature": temp,
        "condition": weather_condition,
        "is_favorable": is_good_weather,
        "recommendation": "Great time to visit!" if is_good_weather else "Consider weather conditions"
    }

def calculate_trip_cost(destination_key: str, days: int, travelers: int, budget_type: str) -> Dict[str, float]:
    """Calculate estimated trip cost breakdown."""
    dest_data = DESTINATIONS.get(destination_key.lower(), {})
    daily_budget = dest_data.get("avg_daily_budget", {}).get(budget_type, 100)
    
    hotels = get_hotels_for_destination(destination_key, budget_type)
    avg_hotel_cost = sum(h["price_per_night"][budget_type] for h in hotels) / len(hotels) if hotels else 100
    
    activities = get_activities_for_destination(destination_key)
    avg_activity_cost = sum(a["cost"][budget_type] for a in activities) / len(activities) if activities else 50
    
    # Cost breakdown
    accommodation_cost = avg_hotel_cost * days * travelers
    activity_cost = avg_activity_cost * 2 * days * travelers  # Assume 2 activities per day
    food_cost = (daily_budget * 0.4) * days * travelers  # 40% of daily budget for food
    transport_cost = (daily_budget * 0.2) * days * travelers  # 20% for local transport
    
    total_cost = accommodation_cost + activity_cost + food_cost + transport_cost
    
    return {
        "accommodation": accommodation_cost,
        "activities": activity_cost,
        "food": food_cost,
        "transport": transport_cost,
        "total": total_cost,
        "per_person": total_cost / travelers,
        "per_day": total_cost / days
    }
