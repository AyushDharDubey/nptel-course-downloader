import requests
from tqdm import tqdm
import os
import json

def download_video(url, filename):
    """
    Downloads a video from a URL with a progress bar, handling potential errors.
    """
    try:
        # Use a session object for potential connection pooling
        with requests.Session() as s:
            response = s.get(url, stream=True, timeout=30)
            response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024

        print(f"Downloading {filename}...")
        with tqdm(total=total_size, unit='iB', unit_scale=True, desc=filename, leave=False) as progress_bar:
            with open(filename, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        if total_size != 0 and progress_bar.n != total_size:
            print(f"Error: Download incomplete for {filename}")
        else:
            print(f"Successfully downloaded {filename}")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Video not found at {url} (404 Error). Skipping.")
        else:
            print(f"HTTP error occurred: {http_err} for URL: {url}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during request: {req_err} for URL: {url}")
    except Exception as e:
        print(f"An unexpected error occurred for {filename}: {e}")

def sanitize_filename(name):
    """
    Removes characters that are invalid for directory/file names.
    """
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()


def main():
    """
    Main function to get user input and start the download process.
    """
    course_id = input("Enter the course id (e.g., 105107463): ")

    details_api_url = f"https://nptel.ac.in/api/subject-details/{course_id}"
    print(f"\nFetching course details from {details_api_url}...")
    course_details = None
    course_dir = f"course_{course_id}" # Fallback directory name

    try:
        response = requests.get(details_api_url, timeout=30)
        response.raise_for_status()
        course_details = response.json()

        course_data = course_details.get('data', {})

        course_name = course_data.get('title', '').strip()
        if course_name:
            course_dir = sanitize_filename(course_name)
        os.makedirs(course_dir, exist_ok=True)
        print(f"Created course directory: {course_dir}")

        details_filename = os.path.join(course_dir, f"{course_id}_course_details.json")
        with open(details_filename, 'w', encoding='utf-8') as f:
            json.dump(course_details, f, ensure_ascii=False, indent=4)
        print(f"Successfully saved course details to {details_filename}")

        if course_data and 'syllabus_url' in course_data and course_data['syllabus_url']:
            syllabus_url = course_data['syllabus_url']
            syllabus_filename = os.path.join(course_dir, syllabus_url.split('/')[-1])
            print(f"\nFound syllabus at {syllabus_url}")
            download_video(syllabus_url, syllabus_filename) # Reusing the download function
        else:
            print("Syllabus download URL not found in course details.")

    except requests.exceptions.RequestException as e:
        print(f"Could not fetch course details: {e}")
    except json.JSONDecodeError:
        print("Failed to parse course details from API response.")
    
    base_url_part = f"https://media.dev.nptel.ac.in/content/mp4/{course_id[:3]}/{course_id[3:6]}/{course_id}/MP4/"

    try:
        total_modules = int(input("Enter the total number of modules in the course (e.g., 12): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    for module_number in range(1, total_modules + 1):
        print(f"\n----- Processing Module {module_number} -----")

        start_lecture = (module_number - 1) * 5 + 1
        end_lecture = module_number * 5

        output_dir = os.path.join(course_dir, f"module_{module_number}_videos")
        os.makedirs(output_dir, exist_ok=True)

        print(f"Starting download for lectures {start_lecture} to {end_lecture}.")

        for lec_num in range(start_lecture, end_lecture + 1):
            # Format lecture number to be two digits (e.g., 01, 02, 10)
            lecture_str = f"{lec_num:02d}"
            filename = f"mod{module_number:02d}lec{lecture_str}.mp4"
            file_path = os.path.join(output_dir, filename)
            url = f"{base_url_part}{filename}"
            
            download_video(url, file_path)

if __name__ == "__main__":
    main()