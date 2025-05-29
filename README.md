# 🕌 Prayer Times - Alfred Workflow

An elegant and comprehensive Alfred workflow that displays Islamic prayer times in real-time with support for multiple calculation methods, schools of jurisprudence, and location detection options.

![SCR 2025-05-29 at 14 55 55](https://github.com/user-attachments/assets/fe9d7e0c-ab9f-47b5-91bd-6ed4e2d6eb8d)


## ✨ Features

- **Real-time Prayer Times**: Fetches current prayer times from the internet
- **Multiple Location Methods**: Auto-detect via IP, manual address, or city/country
- **24 Calculation Methods**: Support for various Islamic authorities worldwide
- **School of Jurisprudence**: Choose between Shafi (Standard) and Hanafi schools
- **Comprehensive Prayer List**: Imsak, Fajr, Sunrise, Dhuhr, Asr, Sunset, Maghrib, Isha, Midnight, and Night Thirds
- **Hijri Calendar**: Displays Islamic date alongside Gregorian date
- **Next Prayer Countdown**: Shows remaining time until the next prayer
- **Flexible Time Formats**: 12-hour (AM/PM) or 24-hour format
- **Large Type Display**: Press ⌘+Enter for large prayer time display
- **Copy to Clipboard**: Press ⌘+C to copy prayer times
- **High Latitude Support**: Special adjustments for northern regions

## 🚀 Installation

### Prerequisites

**Install Node.js** via [Homebrew](https://formulae.brew.sh/formula/node) (recommended):
   ```bash
   brew install node
   ```

### Install Workflow

1. Download the latest release from the [Releases](https://github.com/abdullahahmed-dev/prayer-times/releases) page
2. Double-click the `.alfredworkflow` file to install
3. Alfred will automatically import the workflow

## ⚙️ Configuration

<img src="https://github.com/user-attachments/assets/8cd9677d-3564-4dbc-8ba5-77b832300c7c" width="400" alt="Configuration Interface">

After installation, configure the workflow by opening Alfred Preferences → Workflows → Prayer Times:

- **Auto-Detect Location**: Uses IP geolocation (not recommended for accuracy)
- **Manual Address**: Enter full address (e.g., "Times Square, New York, NY, USA")
- **City**: City name for prayer time calculation
- **Country Code**: 2-letter ISO country code (e.g., US, UK, PK)
- **Calculation Method**: Choose from 24 Islamic authorities:
    - University of Islamic Sciences, Karachi (Default)
    - Islamic Society of North America
    - Muslim World League
    - Umm Al-Qura University, Makkah
    - Egyptian General Authority of Survey
    - And 19 more regional authorities
- **School of Jurisprudence**:
    - **Shafi (Standard)**: Earlier Asr time
    - **Hanafi**: Later Asr time
- **Midnight Mode**: Standard, Jafari, or Auto
- **High Latitude Adjustment**: For regions like UK, Sweden, etc.
- **Time Format**: 12-hour (AM/PM) or 24-hour

## 🎯 Usage

1. **Trigger the workflow**: Type `prayer` in Alfred (or your custom keyword)
2. **View prayer times**: See all daily prayer times with the next prayer highlighted
3. **Copy prayer time**: Select any prayer and press Enter or ⌘+C
4. **Large display**: Select any prayer and press ⌘+Enter for large type view

## 🛠️ Technical Details

- **API**: Uses the reliable [Al-Adhan Prayer Times API](https://aladhan.com/prayer-times-api)
- **Location Detection**: IP-based geolocation with manual override options
- **Error Handling**: Graceful fallbacks for network issues and invalid locations
- **Performance**: Lightweight with minimal system impact
- **Compatibility**: Works with all modern Alfred versions on macOS

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📋 Requirements

- macOS 10.12 or later
- Alfred 4+ with Powerpack
- Node.js (install via [Homebrew](https://formulae.brew.sh/formula/node))
- Internet connection for fetching prayer times

## 🐛 Troubleshooting

### Common Issues

- **No prayer times displayed**: Check your internet connection and location settings
- **Incorrect times**: Verify your calculation method and school of jurisprudence
- **Location not found**: Try using a more specific address or enable auto-detection

### Getting Help

If you encounter any issues:

1. Check the [Issues](https://github.com/abdullahahmed-dev/prayer-times/issues) page
2. Create a new issue with detailed information about the problem
3. Include your configuration settings and error messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://claude.ai/chat/LICENSE) file for details.

## 🙏 Credits

- **[Al-Adhan API](https://aladhan.com/prayer-times-api#get-/timingsByAddress/-date-)** - Reliable Islamic prayer times API
- **[Alfy](https://github.com/sindresorhus/alfy)** by Sindre Sorhus - Simplified Alfred workflow creation
- **[Freepik](https://www.freepik.com/)** for providing workflow icon
- **Islamic Authorities** - For providing accurate prayer time calculation methods

## 📞 Support

If you find this workflow useful, please consider:

- ⭐ Starring this repository
- 🐛 Reporting bugs or suggesting features
- 🤝 Contributing to the codebase

---

**Author**: Abdullah Ahmed  
**Repository**: https://github.com/abdullahahmed-dev/prayer-times  

_May this workflow help you in maintaining your daily prayers. Ameen._
