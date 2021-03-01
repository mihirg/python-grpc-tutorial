from services.product.backup.product_pb2_grpc import ProductInfoStub
import grpc
from services.product.backup.product_pb2 import ProductId

channel = grpc.insecure_channel('localhost:50050')
prod_info = ProductInfoStub(channel)

prod_id = ProductId()
prod_id.id = "1"

print(prod_info.getProductDetails(prod_id))


