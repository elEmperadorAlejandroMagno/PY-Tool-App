from abc import ABC, abstractmethod

class PhoneticTranscriptionInterface(ABC):
    @abstractmethod
    def transcribe_to_ipa(self, text: str, accent: str = "rp") -> str:
        """
        Transcribe English text to IPA phonetic notation.
        
        Args:
            text (str): English text to transcribe
            accent (str): Accent variant to use ("rp" for Received Pronunciation, "ga" for General American)
        
        Returns:
            str: IPA transcription of the text
        
        Raises:
            NotImplementedError: Must be implemented by concrete classes
        """
        raise NotImplementedError
    
    @abstractmethod
    def is_accent_supported(self, accent: str) -> bool:
        """
        Check if the specified accent is supported.
        
        Args:
            accent (str): Accent code to check
        
        Returns:
            bool: True if accent is supported, False otherwise
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_supported_accents(self) -> list[str]:
        """
        Get list of supported accent variants.
        
        Returns:
            list[str]: List of supported accent codes
        """
        raise NotImplementedError