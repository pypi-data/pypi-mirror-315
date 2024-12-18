from typing import Callable, Any, List, Union
from types import ModuleType
from inspect import iscoroutinefunction, isfunction, getmembers
from at_common_workflow.types.meta import MetaFunc
import asyncio, functools, importlib

class Func:
    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if iscoroutinefunction(self.func):
            result = await self.func(*args, **kwargs)
        else:
            result = await asyncio.get_event_loop().run_in_executor(None, functools.partial(self.func, *args, **kwargs))
        
        return result

    def to_meta(self) -> MetaFunc:
        return MetaFunc(
            module=self.func.__module__,
            name=self.func.__qualname__ if hasattr(self.func, '__qualname__') else self.func.__name__
        )

    @classmethod
    def from_meta(cls, meta: MetaFunc) -> 'Func':
        module = importlib.import_module(meta.module)
        obj = module

        for part in meta.name.split('.'):
            obj = getattr(obj, part)
        return cls(obj)

    @staticmethod
    def scan(modules: Union[List[ModuleType], ModuleType]) -> List['Func']:
        """Recursively scan one or more modules for functions.
        
        Args:
            modules: A single Python module or list of modules to scan
            
        Returns:
            List of Func instances wrapping functions
        """
        funcs = []
        
        # Convert single module to list for uniform processing
        if isinstance(modules, ModuleType):
            modules = [modules]
        
        def scan_object(obj, module, prefix: str = ''):
            for name, member in getmembers(obj):
                if name.startswith('_'):
                    continue
                    
                # If it's a function, add it
                if isfunction(member):
                    # Only add functions that belong to this module
                    if getattr(member, '__module__', None) == module.__name__:
                        funcs.append(Func(member))
                    
                # Recursively scan classes and other objects with attributes
                elif isinstance(member, type):  # For classes
                    if getattr(member, '__module__', None) == module.__name__:
                        scan_object(member, module, f"{prefix}{name}.")
        
        # Process each module
        for module in modules:
            # First scan module-level functions
            for name, member in getmembers(module):
                if name.startswith('_'):
                    continue
                
                if isfunction(member) and getattr(member, '__module__', None) == module.__name__:
                    funcs.append(Func(member))
            
            # Then scan classes and their methods
            scan_object(module, module)
        
        return funcs