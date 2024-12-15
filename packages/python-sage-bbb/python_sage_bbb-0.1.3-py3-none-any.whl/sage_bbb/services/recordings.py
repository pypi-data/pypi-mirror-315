from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Recordings:
    """
    This class handles operations related to recordings in BigBlueButton.

    Args:
        client: The client used to interact with the BigBlueButton server.

    Example:
        bbb_client = BigBlueButtonClient(
        "http://example.com/bigbluebutton/api/", "secret"
        )
        recordings = Recordings(bbb_client)
    """

    def __init__(self, client: "BigBlueButtonClient") -> None:
        self.client = client

    def get_recordings(
        self, meeting_id: str, metadata: Optional[Dict[str, Any]] = None
    ) -> dict:
        """
        Retrieves the recordings for a specific meeting, optionally filtered by metadata.

        Args:
            meeting_id (str): The unique identifier for the meeting.
            metadata (dict, optional): A dictionary of metadata to filter the recordings.

        Returns:
            dict: A dictionary containing information about the recordings
            for the specified meeting.

        Example:
            recordings = Recordings(bbb_client)
            recordings_response = recordings.get_recordings("random-9887584")
            print(recordings_response)

            filtered_recordings = recordings.get_recordings(
            "random-9887584", {"state": "published"}
            )
            print(filtered_recordings)
        """
        params = {"meetingID": meeting_id}
        if metadata:
            params.update(metadata)
        logger.info("Retrieving recordings for meeting ID: %s with params: %s", meeting_id, params)
        response = self.client.send_request("getRecordings", params)
        logger.info("Recordings retrieved successfully for meeting ID: %s", meeting_id)
        return self.client.parse_response(response.content)

    def publish_recording(self, recording_id: str, publish: bool) -> Dict[str, Any]:
        """
        Publishes or unpublishes a specific recording.

        Args:
            recording_id (str): The unique identifier for the recording.
            publish (bool): True to publish the recording, False to unpublish.

        Returns:
            dict: The response from the API call.

        Example:
            recordings = Recordings(bbb_client)
            publish_response = recordings.publish_recording("recording-id-1234", True)
            print(publish_response)
        """
        params = {
            "recordID": recording_id,
            "publish": "true" if publish else "false",
        }
        logger.info("Setting publish status for recording ID: %s to %s", recording_id, publish)
        response = self.client.send_request("publishRecordings", params)
        logger.info("Publish status set successfully for recording ID: %s", recording_id)
        return self.client.parse_response(response.content)

    def delete_recording(self, recording_id: str) -> Dict[str, Any]:
        """
        Deletes a specific recording.

        Args:
            recording_id (str): The unique identifier for the recording.

        Returns:
            dict: The response from the API call.

        Example:
            recordings = Recordings(bbb_client)
            delete_response = recordings.delete_recording("recording-id-1234")
            print(delete_response)
        """
        params = {
            "recordID": recording_id,
        }
        logger.info("Deleting recording ID: %s", recording_id)
        response = self.client.send_request("deleteRecordings", params)
        logger.info("Recording ID: %s deleted successfully.", recording_id)
        return self.client.parse_response(response.content)

    def update_recordings(
        self, meeting_id: str, metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Updates the metadata for a specific recording.

        Args:
            meeting_id (str): The unique identifier for the meeting.
            metadata (dict): A dictionary containing the metadata to update.

        Returns:
            dict: The response from the API call.

        Example:
            recordings = Recordings(bbb_client)
            update_response = recordings.update_recordings(
            "recording-id-1234", {"title": "New Title"}
            )
            print(update_response)
        """
        params = {"meetingID": meeting_id}
        if metadata:
            params.update(metadata)
        logger.info("Updating recordings for meeting ID: %s with metadata: %s", meeting_id, metadata)
        response = self.client.send_request("updateRecordings", params)
        logger.info("Recordings updated successfully for meeting ID: %s", meeting_id)
        return self.client.parse_response(response.content)

    def get_recording_text_tracks(self, record_id: str) -> Dict[str, Any]:
        """
        Retrieves the text tracks for a specific recording.

        Args:
            record_id (str): The unique identifier for the recording.

        Returns:
            dict: The response from the API call.

        Example:
            recordings = Recordings(bbb_client)
            text_tracks_response = recordings.get_recording_text_tracks(
            "recording-id-1234"
            )
            print(text_tracks_response)
        """
        params = {
            "recordID": record_id,
        }
        logger.info("Retrieving text tracks for recording ID: %s", record_id)
        response = self.client.send_request("getRecordingTextTracks", params)
        logger.info("Text tracks retrieved successfully for recording ID: %s", record_id)
        return self.client.parse_response(response.content)

    def put_recording_text_track(
        self, record_id: str, track_file: Any
    ) -> Dict[str, Any]:
        """
        Uploads a text track for a specific recording.

        Args:
            record_id (str): The unique identifier for the recording.
            track_file: The text track file to upload.

        Returns:
            dict: The response from the API call.

        Example:
            recordings = Recordings(bbb_client)
            put_track_response = recordings.put_recording_text_track(
            "recording-id-1234", open("track.vtt", "rb")
            )
            print(put_track_response)
        """
        params = {
            "recordID": record_id,
        }
        files = {"file": track_file}
        logger.info("Uploading text track for recording ID: %s", record_id)
        response = self.client.send_request(
            "putRecordingTextTrack", params, files=files
        )
        logger.info("Text track uploaded successfully for recording ID: %s", record_id)
        return self.client.parse_response(response.content)
