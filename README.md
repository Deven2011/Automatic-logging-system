# Automated Vehicle Logging System

A production-grade computer vision pipeline that automates vehicle entry/exit logging using real-time license plate recognition. Replaces manual spreadsheet-based systems and unreliable RFID hardware with a fully autonomous solution.

## Overview

This system detects vehicles at facility entry and exit points using ANPR (Automatic Number Plate Recognition), extracts license plate information in real-time, and automatically logs entries into structured reports with end-of-day email notifications.

**Status:** ✅ Deployed and running autonomously in production

---

## Problem Statement

Manual vehicle logging systems suffer from critical inefficiencies:

- **Labor-intensive:** 2+ hours of daily manual data entry
- **Error-prone:** High rates of human data entry mistakes
- **Unreliable:** RFID hardware failures requiring constant maintenance
- **No visibility:** Real-time tracking unavailable
- **Inconsistent:** No standardized data formats or records

This system eliminates these pain points through full automation.

---

## Solution Architecture

### Core Components

```
┌─────────────────┐
│  Dual ANPR      │
│  Cameras        │
│  (Entry/Exit)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Real-time Detection    │
│  YOLOv8 Model           │
│  (93% accuracy, 10 FPS) │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Data Pipeline          │
│  Plate extraction       │
│  Validation             │
│  Structured logging     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Automated Reporting    │
│  Excel generation       │
│  Email delivery (EOD)   │
└─────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Detection Model** | YOLOv8 (Custom-trained) | Real-time license plate detection |
| **Computer Vision** | OpenCV | Image processing & plate extraction |
| **Backend** | Python 3.8+ | Core pipeline orchestration |
| **Data Storage** | Excel (OpenPyXL) | Structured vehicle logs |
| **Notifications** | SMTP | End-of-day email reports |
| **Version Control** | Git | Deployment tracking |

---

## Performance Metrics

### Accuracy & Reliability

| Metric | Value |
|--------|-------|
| **License Plate Detection** | 93% accuracy |
| **Processing Speed** | 10 FPS real-time throughput |
| **Data Consistency** | 100% (500+ entries processed) |
| **System Uptime** | Autonomous since deployment |
| **Manual Intervention** | Zero required |

### Operational Impact

- **Time Saved:** 2+ hours daily operational overhead eliminated
- **Error Reduction:** Eliminated human data entry errors
- **Scalability:** Handles unlimited entry/exit events autonomously
- **Reliability:** Graceful degradation on edge cases (poor lighting, angled plates, weather)

---

## System Architecture

### Data Flow

```
Raw Image Capture
      ↓
ANPR Camera (Entry/Exit Points)
      ↓
YOLOv8 Detection Model
      ↓
Plate Extraction & Validation
      ↓
Data Standardization
      ↓
Excel Log Generation
      ↓
SMTP Email Notification
      ↓
End-of-Day Report Delivery
```

### Pipeline Stages

**1. Image Capture**
- Dual ANPR cameras monitor entry and exit points
- Synchronized event capture for accurate vehicle counting

**2. Detection & Extraction**
- Custom-trained YOLOv8 model processes frames at 10 FPS
- OpenCV handles image preprocessing and plate localization
- Achieves 93% accuracy across diverse lighting and weather conditions

**3. Validation & Logging**
- Extracted plates validated against format rules
- Timestamps and entry/exit classification recorded
- Data standardized for reporting

**4. Automated Reporting**
- OpenPyXL generates structured Excel files
- SMTP sends end-of-day reports via email
- Requires zero human intervention

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Pip package manager
- Two ANPR cameras (or one for testing)
- Email account (for SMTP notifications)

### Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# Camera Configuration
CAMERA_ENTRY_IP=192.168.1.100
CAMERA_EXIT_IP=192.168.1.101
CAPTURE_FPS=10
CONFIDENCE_THRESHOLD=0.5

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=operations@facility.com

# System Configuration
LOG_OUTPUT_PATH=./logs/
EXCEL_OUTPUT_PATH=./reports/
MODEL_PATH=./models/yolov8_license_plate.pt
```

### Model Setup

The YOLOv8 model is pre-trained on 1000+ license plate images. Place the model file in the `./models/` directory:

```bash
models/
└── yolov8_license_plate.pt
```

---

## Usage

### Running the System

```bash
# Start the main pipeline
python main.py

# With debug logging
python main.py --debug

# Dry run (no email/file writes)
python main.py --dry-run
```

### Generate Report Manually

```bash
# Generate end-of-day report
python generate_report.py --date 2025-04-14 --output ./reports/

# Generate with custom date range
python generate_report.py --start-date 2025-04-01 --end-date 2025-04-14
```

### System Logs

Logs are stored in `./logs/`:

```bash
# View real-time logs
tail -f ./logs/pipeline.log

# Check error logs
tail -f ./logs/errors.log
```

---

## Project Structure

```
automated-vehicle-logging/
│
├── main.py                      # Main pipeline orchestrator
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment configuration template
├── config.py                    # Configuration loader
│
├── models/
│   └── yolov8_license_plate.pt  # Pre-trained YOLOv8 model
│
├── src/
│   ├── __init__.py
│   ├── camera.py                # ANPR camera interface
│   ├── detection.py             # YOLOv8 detection module
│   ├── validation.py            # Plate validation & filtering
│   ├── logger.py                # Structured data logging
│   ├── report_generator.py      # Excel report generation
│   └── email_notifier.py        # SMTP email service
│
├── tests/
│   ├── test_detection.py        # Model accuracy tests
│   ├── test_validation.py       # Data validation tests
│   └── test_pipeline.py         # Integration tests
│
├── logs/
│   ├── pipeline.log             # Main operation logs
│   └── errors.log               # Error logs
│
├── reports/
│   └── vehicle_log_YYYY-MM-DD.xlsx  # Generated reports
│
└── docs/
    ├── architecture.md          # System architecture details
    ├── deployment.md            # Deployment instructions
    └── troubleshooting.md       # Common issues & solutions
```

