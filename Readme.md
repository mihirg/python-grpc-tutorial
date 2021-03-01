You might need to run 
`pip install googleapis-common-protos`

Consists of 2 services

1. Image Service
2. Product Service

Product client calls product service which in turn calls the image service.
The Product service also spins up a rest proxy at port 65000. you can directly invoke the rest api via curl

`curl -X POST -H "Content-Type: application/json" -d '{"name": "linuxize", "email": "linuxize@example.com"}' http://127.0.0.1:65000/product/details`

Note the payload is not validated, so anything goes :-)