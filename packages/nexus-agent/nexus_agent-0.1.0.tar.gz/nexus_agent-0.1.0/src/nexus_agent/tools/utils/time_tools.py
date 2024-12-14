"""Time and date related tools."""

import datetime
import pytz
from typing import Dict, Any, Optional

class TimeTools:
    """A tool for handling time and date operations."""
    
    def __init__(self):
        """Initialize the time tools."""
        pass
    
    async def get_current_time(self, timezone: Optional[str] = None) -> str:
        """
        Get the current time, optionally in a specific timezone.
        
        Args:
            timezone (Optional[str]): Timezone (e.g., 'UTC', 'US/Pacific')
            
        Returns:
            str: Current time in the specified format
        """
        if timezone:
            try:
                tz = pytz.timezone(timezone)
                now = datetime.datetime.now(tz)
            except pytz.exceptions.UnknownTimeZoneError:
                return f"Error: Unknown timezone '{timezone}'"
        else:
            now = datetime.datetime.now()
        
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    async def get_time_difference(self, timezone1: str, timezone2: str) -> str:
        """
        Get the time difference between two timezones.
        
        Args:
            timezone1 (str): First timezone
            timezone2 (str): Second timezone
            
        Returns:
            str: Time difference information
        """
        try:
            tz1 = pytz.timezone(timezone1)
            tz2 = pytz.timezone(timezone2)
            
            now = datetime.datetime.now()
            time1 = now.astimezone(tz1)
            time2 = now.astimezone(tz2)
            
            diff = time2.utcoffset() - time1.utcoffset()
            hours = diff.total_seconds() / 3600
            
            return f"Time difference between {timezone1} and {timezone2} is {hours:+.1f} hours"
            
        except pytz.exceptions.UnknownTimeZoneError as e:
            return f"Error: Unknown timezone - {str(e)}"
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the time tools."""
        return {
            "get_current_time": {
                "description": "Get the current time, optionally in a specific timezone",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": "Optional timezone (e.g., 'UTC', 'US/Pacific')"
                        }
                    }
                }
            },
            "get_time_difference": {
                "description": "Get the time difference between two timezones",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone1": {
                            "type": "string",
                            "description": "First timezone"
                        },
                        "timezone2": {
                            "type": "string",
                            "description": "Second timezone"
                        }
                    },
                    "required": ["timezone1", "timezone2"]
                }
            }
        }
