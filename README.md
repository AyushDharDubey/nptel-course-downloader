# NPTEL Course Downloader

A simple Python script to download video lectures, course details, and the syllabus for any course from the NPTEL website.

The script organizes downloaded content into a structured directory, making it easy to navigate your offline courses.

## Features

- **Bulk Download:** Downloads all video lectures for a given course ID.
- **Organized Structure:** Automatically creates a main course folder and sub-folders for each module's videos.
- **Fetches Metadata:** Retrieves and saves course details (like title and description) into a `_course_details.json` file.
- **Syllabus Download:** Finds and downloads the course syllabus PDF if available.
- **User-Friendly:** Interactive prompts for course ID and number of modules.
- **Progress Bars:** Uses `tqdm` to show a progress bar for each download.
- **Error Handling:** Gracefully handles common issues like 404 errors for missing videos.

## Prerequisites

- Python 3.6+
- `pip` (Python package installer)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AyushDharDubey/nptel-course-downloader.git
    cd nptel-course-downloader
    ```

2.  **Install the required packages:**
    The script depends on the `requests` and `tqdm` libraries. You can install them using the provided `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Find the Course ID:**
    Navigate to the NPTEL course page you're interested in. The URL will look something like this:
    `https://nptel.ac.in/courses/105107463`

    The course ID is `105107463` in the above example. For this script, you'll often find it in URLs for course resources.

2.  **Run the script:**
    ```bash
    python nptel_download.py
    ```

3.  **Follow the prompts:**
    The script will ask for two things:
    - **Course ID:** Enter the ID you found (e.g., `105107463`).
    - **Total number of modules:** Enter the total number of modules in the course.

    ```
    Enter the course id (e.g., 105107463): 105107463
    Enter the total number of modules in the course (e.g., 12): 12
    ```

The script will then create a directory named after the course title and start downloading the content.

### Directory Structure

After running, you will have a folder structure like this:

```
Programming in C++/
├── 105107463_course_details.json
├── syllabus.pdf
├── module_1_videos/
│   ├── mod01lec01.mp4
│   ├── mod01lec02.mp4
│   └── ...
└── module_2_videos/
    ├── mod02lec06.mp4
    └── ...
```

## Disclaimer

This script is intended for personal, educational use only. Please respect the terms of service of the NPTEL platform. The content downloaded is the intellectual property of NPTEL and its content creators.