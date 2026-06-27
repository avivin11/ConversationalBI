"""
test_groq.py — Verify Groq API Connection
==========================================
Run this after setting up your .env file to confirm the LLM is working.

USAGE:
  python test_groq.py

EXPECTED OUTPUT:
  ✅ Groq API is working.
  Response: Groq is working. Your RAG BI Assistant is ready to build.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in environment.")
    print("   Steps to fix:")
    print("   1. Make sure .env file exists in this folder")
    print("   2. Open .env and set: GROQ_API_KEY=your_key_here")
    print("   3. Get a free key at: https://console.groq.com → API Keys")
    sys.exit(1)

print("🔑 API key found. Testing connection to Groq...")

try:
    llm = ChatGroq(
        api_key=api_key,
        model="llama3-70b-8192",
        temperature=0.0,
    )

    response = llm.invoke("Say exactly this: 'Groq is working. Your RAG BI Assistant is ready to build.'")

    print(f"\n✅ Groq API is working.")
    print(f"Response: {response.content}")
    print(f"\n🚀 Phase 0 complete. You're ready for Phase 1.")

except Exception as e:
    print(f"\n❌ Groq API call failed: {e}")
    print("\nCommon causes:")
    print("  - Invalid API key (copy it again from console.groq.com)")
    print("  - No internet connection")
    print("  - Groq rate limit (wait 1 minute and retry)")