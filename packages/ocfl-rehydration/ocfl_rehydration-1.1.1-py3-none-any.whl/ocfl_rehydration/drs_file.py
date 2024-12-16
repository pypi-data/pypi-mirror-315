class DrsFile:
    """
    A class representing a DRS file.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.file_id = ""
        self.file_name = ""
        self.file_dir = ""
        self.digest_alg = ""
        self.digest_value = ""
        self.mime_type = ""
        self.amd_ids = []

    def __repr__(self):
        """
        Returns a string representation of this object.
        """
        return "DrsFile: id={}, file_name={}, file_dir={}, digest_alg={}, "\
               "digest_value={}, mime_type={}".format(self.file_id,
                                                      self.file_name,
                                                      self.file_dir,
                                                      self.digest_alg,
                                                      self.digest_value,
                                                      self.mime_type)

    def get_id(self):
        """
        Returns the id of this file.

        Returns:
            int: The id of this file.
        """
        return self.file_id


    def get_file_name(self):
        """
        Returns the supplied name of the file.

        Returns:
            str: The name of the file.
        """
        return self.file_name
    
    
    def get_file_dir(self):
        """
        Returns the supplied directory containing the file.

        Returns:
            str: The directory containing the file.
        """
        if self.file_dir == '/':
            return ''
        return self.file_dir
    
    def add_amd_id(self, amd_id):
        """
        Adds an amd_id to the list of amd_ids for this file.

        Args:
            amd_id (str): The amd_id to add.
        """
        self.amd_ids.append(amd_id)

    def get_digest_alg(self):
        """
        Returns the digest algorithm used for this file.

        Returns:
            str: The digest algorithm used for this file.
        """
        return self.digest_alg

    def get_digest_value(self):
        """
        Returns the digest value for this file.

        Returns:
            str: The digest value for this file.
        """
        return self.digest_value

    def get_mime_type(self):
        """
        Returns the mime type for this file.

        Returns:
            str: The mime type for this file.
        """
        return self.mime_type

    def set_id(self, file_id):
        """
        Sets the id of this file.

        Args:
            file_id (int): The id of this file.
        """
        self.file_id = file_id

    def set_file_name(self, file_name):
        """
        Sets the supplied name of the file.

        Args:
            file_name (str): The name of the file.
        """
        self.file_name = file_name

    def set_file_dir(self, file_dir):
        """
        Sets the supplied directory containing the file.

        Args:
            file_dir (str): The directory containing the file.
        """
        self.file_dir = file_dir

    def set_digest_alg(self, digest_alg):
        """
        Sets the digest algorithm used for this file.

        Args:
            digest_alg (str): The digest algorithm used for this file.
        """
        self.digest_alg = digest_alg

    def set_digest_value(self, digest_value):
        """
        Sets the digest value for this file.

        Args:
            digest_value (str): The digest value for this file.
        """
        self.digest_value = digest_value

    def set_mime_type(self, mime_type):
        """
        Sets the mime type for this file.

        Args:
            mime_type (str): The mime type for this file.
        """
        self.mime_type = mime_type