class AgentCreativeError(Exception):
    pass


class AudioGenerationError(AgentCreativeError):
    pass


class ImageGenerationError(AgentCreativeError):
    pass


class VideoAssemblyError(AgentCreativeError):
    pass


class StorageError(AgentCreativeError):
    pass


class ConfigurationError(AgentCreativeError):
    pass