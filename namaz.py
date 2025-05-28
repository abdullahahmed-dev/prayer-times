import requests, sys, json, localizations, os
from datetime import datetime as dt, timezone, timedelta
import time

# Get configuration from Alfred environment variables or command line arguments
placeId = os.environ.get('CITY_CODE') or (sys.argv[1] if len(sys.argv) > 1 else "9541")
langCode = os.environ.get('LANGUAGE') or (sys.argv[2] if len(sys.argv) > 2 else "en")
timeFormat = os.environ.get('TIME_FORMAT', '24').lower()  # '12' or '24' (default)
keyword = os.environ.get('KEYWORD', 'prayer')  # Configurable keyword

try:
    localization = eval("localizations." + langCode)
except:
    # Fallback to English if language not found
    localization = localizations.en

fmt = '%H:%M'
display_fmt = '%I:%M %p' if timeFormat == '12' else '%H:%M'

# Islamic month names mapping for different languages
ISLAMIC_MONTHS = {
    'en': {  # English
        'muharrem': 'Muharram',
        'safer': 'Safar', 
        'rebiulevvel': 'Rabi Al-Awwal',
        'rebiulahir': 'Rabi Al-Thani',
        'cemaziyelevvel': 'Jumada Al-Awwal',
        'cemaziyelahir': 'Jumada Al-Thani',
        'receb': 'Rajab',
        'saban': 'Shaban',
        'ramazan': 'Ramadan',
        'sevval': 'Shawwal',
        'zilkade': 'Dhul Qadah',
        'zilhicce': 'Dhu al-Hijjah'
    },
    'tr': {  # Turkish (keep original)
        'muharrem': 'Muharrem',
        'safer': 'Safer', 
        'rebiulevvel': 'Rebiülevvel',
        'rebiulahir': 'Rebiülahir',
        'cemaziyelevvel': 'Cemaziyelevvel',
        'cemaziyelahir': 'Cemaziyelahir',
        'receb': 'Receb',
        'saban': 'Şaban',
        'ramazan': 'Ramazan',
        'sevval': 'Şevval',
        'zilkade': 'Zilkade',
        'zilhicce': 'Zilhicce'
    },
    'ar': {  # Arabic
        'muharrem': 'محرم',
        'safer': 'صفر', 
        'rebiulevvel': 'ربيع الأول',
        'rebiulahir': 'ربيع الثاني',
        'cemaziyelevvel': 'جمادى الأولى',
        'cemaziyelahir': 'جمادى الثانية',
        'receb': 'رجب',
        'saban': 'شعبان',
        'ramazan': 'رمضان',
        'sevval': 'شوال',
        'zilkade': 'ذو القعدة',
        'zilhicce': 'ذو الحجة'
    }
}

# Flag for displaying remaining time - removed since we now calculate next prayer properly
times = []
items = {'items': []}

def get_islamic_month_localized(turkish_month, language):
    """Convert Turkish Islamic month names to the specified language"""
    # Remove spaces and convert to lowercase for matching
    clean_month = turkish_month.lower().replace(' ', '')
    
    # Get the month mapping for the specified language
    month_mapping = ISLAMIC_MONTHS.get(language, ISLAMIC_MONTHS['en'])
    return month_mapping.get(clean_month, turkish_month)

def format_time_display(time_str):
    """Convert 24hr time to 12hr format if requested"""
    try:
        if timeFormat == '12':
            time_obj = dt.strptime(time_str, '%H:%M')
            return time_obj.strftime('%I:%M %p').lstrip('0')
        return time_str
    except:
        return time_str  # Return original if conversion fails

def format_remaining_time(hours, minutes, language):
    """Format remaining time based on language"""
    if language == 'ar':
        # Arabic formatting
        if hours > 0 and minutes > 0:
            return f"{hours} ساعات و {minutes} دقائق"
        elif hours > 0:
            return f"{hours} ساعات"
        elif minutes > 0:
            return f"{minutes} دقائق"
        else:
            return "أقل من دقيقة"
    elif language == 'tr':
        # Turkish formatting
        if hours > 0 and minutes > 0:
            return f"{hours} saat & {minutes} dakika"
        elif hours > 0:
            return f"{hours} saat"
        elif minutes > 0:
            return f"{minutes} dakika"
        else:
            return "Bir dakikadan az"
    else:
        # English formatting (default)
        if hours > 0 and minutes > 0:
            return f"{hours} hours & {minutes} minutes"
        elif hours > 0:
            return f"{hours} hours"
        elif minutes > 0:
            return f"{minutes} minutes"
        else:
            return "Less than a minute"

def create_error_item(error_msg, subtitle=""):
    """Create an Alfred item for error display"""
    return {
        'items': [{
            'title': f"❌ Prayer Times Error",
            'subtitle': f"{error_msg} | City: {placeId} | Lang: {langCode} | Format: {timeFormat}hr",
            'arg': f"error:{error_msg}",
            'icon': {'path': 'icon.png'}
        }]
    }

def find_todays_data(prayer_data):
    """Find today's prayer times from the API response array"""
    today = dt.now().strftime("%d.%m.%Y")
    
    for day_data in prayer_data:
        if day_data.get("MiladiTarihKisa") == today:
            return day_data
    
    # If today's data not found, return the first entry as fallback
    return prayer_data[0] if prayer_data else None

