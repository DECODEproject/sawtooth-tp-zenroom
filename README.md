# Zenroom experimental transaction-processor for Sawtooth




# To run a sawtooth command from inside the docker compose

1. make sure keys are there or generate with: `sawtooth keygen`
2. verify the REST-API connectivity: `curl http://rest-api:8080/peers`
3. append the `--url http://rest-api:8080` option on all commands

For instance:
```
sawtooth peer --url http://rest-api:8080 list 
```
