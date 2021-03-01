from services.product.backup.product_pb2_grpc import ProductInfoServicer
import inspect
import importlib



obj = ProductInfoServicer
print(inspect.isclass(obj))
test = reversed(inspect.getmro(obj))
my_obj = (cls for cls in test if cls is not object)
root_base_class = next(my_obj)
root_base_class_module_name = root_base_class.__module__
print(root_base_class_module_name)
servicer_name = root_base_class.__name__
service_name = servicer_name[: -len("Servicer")]
grcp_module = importlib.import_module(root_base_class_module_name)
stub_name = f'{service_name}Stub'
servicer_name = f'{service_name}Servicer'
add_method_name = f'add_{servicer_name}_to_server'

if not grcp_module.__name__.endswith('_pb2_grpc'):
    raise TypeError(f'{grcp_module} doesn\'t end with _pb2_grpc')
p2b_module_name = grcp_module.__name__[: -len('_grpc')]
p2b_module = importlib.import_module(p2b_module_name)

servicer_cls = getattr(grcp_module, servicer_name)

add_method = getattr(grcp_module, add_method_name, None)
stub_cls = getattr(grcp_module, stub_name, None)

service_descriptor = p2b_module.DESCRIPTOR.services_by_name.get(service_name)


methods = []
for method in service_descriptor.methods:
    # method_proto = MethodDescriptorProto()
    # method.CopyToProto(method_proto)
    request_type = ProtoDatabase.get(method.input_type.full_name)
    response_type = ProtoDatabase.get(method.output_type.full_name)
    if request_type is None:
        raise TypeError(f'Couldn\'t find request proto {method.input_type.full_name}')
    if response_type is None:
        raise TypeError(f'Couldn\'t find response proto {method.output_type.full_name}')

prefix = "Dynamic"
my_dummy_clas = type(f'{prefix}Test', (obj,),{})
my_dummy_obj = my_dummy_clas()


print("end")