---

## Key Features

### ✅ Real-time Detection
- Processes video frames at 10 FPS
- Minimal latency between vehicle detection and logging

### ✅ High Accuracy
- 93% license plate detection accuracy
- Trained on diverse lighting and weather conditions
- Graceful handling of edge cases

### ✅ Fully Autonomous
- Zero manual intervention post-deployment
- Automatic error recovery and retry logic
- Handles system failures gracefully

### ✅ Structured Data Output
- Standardized Excel reports
- Automated end-of-day email notifications
- Query-ready database format

### ✅ Production-Grade
- Comprehensive logging and monitoring
- Error handling and recovery protocols
- Scalable architecture

---

## Technical Insights

### Model Training & Deployment

The YOLOv8 model was trained on 1000+ annotated license plate images with various conditions:

- **Diverse lighting:** Daylight, overcast, night-time scenarios
- **Various angles:** Head-on, angled, side-views
- **Weather conditions:** Clear, rainy, foggy
- **Vehicle types:** Cars, trucks, motorcycles

**Key Challenge:** Model accuracy (93%) doesn't guarantee deployment readiness. Real-world edge cases required iterative refinement and fallback handling.

### Real-time Processing Trade-offs

At 10 FPS throughput:
- Balanced inference time (100ms per frame)
- Acceptable accuracy for production use
- Minimal computational overhead on facility hardware

This required deliberate trade-off decisions between:
- Model size vs. detection accuracy
- Inference latency vs. throughput
- Memory usage vs. processing speed

### Backend Robustness

The system prioritizes reliability over raw speed:

- **Error Recovery:** Automatic retry logic on detection failures
- **Graceful Degradation:** System continues operation even if cameras drop briefly
- **Data Validation:** Multi-stage validation prevents corrupt entries
- **Monitoring:** Continuous logging of system health metrics

---

## Deployment

### Hardware Requirements

- **Processor:** Intel i5/i7 or equivalent (for real-time inference)
- **Memory:** 8GB RAM minimum
- **Storage:** 50GB for logs and reports
- **Network:** Gigabit Ethernet for camera feeds
- **Cameras:** 2x ANPR-capable security cameras

### Installation Steps

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` with camera IPs and email settings
4. Place pre-trained model in `./models/`
5. Run system: `python main.py`

For detailed deployment instructions, see [docs/deployment.md](docs/deployment.md)

---

## Troubleshooting

### Low Detection Accuracy

**Issue:** Model returning <85% accuracy
**Solution:** 
- Check camera focus and alignment
- Verify model file integrity
- Review lighting conditions at entry/exit points
- See [docs/troubleshooting.md](docs/troubleshooting.md) for detailed steps

### Missing Email Notifications

**Issue:** Reports not being sent via email
**Solution:**
- Verify SMTP credentials in `.env`
- Check firewall rules for SMTP port
- Review email service logs
- Test SMTP connection: `python -m src.email_notifier --test`

### System Crashes or Hangs

**Issue:** Pipeline stops unexpectedly
**Solution:**
- Check system logs: `tail -f logs/errors.log`
- Verify camera connectivity
- Check disk space in log directory
- Restart service: `python main.py`

For more troubleshooting guidance, see [docs/troubleshooting.md](docs/troubleshooting.md)

---

## Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_detection.py -v

# Run with coverage
pytest tests/ --cov=src/
```

### Test Coverage

- **Unit Tests:** Individual component validation
- **Integration Tests:** Full pipeline end-to-end tests
- **Accuracy Tests:** Model performance on validation dataset

---

## Performance Benchmarks

### Processing Speed

| Operation | Time |
|-----------|------|
| Image capture | ~5ms |
| YOLOv8 inference | ~70ms |
| Plate extraction | ~15ms |
| Validation | ~5ms |
| **Total per frame** | **~95ms** |

At 10 FPS, this leaves sufficient headroom for system overhead.

### Accuracy Breakdown

| Scenario | Accuracy |
|----------|----------|
| Clear daylight | 96% |
| Overcast conditions | 94% |
| Night-time (with lights) | 91% |
| Rainy weather | 89% |
| **Overall** | **93%** |

---

## Contributing

This is a deployed production system. For modifications:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test thoroughly
3. Ensure all tests pass: `pytest tests/`
4. Submit a pull request with detailed documentation

---

## License

This project is proprietary. Unauthorized use, modification, or distribution is prohibited.

---

## Contact & Support

For deployment issues, technical questions, or feature requests:

- **GitHub Issues:** [Create an issue](https://github.com/yourusername/automated-vehicle-logging/issues)
- **Email:** harshvardhanbeniwal5@gmail.com
- **LinkedIn:** [linkedin.com/in/harshvardhan-beniwal](https://linkedin.com/in/harshvardhan-beniwal)

---

## Changelog

### Version 1.0 (Current)
- ✅ Real-time vehicle detection and logging
- ✅ 93% license plate accuracy
- ✅ Automated Excel reporting
- ✅ Email notifications
- ✅ Production deployment

---

## Acknowledgments

- YOLOv8 by Ultralytics
- OpenCV community
- Python SMTP and OpenPyXL libraries

---

**Last Updated:** April 2025  
**Status:** Production - Actively Running
