# Bitstronauts


CurioCity: The AI Knowledge Alchemist
"Don't just consume information; fuel your innovation."

CurioCity is an AI-powered educational ecosystem that transforms passive content consumption into active, gamified innovation.

Built by Team Bitstronauts, it leverages Google Gemini 1.5 Flash to solve two critical modern education problems:

Information Overload

Passive Learning

CurioCity acts as a Cognitive Filter, converting YouTube lectures and dense PDFs into structured “Wisdom Scrolls.”

Table of Contents

Executive Summary

System Architecture

Module Breakdown

6 Pillars of Innovation

Correctness & Verification

Technical Stack

Installation & Deployment

1. Executive Summary

Modern education suffers from Digital Noise — infinite scrolling, shallow learning, and low retention.

CurioCity solves this by:

Converting long-form content into structured summaries

Applying metaphor-based learning

Creating mnemonic anchors

Encouraging conceptual invention over rote memorization

Goal: Shift dopamine reward from content consumption to conceptual mastery.

2. System Architecture

CurioCity follows a Decoupled Tiered Architecture ensuring:

High cohesion

Low coupling

Scalability

Maintainability

Architectural Layers
Logic Layer (The Brain)

Implemented in utils.py
Handles AI processing and data transformation

Orchestration Layer (The Interface)

Implemented in curiocityapp.py
Manages session state and user interactions

Presentation Layer (The Identity)

Implemented in styles.css
Controls UI aesthetics and branding

3. Detailed Module Analysis
A. The Alchemist Core Engine (utils.py)
Neural Bridge (setup_model)

Implements Self-Healing Model Discovery

Dynamically selects the most efficient Gemini model

Includes failover mechanism for high uptime

Switches to backup models if primary endpoint fails

Media Ingestors
YouTube Ingestor

Regex-based video ID extraction

Fetches localized transcripts

Cleans unnecessary metadata

PDF Ingestor

Uses PyPDF2 PdfReader

Extracts clean semantic text

Removes formatting noise

Cognitive Transmutation

Uses Zero-Shot Prompt Engineering

Converts raw content into:

Metaphors

“Aha!” insights

Mnemonics

B. The App Orchestrator (curiocityapp.py)
Session State Management

Preserves user profile

Maintains learning history

Supports re-render consistency

The Sage Doubt Solver

Sidebar-based contextual chat

Strictly locked to uploaded material

Prevents AI hallucinations

Asynchronous UI

Uses Streamlit status indicators

Smooth AI generation feedback

Reduced perceived latency

C. Visual Identity (styles.css)
Glassmorphism Design

Semi-transparent containers

High blur effects

Futuristic laboratory aesthetic

Interactive Motion

Gradient buttons

Hover animations

Responsive card transitions

4. The 6 Pillars of Innovation
Phase 1: Knowledge Ingestion (Completed)

The Alchemist Engine

The Sage Solver

Resource Radar (educational link filtering)

Phase 2: Cognitive Engagement (In Progress)
Focus Guard

Gamified Deep Work Timer

Monitors tab switching

Reduces XP on distraction

Fights short-form content addiction

“What If?” Engine

Generates hypothetical scenarios

Tests conceptual understanding

Encourages logical reasoning

Example:
What if gravity were 2x stronger?

Phase 3: Global Accessibility (Future)
Translation Spell

Real-time semantic translation

Supports regional languages such as Hindi and Tamil

Ensures language is not a barrier to conceptual mastery

5. Correctness Properties (Verification)
Property 1: Metaphor Integrity

Every complex concept must include a relatable analogy.

Property 2: Contextual Sandbox

The Sage cannot answer outside provided material.

Property 3: Failover Resilience

Automatic model switching on failure.

Property 4: Search Purity

Filters non-educational domains.

6. Technical Stack
LLM

Google Gemini 1.5 Flash

Backend

Streamlit (Python)

Data Parsing

youtube-transcript-api

PyPDF2

re (Regex)

UI/UX

CSS3 (Flexbox, Glassmorphism)

HTML5

Environment

Python 3.9+

7. Installation & Deployment
Clone Repository
git clone https://github.com/your-username/curiocity.git
cd curiocity
Install Dependencies
pip install -r requirements.txt
Run Application
streamlit run curiocityapp.py
Vision Statement

CurioCity is not just a summarizer.
It is a Cognitive Operating System that:

Filters noise

Encourages invention

Gamifies focus

Reinforces understanding

Scales education globally
