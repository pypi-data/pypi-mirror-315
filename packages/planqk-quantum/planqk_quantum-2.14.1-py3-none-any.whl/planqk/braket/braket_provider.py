from typing import Dict, Type, List

from planqk.braket.aws_device import PlanqkAwsDevice
from planqk.client.backend_dtos import BackendDto
from planqk.exceptions import BackendNotFoundError, PlanqkClientError
from planqk.qiskit.provider import _PlanqkProvider


class PlanqkBraketProvider(_PlanqkProvider):
    _device_mapping: Dict[str, Type[PlanqkAwsDevice]] = {}

    @classmethod
    def register_device(cls, device_id: str):
        """For internal use only. Binds a device class to a PlanQK backend id."""
        def decorator(device_cls: Type[PlanqkAwsDevice]):
            cls._device_mapping[device_id] = device_cls
            return device_cls
        return decorator

    def get_device(self, backend_id: str) -> PlanqkAwsDevice:
        """
        Retrieves an AWS Braket Device based on the provided PlanQK backend id.

        Args:
            backend_id (str): The unique identifier for the backend.

        Returns:
            PlanqkAwsDevice: The AWS Braket device corresponding to the backend id.

        Raises:
            BackendNotFoundError: If the backend with the given id cannot be found or is not supported by the Braket SDK.

        Note:
            An overview of the supported backends and their IDs can be found at: https://platform.planqk.de/quantum-backends
        """
        backend_info = self._get_backend_info(backend_id)
        return self._get_planqk_braket_device(backend_info)

    def devices(self) -> List[str]:
        """
        Retrieves a list of all AWS Braket devices (backends) provided through PlanQK that can be accessed using this SDK.

        Returns:
            List[str]: A list of supported AWS Braket device IDs.
        """
        return list(self._device_mapping.keys())

    def _get_backend_info(self, backend_id):
        try:
            return self._client.get_backend(backend_id=backend_id)
        except PlanqkClientError as e:
            if e.response.status_code == 404:
                raise BackendNotFoundError(f"PlanQK device with id {backend_id} not found.")
            raise e

    def _get_planqk_braket_device(self, backend_info: BackendDto) -> PlanqkAwsDevice:
        device_class = self._device_mapping.get(backend_info.id)
        if device_class:
            return device_class(planqk_client=self._client, backend_info=backend_info)
        else:
            raise BackendNotFoundError(f"Braket device '{backend_info.id}' is not supported.")

