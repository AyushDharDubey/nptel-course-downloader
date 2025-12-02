import requests
from tqdm import tqdm
import os

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

def main():
    """
    Main function to get user input and start the download process.
    """
    base_url_part = input("Enter the course id: ")
    base_url_part = f"https://media.dev.nptel.ac.in/content/mp4/{base_url_part[:3]}/{base_url_part[3:6]}/{base_url_part}/MP4/"
    
    if not base_url_part.endswith('/'):
        base_url_part += '/'

    try:
        total_modules = int(input("Enter the total number of modules in the course (e.g., 12): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    for module_number in range(1, total_modules + 1):
        print(f"\n----- Processing Module {module_number} -----")
        
        # Calculate lecture range based on the pattern (5 lectures per module)
        start_lecture = (module_number - 1) * 5 + 1
        end_lecture = module_number * 5

        # Create a directory for the current module if it doesn't exist
        output_dir = f"module_{module_number}_videos"
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