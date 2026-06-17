from mcp.server.fastmcp import FastMCP
mcp = FastMCP("unit_converter")
@mcp.tool()
def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (c * 9/5) + 32
@mcp.tool()
def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5/9
@mcp.tool()
def km_to_miles(km: float) -> float:
    """Convert kilometers to miles."""
    return km * 0.621371
@mcp.tool()
def miles_to_km(miles: float) -> float:
    """Convert miles to kilometers."""
    return miles / 0.621371
if __name__ == "__main__":
    mcp.run()
