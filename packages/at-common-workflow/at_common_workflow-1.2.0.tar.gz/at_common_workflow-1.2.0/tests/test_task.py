# tests/test_task.py
import pytest
from at_common_workflow.core.task import Task
from at_common_workflow.core.context import Context
from at_common_workflow.core.func import Func
from at_common_workflow.types.meta import MetaTask, MetaFunc, Schema, Mappings

# Test fixtures
async def sample_func(a: int, b: str):
    return f"{a}-{b}"

async def none_func() -> None:
    return None

async def invalid_func() -> str:
    return "invalid"

class TestTask:
    @pytest.fixture
    def basic_task(self):
        return Task(
            name="sample_task",
            description="A sample task that combines a number and text",
            func=sample_func,
            args={},
            requires={"num": int, "text": str},
            provides={"output": str},
            input_mappings={"num": "a", "text": "b"},
            output_mappings={"output": "return_0"}
        )

    # Test initialization
    def test_init_basic(self, basic_task):
        assert isinstance(basic_task.func, Func)
        assert isinstance(basic_task.args, dict)
        assert isinstance(basic_task.requires, Schema)
        assert isinstance(basic_task.provides, Schema)
        assert isinstance(basic_task.input_mappings, Mappings)
        assert isinstance(basic_task.output_mappings, Mappings)

    def test_init_with_arguments(self):
        task = Task(
            name="param_task",
            description="A task with extra arguments",
            func=sample_func,
            args={"extra": "param"},
            requires={},
            provides={},
            input_mappings={},
            output_mappings={}
        )
        assert task.args == {"extra": "param"}

    # Test validation
    def test_invalid_input_mapping(self):
        with pytest.raises(ValueError, match="Input mapping 'invalid' not in requires schema"):
            Task(
                name="invalid_input_task",
                description="A task with invalid input mapping",
                func=sample_func,
                args={},
                requires={"valid": str},
                provides={},
                input_mappings={"invalid": "arg"},
                output_mappings={}
            )

    def test_invalid_output_mapping(self):
        with pytest.raises(ValueError, match="Provided output 'valid' has no mapping"):
            Task(
                name="invalid_output_task",
                description="A task with invalid output mapping",
                func=sample_func,
                args={},
                requires={},
                provides={"valid": str},
                input_mappings={},
                output_mappings={"invalid": "result"}
            )

    def test_missing_output_mapping(self):
        with pytest.raises(ValueError, match="Provided output 'output' has no mapping"):
            Task(
                name="missing_output_task",
                description="A task with missing output mapping",
                func=sample_func,
                args={},
                requires={},
                provides={"output": str},
                input_mappings={},
                output_mappings={}
            )

    # Test execution
    @pytest.mark.asyncio
    async def test_execute_basic(self, basic_task):
        context = Context({"num": 42, "text": "test"})
        await basic_task.execute(context)
        assert context["output"] == "42-test"

    @pytest.mark.asyncio
    async def test_execute_none_return(self):
        task = Task(
            name="none_task",
            description="A task that returns None",
            func=none_func,
            args={},
            requires={},
            provides={},
            input_mappings={},
            output_mappings={}
        )
        context = Context()
        await task.execute(context)
        assert len(context) == 0

    @pytest.mark.asyncio
    async def test_execute_missing_input(self, basic_task):
        context = Context({"num": 42})  # Missing 'text'
        with pytest.raises(ValueError, match="Required input 'text' not found in context"):
            await basic_task.execute(context)

    @pytest.mark.asyncio
    async def test_execute_wrong_input_type(self, basic_task):
        context = Context({"num": "not_an_int", "text": "test"})
        with pytest.raises(TypeError, match="Input 'num' expected type"):
            await basic_task.execute(context)

    @pytest.mark.asyncio
    async def test_execute_wrong_output_type(self):
        async def bad_output() -> dict:
            return {"result": 42}  # Returns int when str is expected
        
        task = Task(
            name="wrong_output_task",
            description="A task that returns the wrong output type",
            func=bad_output,
            args={},
            requires={},
            provides={"output": str},
            input_mappings={},
            output_mappings={"output": "return_0"}
        )
        context = Context()
        with pytest.raises(TypeError, match="Output 'output' expected type"):
            await task.execute(context)

    @pytest.mark.asyncio
    async def test_execute_missing_promised_output(self):
        async def incomplete_output() -> dict:
            return {"something_else": "value"}  # Return dict without the promised output key
        
        task = Task(
            name="incomplete_output_task",
            description="A task that returns an incomplete output",
            func=incomplete_output,
            args={},
            requires={},
            provides={"output": str},
            input_mappings={},
            output_mappings={"output": "something_else_key"}  # Key that doesn't exist in result
        )
        context = Context()
        with pytest.raises(ValueError, match="Output mapping 'something_else_key' not found in function result"):
            await task.execute(context)

    # Test metadata conversion
    def test_to_meta(self, basic_task):
        meta = basic_task.to_meta()
        assert isinstance(meta, MetaTask)
        assert isinstance(meta.func, MetaFunc)
        assert meta.requires == basic_task.requires
        assert meta.provides == basic_task.provides
        assert meta.input_mappings == basic_task.input_mappings
        assert meta.output_mappings == basic_task.output_mappings
        assert meta.args == basic_task.args

    def test_from_meta(self, basic_task):
        meta = basic_task.to_meta()
        new_task = Task.from_meta(meta)
        assert isinstance(new_task, Task)
        assert new_task.args == basic_task.args
        assert new_task.requires == basic_task.requires
        assert new_task.provides == basic_task.provides
        assert new_task.input_mappings == basic_task.input_mappings
        assert new_task.output_mappings == basic_task.output_mappings

    # Test with complex scenarios
    @pytest.mark.asyncio
    async def test_execute_with_nested_data(self):
        async def nested_func(data: dict) -> dict:
            return {"nested": {"value": data["key"]}}
        
        task = Task(
            name="nested_data_task",
            description="A task that processes nested data",
            func=nested_func,
            args={},
            requires={"input": dict},
            provides={"output": dict},
            input_mappings={"input": "data"},
            output_mappings={"output": "return_0"}
        )
        
        context = Context({"input": {"key": "test"}})
        await task.execute(context)
        assert context["output"] == {"nested": {"value": "test"}}

    @pytest.mark.asyncio
    async def test_execute_with_params(self):
        async def param_func(a: int, fixed: str) -> dict:
            return {"result": f"{a}-{fixed}"}
        
        task = Task(
            name="param_task",
            description="A task that processes parameters",
            func=param_func,
            args={"fixed": "constant"},
            requires={"num": int},
            provides={"output": dict},
            input_mappings={"num": "a"},
            output_mappings={"output": "return_0"}
        )
        
        context = Context({"num": 42})
        await task.execute(context)
        assert context["output"]["result"] == "42-constant"

    @pytest.mark.asyncio
    async def test_execute_none_return_with_promises(self):
        """Test that a function returning None when outputs are promised raises an error"""
        task = Task(
            name="none_with_promises_task",
            description="A task that returns None but promises outputs",
            func=none_func,
            args={},
            requires={},
            provides={"output": str},  # Promising output but returning None
            input_mappings={},
            output_mappings={"output": "result"}
        )
        context = Context()
        with pytest.raises(ValueError, match="Function returned None but outputs were promised"):
            await task.execute(context)

    def test_init_with_empty_name(self):
        """Test that empty task name is not allowed"""
        with pytest.raises(ValueError, match="Task name cannot be empty"):
            Task(
                name="",  # Empty name
                description="A task with empty name",
                func=sample_func,
                args={},
                requires={},
                provides={},
                input_mappings={},
                output_mappings={}
            )

    def test_init_with_empty_description(self):
        """Test that empty task description is not allowed"""
        with pytest.raises(ValueError, match="Task description cannot be empty"):
            Task(
                name="task",
                description="",  # Empty description
                func=sample_func,
                args={},
                requires={},
                provides={},
                input_mappings={},
                output_mappings={}
            )

    def test_duplicate_output_mappings(self):
        """Test that multiple output mappings to the same result key are not allowed"""
        with pytest.raises(ValueError, match="Multiple output mappings to the same result key 'result'"):
            Task(
                name="duplicate_mapping_task",
                description="A task with duplicate output mappings",
                func=sample_func,
                args={},
                requires={},
                provides={"output1": str, "output2": str},
                input_mappings={},
                output_mappings={"output1": "result", "output2": "result"}  # Duplicate mapping
            )

    @pytest.mark.asyncio
    async def test_execute_with_none_input_value(self, basic_task):
        """Test handling of None values in context"""
        context = Context({"num": None, "text": "test"})
        with pytest.raises(TypeError, match="Input 'num' expected type"):
            await basic_task.execute(context)

    @pytest.mark.asyncio
    async def test_execute_with_circular_mappings(self):
        """Test detection of circular mappings between input and output"""
        async def circular_func(x: str) -> dict:
            return {"x": x}

        with pytest.raises(ValueError, match="Circular dependency detected for key 'a'"):
            task = Task(
                name="circular_task",
                description="A task with circular mappings",
                func=circular_func,
                args={},
                requires={"a": str},
                provides={"a": dict},  # Changed from str to dict
                input_mappings={"a": "x"},
                output_mappings={"a": "return_0"}  # Changed to return_0
            )

    def test_init_with_invalid_func_type(self):
        """Test initialization with invalid function type"""
        with pytest.raises(TypeError, match="Function must be callable"):
            Task(
                name="invalid_func_task",
                description="A task with invalid function",
                func="not_a_function",  # This should trigger the TypeError
                args={},
                requires={},
                provides={},
                input_mappings={},
                output_mappings={}
            )

    @pytest.mark.asyncio
    async def test_execute_with_empty_context(self, basic_task):
        """Test execution with completely empty context"""
        context = Context()
        with pytest.raises(ValueError, match="Required input 'num' not found in context"):
            await basic_task.execute(context)

    def test_init_with_mismatched_mapping_types(self):
        """Test initialization with mismatched types in mappings"""
        with pytest.raises(TypeError, match="Mapping values must be strings"):
            Task(
                name="mismatched_types_task",
                description="A task with mismatched mapping types",
                func=sample_func,
                args={},
                requires={"num": int},
                provides={},
                input_mappings={"num": 42},  # Integer instead of string
                output_mappings={}
            )

    @pytest.mark.asyncio
    async def test_execute_with_very_large_data(self):
        """Test task execution with very large input/output data"""
        large_data = {"key": "x" * 1000000}  # 1MB string
        
        async def large_data_func(data: dict) -> dict:
            return {"result": len(data["key"])}
        
        task = Task(
            name="large_data_task",
            description="Process very large data",
            func=large_data_func,
            args={},
            requires={"input": dict},
            provides={"output": dict},
            input_mappings={"input": "data"},
            output_mappings={"output": "return_0"}
        )
        
        context = Context({"input": large_data})
        await task.execute(context)
        assert context["output"]["result"] == 1000000

    @pytest.mark.asyncio
    async def test_empty_result_with_outputs(self):
        async def empty_func() -> dict:
            return {}
        
        task = Task(
            name="empty_task",
            description="Task with empty result",
            func=empty_func,
            args={},
            requires={},
            provides={"output": dict},
            input_mappings={},
            output_mappings={"output": "return_0"}
        )
        
        with pytest.raises(ValueError, match="Output mapping 'return_0' is empty"):
            await task.execute(Context())

    @pytest.mark.asyncio
    async def test_nested_dictionary_result(self):
        async def nested_func() -> dict:
            return {"result": {"nested": 42}}
        
        task = Task(
            name="nested_task",
            description="Task with nested result",
            func=nested_func,
            args={},
            requires={},
            provides={"output": dict},
            input_mappings={},
            output_mappings={"output": "return_0"}
        )
        
        context = Context()
        await task.execute(context)
        assert context["output"]["result"]["nested"] == 42

    @pytest.mark.asyncio
    async def test_execute_with_tuple_return(self):
        """Test handling of tuple return values"""
        async def tuple_func() -> tuple:
            return ("first", "second")
        
        task = Task(
            name="tuple_task",
            description="A task returning a tuple",
            func=tuple_func,
            args={},
            requires={},
            provides={"out1": str, "out2": str},
            input_mappings={},
            output_mappings={"out1": "return_0", "out2": "return_1"}
        )
        
        context = Context()
        await task.execute(context)
        assert context["out1"] == "first"
        assert context["out2"] == "second"

    @pytest.mark.asyncio
    async def test_execute_with_list_return(self):
        """Test handling of list return values"""
        async def list_func() -> list:
            return [1, 2, 3]
        
        task = Task(
            name="list_task",
            description="A task returning a list",
            func=list_func,
            args={},
            requires={},
            provides={"first": int, "second": int},
            input_mappings={},
            output_mappings={"first": "return_0", "second": "return_1"}
        )
        
        context = Context()
        await task.execute(context)
        assert context["first"] == 1
        assert context["second"] == 2

    @pytest.mark.asyncio
    async def test_execute_with_primitive_return(self):
        """Test handling of primitive return values"""
        async def primitive_func() -> int:
            return 42
        
        task = Task(
            name="primitive_task",
            description="A task returning a primitive",
            func=primitive_func,
            args={},
            requires={},
            provides={"result": int},
            input_mappings={},
            output_mappings={"result": "return_0"}
        )
        
        context = Context()
        await task.execute(context)
        assert context["result"] == 42