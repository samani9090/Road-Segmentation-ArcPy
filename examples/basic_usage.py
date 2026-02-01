"""
Example usage of the Road Segmentation Tool
"""

from src.road_splitter import split_roads_simple, RoadSegmenter

def example_1_simple():
    """Simplest usage example"""
    print("Example 1: Simple interface")
    
    result = split_roads_simple(
        input_fc="your_roads.shp",  # Replace with your data
        output_name="road_segments_2km",
        segment_length_km=2.0
    )
    
    return result

def example_2_advanced():
    """Advanced usage with more control"""
    print("Example 2: Advanced interface")
    
    # Initialize with custom workspace
    segmenter = RoadSegmenter(workspace="C:/YourData/Transportation.gdb")
    
    # Split with error handling
    result = segmenter.split_roads(
        input_fc="highway_network",
        output_name="highway_segments_1km",
        segment_length_km=1.0
    )
    
    if result["success"]:
        print(f"Created {result['segments']} segments")
        print(f"Time: {result['time']:.1f} seconds")
        print(f"Output: {result['output']}")
    else:
        print(f"Failed: {result['error']}")
    
    return result

def example_3_multiple_lengths():
    """Example with different segment lengths"""
    print("Example 3: Multiple segment lengths")
    
    segmenter = RoadSegmenter()
    
    # Test different segment lengths
    test_lengths = [0.5, 1.0, 2.0, 5.0]  # kilometers
    
    for length in test_lengths:
        result = segmenter.split_roads(
            input_fc="test_roads.shp",
            output_name=f"segments_{length}km",
            segment_length_km=length
        )
        
        if result["success"]:
            print(f"  {length}km: {result['segments']} segments")

if __name__ == "__main__":
    print("Road Segmentation Tool - Examples")
    print("=" * 50)
    
    # Run examples (commented out for safety)
    # example_1_simple()
    # example_2_advanced()
    # example_3_multiple_lengths()
    
    print("\nTo run examples:")
    print("1. Uncomment the example you want to run")
    print("2. Replace 'your_roads.shp' with your actual data path")
    print("3. Run: python examples/basic_usage.py")
