---
name: travel-planner
description: Comprehensive travel planning skill that creates complete travel guides with itinerary planning, hotel/food recommendations, weather info, and multi-format output (Word/MD/Web). Use when users want to plan a trip, get travel recommendations, or generate travel guide documents.
---

# Travel Planner Skill

## Overview

Creates comprehensive, personalized travel guides through interactive dialogue. Collects travel preferences (destination, dates, budget, companions) and generates polished travel documents in multiple formats.

## When to Use

- User wants to plan a trip and needs guidance
- User asks for travel recommendations (hotels, restaurants, attractions)
- User needs a complete travel itinerary document
- User wants weather info, route planning, or budget calculations
- Keywords: travel, trip, vacation, hotel, itinerary, 攻略, 旅游, 酒店, 行程

## Interactive Data Collection

When user initiates travel planning, guide them through these categories:

| Category | Key Information to Collect |
|----------|---------------------------|
| **Destination** | City/region, specific attractions |
| **Dates** | Start/end, travel duration, season considerations |
| **Companions** | Solo, couple, family (children age), friends, group |
| **Budget** | Total budget, breakdown (accommodation, food, transport, activities) |
| **Preferences** | Interests (culture, nature, food, shopping), pace (relaxed vs packed) |
| **Transportation** | Flight, train, driving, local transport preferences |
| **Special Needs** | Dietary restrictions, accessibility, language |

## Information Sufficiency Check

**If user provides minimal info** (e.g., "plan a trip"):
- Ask clarifying questions proactively
- Suggest popular destinations based on season
- Provide a template for what information helps

**If user provides sufficient info**:
- Confirm key details before generating
- Offer to start with a draft and refine

## Workflow

### Step 1: Collect Information
Use natural dialogue to gather all necessary details. Reference [travel_template.md](references/travel_template.md) for required fields.

### Step 2: Generate Content
After data collection, use scripts to create output:
- `generate_word.py` - Word document (.docx)
- `generate_markdown.py` - Markdown file (.md)
- `generate_web.py` - Interactive HTML page

### Step 3: Output Selection
Let user choose format or generate all. Default: Word document.

## API Configuration

For full functionality, configure these APIs. Missing keys will prompt user input.

### Required: API Keys

| Service | Purpose | How to Get |
|---------|---------|------------|
| **高德地图** | POI search, route planning, geocoding | https://lbs.amap.com/api |
| **天气API** | Weather forecasts | https://lbs.amap.com/api/weather |

### Optional: API Keys

| Service | Purpose |
|---------|---------|
| OpenRouteService | Alternative routing |
| Amadeus | Flight booking info |

See [api_config.md](references/api_config.md) for setup instructions.

## Output Formats

### Word Document (Default)
- Professional travel guide layout
- Includes: cover, itinerary timeline, hotel info, budget breakdown
- File: `travel_guide_[destination]_[date].docx`

### Markdown
- Portable, editable format
- Includes: all sections with markdown formatting
- File: `travel_guide_[destination]_[date].md`

### Web Page (Interactive)
- Rich visuals: maps, charts, timeline animations
- Responsive design for mobile/desktop
- File: `travel_guide_[destination].html`

## Resources

### scripts/
- `generate_word.py` - Generate Word documents
- `generate_markdown.py` - Generate Markdown files
- `generate_web.py` - Generate interactive HTML pages
- `api_config.py` - Manage API configuration
- `weather_service.py` - Fetch weather data

### references/
- `api_config.md` - API setup guide
- `travel_template.md` - Travel guide content template
- `format_specs.md` - Output format specifications

### assets/
- `web_template/` - HTML/CSS/JS templates for web output
- `chart_templates/` - Chart configurations
- `styles/` - CSS styles for all formats