def getTimes():
    global times
    try:
        # Make API request with timeout
        api_url = f"https://ezanvakti.emushaf.net/vakitler/{placeId}"
        vakit = requests.get(api_url, timeout=15)
        
        # Check if request was successful
        if vakit.status_code != 200:
            raise requests.HTTPError(f"API returned status code {vakit.status_code}")
        
        # Parse JSON response
        response_data = json.loads(vakit.text)
        
        # Check if response has data
        if not response_data or len(response_data) == 0:
            raise ValueError(f"No prayer times found for city code {placeId}")
        
        # Find today's data from the array
        root = find_todays_data(response_data)
        if not root:
            raise ValueError("Could not find today's prayer times in API response")
        
        # Validate required fields exist
        required_fields = ["Imsak", "Gunes", "Ogle", "Ikindi", "Aksam", "Yatsi", "MiladiTarihKisa", "HicriTarihUzun"]
        missing_fields = [field for field in required_fields if field not in root]
        if missing_fields:
            raise KeyError(f"Missing required fields in API response: {', '.join(missing_fields)}")
        
        # Process Islamic date with localized month names
        hijri_date = root["HicriTarihUzun"]
        # Extract day and month from format like "28 Zilkade 1446"
        date_parts = hijri_date.split()
        if len(date_parts) >= 3:
            day = date_parts[0]
            month_turkish = date_parts[1].lower()
            year = date_parts[2]
            month_localized = get_islamic_month_localized(month_turkish, langCode)
            hijri_date_localized = f"{day} {month_localized} {year}"
        else:
            hijri_date_localized = hijri_date
        
        # Build times array with formatted time display
        times = [
            localization.Fajr + ": " + format_time_display(root["Imsak"]),
            localization.Sun + ": " + format_time_display(root["Gunes"]),
            localization.Dhuhr + ": " + format_time_display(root["Ogle"]),
            localization.Asr + ": " + format_time_display(root["Ikindi"]),
            localization.Maghrib + ": " + format_time_display(root["Aksam"]),
            localization.Isha + ": " + format_time_display(root["Yatsi"])
        ]
        
        title = localization.results_for + root["MiladiTarihKisa"] + " / " + hijri_date_localized
        times.insert(0, title)
        return times
        
    except requests.exceptions.Timeout:
        raise Exception("Request timed out - check your internet connection")
    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to prayer times API - check your internet connection")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"API request failed: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Invalid response from API - service may be down")
    except KeyError as e:
        raise Exception(f"API response format changed: {str(e)}")
    except ValueError as e:
        raise Exception(str(e))
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

def calculate_times():
    global times
    try:
        now = dt.now()
        times = getTimes()
        
        # Find the next prayer time
        next_prayer_index = None
        prayer_times_24h = []
        
        # Extract and convert all prayer times to 24h format for comparison
        for i, time in enumerate(times):
            if i == 0:  # Skip the title/date line
                continue
                
            # Extract time from formatted string
            time_part = time.split(": ", 1)[1] if ": " in time else time
            
            # Convert to 24hr format for calculation
            if timeFormat == '12' and ('AM' in time_part or 'PM' in time_part):
                try:
                    clock_time_24h = dt.strptime(time_part, '%I:%M %p').strftime('%H:%M')
                except:
                    clock_time_24h = time_part.replace(' AM', '').replace(' PM', '')
            else:
                clock_time_24h = time_part
            
            prayer_times_24h.append(clock_time_24h)
        
        # Find next prayer
        current_time_str = now.strftime('%H:%M')
        for i, prayer_time_str in enumerate(prayer_times_24h):
            try:
                prayer_time = dt.strptime(prayer_time_str, '%H:%M').replace(year=now.year, month=now.month, day=now.day)
                if prayer_time > now:
                    next_prayer_index = i + 1  # +1 because we skip title at index 0
                    break
            except:
                continue
        
        # If no prayer found for today, next prayer is Fajr tomorrow
        if next_prayer_index is None and len(prayer_times_24h) > 0:
            next_prayer_index = 1  # Fajr is at index 1
            # Calculate time to Fajr tomorrow
            try:
                fajr_today = dt.strptime(prayer_times_24h[0], '%H:%M').replace(year=now.year, month=now.month, day=now.day)
                fajr_tomorrow = fajr_today + timedelta(days=1)
                delta_seconds = int((fajr_tomorrow - now).total_seconds())
            except:
                delta_seconds = None
        else:
            # Calculate time to next prayer today
            try:
                next_prayer_time = dt.strptime(prayer_times_24h[next_prayer_index - 1], '%H:%M').replace(year=now.year, month=now.month, day=now.day)
                delta_seconds = int((next_prayer_time - now).total_seconds())
            except:
                delta_seconds = None
        
        # Build items with remaining time only for next prayer
        for i, time in enumerate(times):
            subtitle = ""
            
            # Show remaining time only for the next prayer
            if i == next_prayer_index and delta_seconds and delta_seconds > 60:
                hours = delta_seconds // 3600
                minutes = (delta_seconds % 3600) // 60
                subtitle = localization.remaining + format_remaining_time(hours, minutes, langCode)
            
            items["items"].append({"title": time, "subtitle": subtitle})
        
        return json.dumps(items, ensure_ascii=False)
        
    except Exception as e:
        # Return error in Alfred-compatible format
        error_response = create_error_item(str(e))
        return json.dumps(error_response, ensure_ascii=False)

# Main execution with comprehensive error handling
try:
    # Always fetch fresh data for accurate remaining time calculation
    times = calculate_times()
    print(times)

except Exception as e:
    # Final fallback - output error as Alfred item
    error_response = create_error_item(f"Critical error: {str(e)}")
    print(json.dumps(error_response, ensure_ascii=False))