from services.product.product_pb2_grpc import ProductInfoServicer
from concurrent import futures
import grpc
from services.product.product_pb2_grpc import add_ProductInfoServicer_to_server
from image_pb2_grpc import ImageServiceStub
from image_pb2 import ProductImageId
from services.product.product_pb2 import ProductDetails

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.instrumentation.grpc import server_interceptor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry import propagators
from opentelemetry.propagators.b3 import B3Format
from rest_proxy import MyProxy

class ProductInfoServer(ProductInfoServicer):
    def getProductDetails(self, request, context):
        GrpcInstrumentorClient().instrument()
        channel = grpc.insecure_channel('localhost:50051')
        image_service = ImageServiceStub(channel)
        image_id = ProductImageId()
        image_id.value = "1"
        retVal = image_service.getImageDetails(image_id)
        product_details = ProductDetails()
        product_details.name = "test"
        product_details.imageUrl = retVal.imageUrl
        return product_details


def serve():
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        SimpleExportSpanProcessor(ConsoleSpanExporter())
    )
    propagators.set_global_textmap(B3Format())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[server_interceptor()])
    add_ProductInfoServicer_to_server(ProductInfoServer(), server)
    server.add_insecure_port("[::]:50050")
    server.start()
    proxy = MyProxy(ProductInfoServer)
    try:
        proxy.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("terminating")
        proxy.stop()
    print("Goodbye")


if __name__=="__main__":
    serve()
