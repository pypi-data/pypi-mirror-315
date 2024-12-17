from sentence_transformers import SentenceTransformer
from torch import cuda
from torch.backends import mps


class App:
    _instance: "App" = None

    def __new__(cls) -> "App":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self._initialized = True

            self.model = None
            self.allow_origins = []
            self._default_encode = self.encode.__get__(
                self, App
            )  # Store reference to default implementation

    def run(self, host: str, port: int, allow_origins: list[str]) -> None:
        self.allow_origins = allow_origins

        # Setting a default model and encode function
        if not self.model:
            self.set_model(
                **{
                    "model_name_or_path": "avsolatorio/GIST-Embedding-v0",
                    "revision": None,
                }
            )
            self.set_model_device(get_device())

        # If the user did not override, set to a default
        if self.is_default_encode():

            def default_encode(
                text: str, convert_to_tensor: bool
            ) -> list[float]:
                return self.model.encode(
                    text, convert_to_tensor=convert_to_tensor
                )

            self.encode = default_encode

        import uvicorn

        from .router import api

        uvicorn.run(api, host=host, port=port)

    def set_model(self, **model_kwargs: dict) -> None:
        self.model = SentenceTransformer(**model_kwargs)
        self.model.eval()
        self.model.zero_grad()
        self.model.requires_grad_(False)

    def encode(
        self, text: str | list[str], *args: list, **kwargs: dict
    ) -> list[float] | list[list[float]]:
        """Default encode implementation that raises NotImplementedError"""

        raise NotImplementedError

    def is_default_encode(self) -> bool:
        """Check if current encode method is the default implementation"""

        return self.encode.__get__(self, App) == self._default_encode

    def set_model_device(self, device: str) -> None:
        self.model.to(device)


def get_device() -> str:
    if cuda.is_available():
        return "cuda"
    elif mps.is_available():
        return "mps"

    return "cpu"
