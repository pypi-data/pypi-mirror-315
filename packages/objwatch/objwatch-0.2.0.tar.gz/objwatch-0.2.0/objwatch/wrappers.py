from abc import ABC, abstractmethod


class FunctionWrapper(ABC):
    @abstractmethod
    def wrap_call(self, func_name, frame):
        call_msg = ''
        return call_msg

    @abstractmethod
    def wrap_return(self, func_name, result):
        return_msg = ''
        return return_msg


try:
    import torch
except ImportError:
    torch = None


class TensorShapeLogger(FunctionWrapper):
    def wrap_call(self, func_name, frame):
        call_msg = ' <- '
        args = []
        code = frame.f_code
        arg_names = code.co_varnames[: code.co_argcount]
        for name in arg_names:
            if name in frame.f_locals:
                args.append(frame.f_locals[name])

        if code.co_flags & 0x08:  # CO_VARKEYWORDS
            kwargs = {k: v for k, v in frame.f_locals.items() if k not in arg_names and not k.startswith('_')}
        else:
            kwargs = {}

        tensor_args = [
            arg
            for arg in args
            if isinstance(arg, torch.Tensor)
            or (isinstance(arg, list) and all(isinstance(item, torch.Tensor) for item in arg))
        ]
        tensor_kwargs = {
            k: v
            for k, v in kwargs.items()
            if isinstance(v, torch.Tensor)
            or (isinstance(v, list) and all(isinstance(item, torch.Tensor) for item in v))
        }

        if len(tensor_args) == 0 and len(tensor_kwargs) == 0:
            return ""

        for i, arg in enumerate(tensor_args):
            if isinstance(arg, torch.Tensor):
                call_msg += f"'{i}':{arg.shape}, "
            elif isinstance(arg, list):
                num_tensors = len(arg)
                display_tensors = arg[:3] if num_tensors > 3 else arg
                tensor_shapes = ', '.join([f"tensor_{j}:{tensor.shape}" for j, tensor in enumerate(display_tensors)])
                if num_tensors > 3:
                    tensor_shapes += f"...({num_tensors - 3} more tensors)"
                call_msg += f"'{i}':[{tensor_shapes}], "

        for k, v in tensor_kwargs.items():
            if isinstance(v, torch.Tensor):
                call_msg += f"'{k}':{v.shape}, "
            elif isinstance(v, list):
                num_tensors = len(v)
                display_tensors = v[:3] if num_tensors > 3 else v
                tensor_shapes = ', '.join([f"tensor_{j}:{tensor.shape}" for j, tensor in enumerate(display_tensors)])
                if num_tensors > 3:
                    tensor_shapes += f"...({num_tensors - 3} more tensors)"
                call_msg += f"'{k}':[{tensor_shapes}], "

        call_msg = call_msg.rstrip(', ')
        return call_msg

    def wrap_return(self, func_name, result):
        return_msg = ' -> '
        if isinstance(result, (bool, int, float)):
            return_msg += f"{result}"
        elif isinstance(result, torch.Tensor):
            return_msg += f"{result.shape}"
        elif isinstance(result, list):
            if len(result) == 0:
                return_msg += f"[]"
            elif isinstance(result[0], (bool, int, float)):
                numel = len(result)
                display_elm = result[:3] if numel > 3 else result
                elm_values = ', '.join([f"value_{j}:{element}" for j, element in enumerate(display_elm)])
                if numel > 3:
                    elm_values += f"...({numel - 3} more elements)"
                return_msg += f"[{elm_values}]"
            elif isinstance(result[0], torch.Tensor):
                num_tensors = len(result)
                display_tensors = result[:3] if num_tensors > 3 else result
                tensor_shapes = ', '.join([f"tensor_{j}:{tensor.shape}" for j, tensor in enumerate(display_tensors)])
                if num_tensors > 3:
                    tensor_shapes += f"...({num_tensors - 3} more tensors)"
                return_msg += f"[{tensor_shapes}]"
        else:
            return ""

        return return_msg
