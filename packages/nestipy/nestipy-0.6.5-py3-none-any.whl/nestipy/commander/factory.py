from typing import Optional, Type

from .commander import NestipyCommander


class CommandFactory:

    @classmethod
    async def run(cls, root_module: Optional[Type]) -> None:
        instance = NestipyCommander()
        instance.init(root_module)
        await instance.run()
