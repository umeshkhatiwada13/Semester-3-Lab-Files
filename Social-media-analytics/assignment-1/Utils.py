class Utils:
    # Function to get video details
    def get_video_details(video_id):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        if not response['items']:
            return None

        video_info = response['items'][0]
        snippet = video_info['snippet']
        statistics = video_info['statistics']
        content_details = video_info['contentDetails']
        title = snippet.get('title', "")  # Extract title
        description = snippet.get('description', "")
        view_count = statistics.get('viewCount', 0)
        like_count = statistics.get('likeCount', 0)
        dislike_count = statistics.get('dislikeCount', 0)
        comment_count = statistics.get('commentCount', 0)
        duration = content_details.get('duration', "")
        favorite_count = statistics.get('favoriteCount', 0)

        return {
            "video_id": video_id,
            "title": title,
            "description": description,
            "view_count": view_count,
            "like_count": like_count,
            "dislike_count": dislike_count,
            "comment_count": comment_count,
            "duration": duration,
            "favorite_count": favorite_count
        }

    # Function to get comments
    def get_comments(video_id):
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="relevance"  # Order comments by relevance (most popular)
        )
        response = request.execute()

        comments = []
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        return comments

    # Function to save results to a CSV file
    def save_results_to_csv(results, start_video_id, end_video_id):
        if results:
            output_filename = f'/content/drive/MyDrive/Colab Notebooks/Data/youtube_video_data_{start_video_id}_to_{end_video_id}.csv'
            results_df = pd.DataFrame(results)
            results_df.to_csv(output_filename, index=False)
            print(f"Saved results to {output_filename}")
