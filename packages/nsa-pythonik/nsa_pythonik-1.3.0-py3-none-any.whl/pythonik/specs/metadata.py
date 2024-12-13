from loguru import logger
from pythonik.models.base import Response
from pythonik.models.metadata.views import ViewMetadata
from pythonik.models.mutation.metadata.mutate import (
    UpdateMetadata,
    UpdateMetadataResponse,
)
from pythonik.specs.base import Spec
from typing import Literal, Union, Dict, Any

ASSET_METADATA_FROM_VIEW_PATH = "assets/{}/views/{}"
UPDATE_ASSET_METADATA = "assets/{}/views/{}/"
ASSET_OBJECT_VIEW_PATH = "assets/{}/{}/{}/views/{}/"
PUT_METADATA_DIRECT_PATH = "{}/{}/"


ObjectType = Literal["segments"]


class MetadataSpec(Spec):
    server = "API/metadata/"

    def get_asset_metadata(
        self, 
        asset_id: str, 
        view_id: str, 
        intercept_404: ViewMetadata | bool = False,
        **kwargs
    ) -> Response:
        """Given an asset id and the asset's view id, fetch metadata from the asset's view

        Args:
            asset_id: The asset ID to get metadata for
            view_id: The view ID to get metadata from
            intercept_404: Iconik returns a 404 when a view has no metadata, intercept_404 will intercept that error
                and return the ViewMetadata model provided
            **kwargs: Additional kwargs to pass to the request

        Note:
            You can no longer call response.raise_for_status, so be careful using this.
            Call raise_for_status_404 if you still want to raise status on 404 error
        """
        resp = self._get(ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id), **kwargs)

        if intercept_404 and resp.status_code == 404:
            parsed_response = self.parse_response(resp, ViewMetadata)
            parsed_response.data = intercept_404
            parsed_response.response.raise_for_status_404 = (
                parsed_response.response.raise_for_status
            )

            parsed_response.response.raise_for_status = lambda: logger.warning(
                "raise for status disabled due to intercept_404, please call"
                " raise_for_status_404 to throw an error on 404"
            )
            return parsed_response

        return self.parse_response(resp, ViewMetadata)

    def update_asset_metadata(
        self, 
        asset_id: str, 
        view_id: str, 
        metadata: Union[UpdateMetadata, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """Given an asset's view id, update metadata in asset's view
        
        Args:
            asset_id: The asset ID to update metadata for
            view_id: The view ID to update metadata in
            metadata: The metadata to update, either as UpdateMetadata model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request
        """
        json_data = self._prepare_model_data(metadata, exclude_defaults=exclude_defaults)
        resp = self._put(
            UPDATE_ASSET_METADATA.format(asset_id, view_id), 
            json=json_data,
            **kwargs
        )

        return self.parse_response(resp, UpdateMetadataResponse)
    
    def put_metadata_direct(
        self, 
        object_type: str, 
        object_id: str, 
        metadata: Union[UpdateMetadata, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """Edit metadata values directly without a view.

        Args:
            object_type: The type of object to update metadata for
            object_id: The unique identifier of the object
            metadata: Metadata values to update, either as UpdateMetadata model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response[UpdateMetadataResponse]

        Required roles:
            - admin_access

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 403 Forbidden (non-admin user)
            - 404 Object not found

        Note:
            Use with caution. This method bypasses standard validation checks for speed,
            and will write to the database even if the object_id doesn't exist. Admin
            access required as this is a potentially dangerous operation.
        """
        json_data = self._prepare_model_data(metadata, exclude_defaults=exclude_defaults)
        resp = self._put(
            PUT_METADATA_DIRECT_PATH.format(object_type, object_id),
            json=json_data,
            **kwargs
        )

        return self.parse_response(resp, UpdateMetadataResponse)

    def put_object_view_metadata(
        self,
        asset_id: str,
        object_type: ObjectType,
        object_id: str,
        view_id: str,
        metadata: Union[UpdateMetadata, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """Put metadata for a specific sub-object view of an asset
        
        Args:
            asset_id: The asset ID to update metadata for
            object_type: The type of object to update metadata for
            object_id: The object ID to update metadata for
            view_id: The view ID to update metadata in
            metadata: The metadata to update, either as UpdateMetadata model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request
        """
        json_data = self._prepare_model_data(metadata, exclude_defaults=exclude_defaults)
        endpoint = ASSET_OBJECT_VIEW_PATH.format(asset_id, object_type, object_id, view_id)
        resp = self._put(
            endpoint,
            json=json_data,
            **kwargs
        )

        return self.parse_response(resp, UpdateMetadataResponse)

    def put_segment_view_metadata(
        self,
        asset_id: str,
        segment_id: str,
        view_id: str,
        metadata: Union[UpdateMetadata, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """Put metadata for a segment view (backwards compatibility wrapper)
        
        Args:
            asset_id: The asset ID to update metadata for
            segment_id: The segment ID to update metadata for
            view_id: The view ID to update metadata in
            metadata: The metadata to update, either as UpdateMetadata model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request
        """
        return self.put_object_view_metadata(
            asset_id=asset_id,
            object_type="segments",
            object_id=segment_id,
            view_id=view_id,
            metadata=metadata,
            exclude_defaults=exclude_defaults,
            **kwargs
        )

    def put_segment_metadata(
        self, 
        asset_id: str, 
        segment_id: str, 
        view_id: str, 
        metadata: Union[UpdateMetadata, Dict[str, Any]], 
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """Put metadata for a segment of an asset
        
        Args:
            asset_id: The asset ID to update metadata for
            segment_id: The segment ID to update metadata for
            view_id: The view ID to update metadata in
            metadata: The metadata to update, either as UpdateMetadata model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request
        """
        return self.put_object_view_metadata(
            asset_id, 
            "segments", 
            segment_id, 
            view_id, 
            metadata, 
            exclude_defaults=exclude_defaults,
            **kwargs
        )
