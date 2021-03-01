from image_pb2_grpc import ImageServiceServicer
from image_pb2_grpc import add_ImageServiceServicer_to_server
from image_pb2 import ImageDetails
import grpc
from concurrent import futures
from demo import do_something

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.instrumentation.grpc import server_interceptor
from opentelemetry import propagators
from opentelemetry.propagators.b3 import B3Format


class ImageServer(ImageServiceServicer):
    def getImageDetails(self, request, context):
        image_details = ImageDetails()
        image_details.productId = "1"
        image_details.imageUrl = "localhost"
        do_something()
        return image_details


def serve():
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        SimpleExportSpanProcessor(ConsoleSpanExporter())
    )

    propagators.set_global_textmap(B3Format())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[server_interceptor()])
    add_ImageServiceServicer_to_server(ImageServer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()