import os
import shutil

from ocfl_rehydration.drs_descriptor import DrsDescriptor
from ocfl_rehydration.ocfl_inventory import OcflInventory


class Rehydrator():
    """
    A class for rehydrating files from an OCFL object.

    Attributes:
        ocfl_obj_root (str): The path to the root directory of the OCFL object.
        output_dir (str): The path to the directory where rehydrated files will be written.
    """

    def __init__(self, ocfl_obj_root, output_dir) -> None:
        """
        Initializes a Rehydrator object.

        Args:
            ocfl_obj_root (str): The path to the root directory of the OCFL object.
            output_dir (str): The path to the directory where rehydrated files will be written.
        """
        self.ocfl_obj_root = ocfl_obj_root
        self.output_dir = output_dir

    def __repr__(self) -> str:
        return "Rehydrator..."

    def rehydrate(self):
        """
        Rehydrates files from the OCFL object.
        """
        ocfl_inventory = self._get_ocfl_inventory()
        drs_descriptor = self._get_drs_descriptor(ocfl_inventory)
        
        self._rehydrate_files(ocfl_inventory, drs_descriptor)

    def _get_ocfl_inventory(self):
        """
        Gets the OCFL inventory for the OCFL object.

        Returns:
            OcflInventory: The OCFL inventory for the OCFL object.
        """
        inventory_path = os.path.join(self.ocfl_obj_root, 'inventory.json')
        with open(inventory_path, 'r') as file:
            return OcflInventory(file)
        
    def _get_drs_descriptor(self, ocfl_inventory):
        """
        Gets the DRS descriptor for the OCFL object.

        Args:
            ocfl_inventory (OcflInventory): The OCFL inventory for the OCFL object.

        Returns:
            DrsDescriptor: The DRS descriptor for the OCFL object.
        """
        descriptor_path = ocfl_inventory.get_descriptor_path()
        return DrsDescriptor(os.path.join(self.ocfl_obj_root, descriptor_path))
    
    def _rehydrate_files(self, ocfl_inventory, drs_descriptor):
        """
        Rehydrates files from the OCFL object.

        Args:
            ocfl_inventory (OcflInventory): The OCFL inventory for the OCFL object.
            drs_descriptor (DrsDescriptor): The DRS descriptor for the OCFL object.
        """
        output_batch_name = drs_descriptor.get_batch_name()
        output_batch_dir = os.path.join(self.output_dir, output_batch_name)
        for file_id, drs_file in drs_descriptor.files.items():
            data_path = ocfl_inventory.get_data_path(file_id)
            input_data_path = os.path.join(self.ocfl_obj_root, data_path)

            file_dir = self._clean_path(drs_file.get_file_dir())
            output_dir = os.path.join(output_batch_dir, file_dir)
            output_file_path = os.path.join(output_dir, drs_file.get_file_name())
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            shutil.copyfile(input_data_path, output_file_path)

    def _clean_path(self, file_dir):
        """
        Gets a path that omits any leading slashes.

        Args:
            file_dir (str): The path to clean up.

        Returns:
            str: The cleaned up path.
        """
        while file_dir.startswith('/'):
            file_dir = file_dir[1:]  # Remove the leading slash if present

        return file_dir
