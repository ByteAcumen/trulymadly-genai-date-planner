import asyncio
import requests
import json


def test_health_check():
    """Test server health endpoint."""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_date_plan(prompt: str):
    """Test date planning endpoint."""
    print(f"\n=== Testing: {prompt} ===")
    try:
        response = requests.post(
            "http://localhost:8000/plan",
            json={"prompt": prompt},
            timeout=30
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nTitle: {data['title']}")
            print(f"City: {data['city']}")
            print(f"Weather: {data['weather']['temperature']}°C, {data['weather']['condition']}")
            print(f"\nRecommendations:")
            for place in data['recommendations'][:2]:
                print(f"  - {place['name']} ({place['category']})")
            print(f"\nItinerary: {data['itinerary'][:200]}...")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Run test suite."""
    print("TrulyMadly GenAI Date Planner - Test Suite")
    print("=" * 50)
    
    test_prompts = [
        "Plan a romantic dinner in Mumbai this Saturday",
        "Suggest a fun date in Bangalore within ₹2000",
        "Cozy coffee date in Delhi today"
    ]
    
    if not test_health_check():
        print("\n❌ Server is not running!")
        print("Start it with: uvicorn main:app")
        return
    
    print("\n✅ Server is healthy!")
    
    for prompt in test_prompts:
        success = test_date_plan(prompt)
        if not success:
            print(f"❌ Test failed for: {prompt}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")


if __name__ == "__main__":
    main()
