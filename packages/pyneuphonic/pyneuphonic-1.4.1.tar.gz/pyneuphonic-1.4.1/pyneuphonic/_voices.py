from typing import List

import httpx

from ._endpoint import Endpoint
from .models import VoicesResponse, VoiceItem


class Voices(Endpoint):
    def get(self) -> List[VoiceItem]:
        """List all the voices."""
        response = httpx.get(
            f'{self.http_url}/voices',
            headers=self.headers,
            timeout=self.timeout,
        )

        if not response.is_success:
            raise httpx.HTTPStatusError(
                f'Failed to fetch voices. Status code: {response.status_code}. Error: {response.text}',
                request=response.request,
                response=response,
            )

        voice_response = VoicesResponse(**response.json())

        return voice_response.data.voices

    def clone(
        self, voice_name: str, voice_file_path: str, voice_tags: List[str] = []
    ) -> dict:
        """
        Clone a voice by uploading a file with the specified name and tags.

        Parameters
        ----------
        voice_name : str
            The name of the new cloned voice.
        voice_file_path : str
            Path to the voice file (e.g., a .wav file) to be uploaded.
        voice_tags : List[str]
            Tags associated with the voice. Default is an empty list.

        Returns
        -------
        dict
            A dictionary with the response data from the API.

        Raises
        ------
        httpx.HTTPStatusError
            If the request to clone the voice fails.
        """

        # Prepare the multipart form-data payload
        data = {
            'voice_tags': voice_tags,
        }
        files = {'voice_file': open(voice_file_path, 'rb')}

        # Send the POST request with voice_name as a query parameter
        response = httpx.post(
            f'{self.http_url}/voices/clone?voice_name={voice_name}',
            data=data,
            files=files,
            headers=self.headers,
            timeout=self.timeout,
        )

        # Handle response errors
        if not response.is_success:
            raise httpx.HTTPStatusError(
                f'Failed to clone voice. Status code: {response.status_code}. Error: {response.text}',
                request=response.request,
                response=response,
            )

        # Return the JSON response content as a dictionary
        return response.json()

    def update(
        self, voice_file_path: str, voice_id: str = None, voice_name: str = None
    ) -> dict:
        """
        Update a voice by its ID or name.

        Parameters
        ----------
        voice_id : str
            The ID of the voice to be deleted.
        voice_name : str
            The name of the voice to be deleted.

        Returns
        -------
        dict
            A dictionary with the response data from the API.

        Raises
        ------
        httpx.HTTPStatusError
            If the request to update the voice fails. This will usually trigger if you do not have
            permissions to update the voice.
        """

        if not voice_id:
            # Get all voices for this user
            voices = self.get()
            try:
                # Fetch voice id
                voice_id = next(
                    voice.id for voice in voices if voice.name == voice_name
                )

            except StopIteration as e:
                raise ValueError(
                    f'No voice found with the name {voice_name}. You cannot update this voice.'
                )

        files = {'voice_file': open(voice_file_path, 'rb')}

        response = httpx.patch(
            f'{self.http_url}/voices/clone?voice_id={voice_id}',
            headers=self.headers,
            timeout=self.timeout,
            files=files,
        )

        # Handle response errors
        if not response.is_success:
            raise httpx.HTTPStatusError(
                f'Failed to update voice. Status code: {response.status_code}. Error: {response.text}',
                request=response.request,
                response=response,
            )

        # Return the JSON response content as a dictionary
        return response.json()

    def delete(self, voice_id: str = None, voice_name=None) -> dict:
        """
        Delete a voice by its ID.

        Parameters
        ----------
        voice_id : str
            The ID of the voice to be deleted.

        Returns
        -------
        dict
            A dictionary with the response data from the API.

        Raises
        ------
        httpx.HTTPStatusError
            If the request to delete the voice fails. This will usually trigger if you do not have
            permissions to delete the voice.
        """
        if not voice_id:
            # Get all voices for this user
            voices = self.get()
            try:
                # Fetch voice id
                voice_id = next(
                    voice.id for voice in voices if voice.name == voice_name
                )

            except StopIteration as e:
                raise ValueError(
                    f'No voice found with the name {voice_name}. You cannot Delete this voice.'
                )

        response = httpx.delete(
            f'{self.http_url}/voices/clone?voice_id={voice_id}',
            headers=self.headers,
            timeout=self.timeout,
        )

        # Handle response errors
        if not response.is_success:
            raise httpx.HTTPStatusError(
                f'Failed to delete voice. Status code: {response.status_code}. Error: {response.text}',
                request=response.request,
                response=response,
            )

        # Return the JSON response content as a dictionary
        return response.json()
