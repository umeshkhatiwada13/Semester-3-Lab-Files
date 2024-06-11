import pandas as pd
import googleapiclient.discovery
from googleapiclient.discovery import build
from Utils import Utils as utils
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create YouTube resource object
youtube = build('youtube',
                'v3',
                developerKey=os.getenv("API_KEY"))

# Load the CSV file with status
file_path = './files'
csv_file_path = file_path + '/youtube_video_links.csv'
df = pd.read_csv(csv_file_path)

print("File Size ", df.size)

# Check if 'status' column exists
if 'status' not in df.columns:
    # Add a status column and initialize with 'Not Fetched'
    df['status'] = 'Not Fetched'

    # Save the updated CSV file
    df.to_csv(csv_file_path, index=False)

# Initialize or get the start index
start_index = 0
# if 'd1' in df.columns and pd.notna(df.at[0, 'd1']) and df.at[0, 'd1'] != 0:
#     start_index = int(df.at[0, 'd1'])

print(f"Starting from index {start_index}")

# Initialize start row number
start_row_number = start_index  # Initialize start_row_number here

# List to store results
results = []

# Get the start video ID for the output filename
start_video_id = None
comments = None

# Process each video ID from the start index
for idx in range(start_index, len(df)):
    print(f"Processing video {idx}")
    is_comment_disabled = False
    # reset comment for each iteration
    comments = ''

    row = df.iloc[idx]
    if row['status'] == 'Not Fetched':
        if start_video_id is None:
            start_video_id = row['youtubeId']

        video_id = row['youtubeId']
        try:
            video_details = utils.get_video_details(youtube, video_id)
            comments = utils.get_comments(youtube, video_id)
        except googleapiclient.errors.HttpError as e:
            # print(e)
            if e.resp.status == 404:
                print(f"Video not found: {video_id}")
                df.at[idx, 'status'] = 'Video Not Found'
                continue
            elif e.resp.status == 403:
                error_reason = e.content.decode().lower()
                if "exceeded" in error_reason:
                    print(f"Quota exceeded. Stopping the execution.")
                    break  # Stop the execution if quota is exceeded
                elif "commentsdisabled" in error_reason:
                    print(f"Error fetching data for video {video_id}: {error_reason}")
                    is_comment_disabled = True
                    # continue
            elif e.resp.status in [500, 503]:
                print(f"Temporary server error for video {video_id}")
                break
            else:
                print(f"Error fetching data for video {video_id}")
                continue

        if video_details:
            video_details['comments'] = comments
            results.append(video_details)
            df.at[idx, 'status'] = 'Fetched, Comment Disabled' if is_comment_disabled else 'Fetched'

        # Periodically save results and update CSV
        if len(results) >= 10:  # Save every 1000 records
            end_video_id = video_details['video_id']
            utils.save_results_to_csv(results, start_row_number, idx)
            results = []  # Clear results after saving
            start_video_id = None  # Reset start_video_id for the next batch
            start_row_number = idx + 1  # Update start row number

            # Update the d1 column with the current index
            df.at[0, 'd1'] = idx
            df.to_csv(csv_file_path, index=False)

print("results ", results)
# Save any remaining results
if results:
    end_video_id = results[-1]['video_id']
    utils.save_results_to_csv(results, start_row_number, idx)
    # Update the d1 column with the current index
    df.at[0, 'd1'] = idx
    df.to_csv(csv_file_path, index=False)
print(df.head())

print("Processing complete.")
