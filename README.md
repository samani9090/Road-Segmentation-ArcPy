# Road-Segmentation-ArcPy
Python tool for splitting road networks into equal segments using ArcPy and UTM projection
# 🛣️ Road Segmentation with ArcPy

![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![ArcGIS](https://img.shields.io/badge/ArcGIS%20Pro-Required-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

A professional Python tool for automated road network segmentation using ArcPy. Converts WGS84 geographic coordinates to UTM projection and splits roads into equal-length segments for transportation analysis.

## 🌟 Features

- **Automatic Coordinate Conversion**: WGS84 → UTM Zone 39N (for Iran/Central Asia)
- **Configurable Segmentation**: Split roads into 1km, 2km, or any custom length
- **Intelligent Processing**: Handles both short and long road segments appropriately
- **Metadata Preservation**: Maintains original attributes while adding segment information
- **Production Ready**: Includes logging, error handling, and progress tracking

## 📊 Real-World Application

**Problem**: Road networks in WGS84 have lengths in degrees, not kilometers  
**Solution**: This tool automatically converts to metric system and splits for micro-analysis

**Example Input**: 99 road segments in WGS84 (appearing as 0.5-0.9° length)  
**Actual Length**: 10-100 kilometers per road  
**Output**: 247 segments of exactly 2km each  
**Processing Time**: 3.2 seconds

## 🚀 Quick Start

### Prerequisites
- ArcGIS Pro (for ArcPy functionality)
- Python 3.8+
- Basic understanding of GIS concepts

### Installation
```bash
git clone https://github.com/samani9090/Road-Segmentation-ArcPy.git
cd Road-Segmentation-ArcPy
