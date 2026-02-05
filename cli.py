#!/usr/bin/env python3
"""
CLI Interface for TrulyMadly GenAI Date Planner
Run directly from command line without starting the server.
"""

import asyncio
import json
import sys
from dotenv import load_dotenv
from agents import PlannerAgent, ExecutorAgent, VerifierAgent


async def plan_date(prompt: str):
    """Execute date planning flow via CLI."""
    print("\n🎯 TrulyMadly GenAI Date Planner")
    print("=" * 50)
    print(f"\n📝 Prompt: {prompt}\n")
    
    try:
        # Initialize agents
        print("🤖 Initializing AI agents...")
        planner = PlannerAgent()
        executor = ExecutorAgent()
        verifier = VerifierAgent()
        
        # Step 1: Plan
        print("📊 Planner Agent analyzing request...")
        plan_output = await planner.analyze(prompt)
        print(f"   ✓ Extracted: {plan_output.city}, {plan_output.vibe} vibe")
        
        # Step 2: Execute
        print("🔧 Executor Agent calling APIs...")
        execution_data = await executor.execute(plan_output)
        print(f"   ✓ Weather: {execution_data['weather'].temperature}°C")
        print(f"   ✓ Found {len(execution_data['places'])} venues")
        
        # Step 3: Verify
        print("✅ Verifier Agent generating final plan...")
        final_plan = await verifier.verify(execution_data)
        
        # Display results
        print("\n" + "=" * 50)
        print(f"🎉 {final_plan.title}")
        print("=" * 50)
        print(f"\n📍 City: {final_plan.city}")
        print(f"🌤️  Weather: {final_plan.weather.temperature}°C, {final_plan.weather.condition}")
        
        print(f"\n🏨 Top Recommendations:")
        for i, place in enumerate(final_plan.recommendations, 1):
            print(f"   {i}. {place.name} ({place.category})")
            print(f"      📍 {place.address}")
            if place.rating:
                print(f"      ⭐ {place.rating}/10")
        
        print(f"\n📅 Itinerary:")
        print(f"   {final_plan.itinerary}")
        
        if final_plan.budget_estimate:
            print(f"\n💰 Budget: ₹{final_plan.budget_estimate}")
        
        if final_plan.tips:
            print(f"\n💡 Tips:")
            for tip in final_plan.tips:
                print(f"   • {tip}")
        
        print("\n" + "=" * 50)
        print("✨ Date plan generated successfully!")
        print("=" * 50 + "\n")
        
        return final_plan
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def main():
    """CLI entry point."""
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Usage: python cli.py \"<your date planning request>\"")
        print("\nExamples:")
        print('  python cli.py "Plan a romantic dinner in Mumbai"')
        print('  python cli.py "Suggest a fun date in Bangalore within ₹2000"')
        print('  python cli.py "Cozy coffee date in Delhi"')
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    asyncio.run(plan_date(prompt))


if __name__ == "__main__":
    main()
