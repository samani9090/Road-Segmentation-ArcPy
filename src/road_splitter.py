"""
Road Segmentation Tool - ArcPy Implementation
Author: [Your Name]
Description: Convert WGS84 roads to UTM and split into equal segments
"""

import arcpy
import os
import time
import logging
from typing import Optional, Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RoadSegmenter:
    """Main class for road segmentation"""
    
    UTM_ZONE_39N = """PROJCS["WGS_1984_UTM_Zone_39N",
        GEOGCS["GCS_WGS_1984",
            DATUM["D_WGS_1984",
                SPHEROID["WGS_1984",6378137.0,298.257223563]],
            PRIMEM["Greenwich",0.0],
            UNIT["Degree",0.0174532925199433]],
        PROJECTION["Transverse_Mercator"],
        PARAMETER["False_Easting",500000.0],
        PARAMETER["False_Northing",0.0],
        PARAMETER["Central_Meridian",51.0],
        PARAMETER["Scale_Factor",0.9996],
        PARAMETER["Latitude_Of_Origin",0.0],
        UNIT["Meter",1.0]]"""
    
    def __init__(self, workspace: Optional[str] = None):
        if workspace:
            arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        logger.info("RoadSegmenter initialized")
    
    def split_roads(self, input_fc: str, output_name: str, 
                   segment_length_km: float = 2.0) -> Dict:
        """Main splitting function"""
        
        logger.info(f"Starting: {input_fc} → {segment_length_km}km segments")
        
        try:
            # 1. Validate
            if not arcpy.Exists(input_fc):
                return {"success": False, "error": "Input not found"}
            
            # 2. Project to UTM
            projected = self._project_to_utm(input_fc)
            
            # 3. Create output
            output_fc = os.path.join(arcpy.env.workspace, output_name)
            self._create_output(projected, output_fc)
            
            # 4. Split
            results = self._perform_split(projected, output_fc, segment_length_km)
            
            # 5. Cleanup
            if arcpy.Exists(projected):
                arcpy.Delete_management(projected)
            
            return {
                "success": True,
                "output": output_fc,
                "segments": results["segments"],
                "time": results["time"]
            }
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _project_to_utm(self, input_fc: str) -> str:
        """Project to UTM Zone 39N"""
        projected = f"{input_fc}_UTM"
        
        if arcpy.Exists(projected):
            arcpy.Delete_management(projected)
        
        try:
            arcpy.Project_management(input_fc, projected, self.UTM_ZONE_39N)
        except:
            # Fallback
            arcpy.CopyFeatures_management(input_fc, projected)
            arcpy.DefineProjection_management(projected, self.UTM_ZONE_39N)
        
        return projected
    
    def _create_output(self, template_fc: str, output_fc: str):
        """Create output feature class"""
        if arcpy.Exists(output_fc):
            arcpy.Delete_management(output_fc)
        
        arcpy.CreateFeatureclass_management(
            os.path.dirname(output_fc),
            os.path.basename(output_fc),
            "POLYLINE",
            template=template_fc
        )
        
        # Add fields
        fields = [
            ("SEGMENT_ID", "LONG", "Segment Number"),
            ("ROAD_ID", "LONG", "Original Road ID"),
            ("LENGTH_KM", "DOUBLE", "Length in Kilometers"),
            ("LABEL", "TEXT", "Segment Label", 50)
        ]
        
        for field in fields:
            if len(field) == 3:
                arcpy.AddField_management(output_fc, field[0], field[1], field_alias=field[2])
            else:
                arcpy.AddField_management(output_fc, field[0], field[1], 
                                         field_length=field[3], field_alias=field[2])
    
    def _perform_split(self, input_fc: str, output_fc: str, 
                      segment_length_km: float) -> Dict:
        """Perform the actual splitting"""
        segment_m = segment_length_km * 1000
        start = time.time()
        total_segments = 0
        road_id = 1
        
        with arcpy.da.SearchCursor(input_fc, ["OID@", "SHAPE@"]) as s_cursor, \
             arcpy.da.InsertCursor(output_fc, ["SHAPE@", "SEGMENT_ID", "ROAD_ID", 
                                             "LENGTH_KM", "LABEL"]) as i_cursor:
            
            for oid, geom in s_cursor:
                if not geom:
                    continue
                
                if geom.length <= segment_m:
                    # Single segment
                    i_cursor.insertRow([
                        geom, 1, road_id, geom.length/1000, f"R{road_id}_S01"
                    ])
                    total_segments += 1
                else:
                    # Multiple segments
                    cumulative = 0
                    seg_num = 1
                    
                    while cumulative < geom.length:
                        start_ratio = cumulative / geom.length
                        end_ratio = min((cumulative + segment_m) / geom.length, 1.0)
                        
                        segment = geom.segmentAlongLine(start_ratio, end_ratio, False)
                        i_cursor.insertRow([
                            segment, seg_num, road_id, 
                            segment.length/1000, f"R{road_id}_S{seg_num:02d}"
                        ])
                        
                        cumulative += segment.length
                        seg_num += 1
                        total_segments += 1
                
                road_id += 1
        
        return {
            "segments": total_segments,
            "time": time.time() - start
        }

# Simple interface
def split_roads_simple(input_fc: str, output_name: str, 
                      segment_length_km: float = 2.0) -> str:
    """
    Simple interface for road segmentation
    
    Example:
        result = split_roads_simple("roads.shp", "segments_2km", 2.0)
    """
    segmenter = RoadSegmenter()
    result = segmenter.split_roads(input_fc, output_name, segment_length_km)
    
    if result["success"]:
        print(f"✅ Success! Created {result['segments']} segments in {result['time']:.1f}s")
        return result["output"]
    else:
        print(f"❌ Error: {result['error']}")
        return None

if __name__ == "__main__":
    # Example usage
    output = split_roads_simple(
        input_fc="roadlinkdin",
        output_name="RoadSegments_2km",
        segment_length_km=2.0
    )
    
    if output:
        print(f"Output: {output}")
