# Zenroom-TP (Transaction Processor) for the Hyperledger Sawtooth blockchain

This repository integrates the [Zenroom VM](https://zenroom.dyne.org) to be used as a transaction processor in the [Sawtooth](https://sawtooth.hyperledger.org/) blockchain distributed by the Linux Foundation's [Hyperledger](https://www.hyperledger.org/) consortium.

To facilitate the creation of transaction families based on Zenroom and the [Zencode human-friendly language for smart-contracts](https://decodeproject.eu/blog/smart-contracts-english-speaker), this TP uses the [Sawtooth SDK](https://sawtooth.hyperledger.org/docs/core/releases/latest/sdks.html) in Python and the [zenroom-py](https://github.com/DECODEproject/zenroom-py) bindings.

## Getting started

After reading Sawtooth's [documentation](https://sawtooth.hyperledger.org/docs/core/releases/1.0/app_developers_guide/docker.html#using-sawtooth-with-docker) and understanding its architecture and operational underpinnings, one can start playing around with this transaction processor simply using Docker. 
 

There is a script `xec.sh` which can be used to operate docker compose. This will create a network with the following containers:

| docker-compose service | Container name         | purpose |
| ---------------------- | ---------------------- | ------- |
| validator              | sawtooth-validator     | Main "node" of the blockchain which executes and validates transactions |
| rest-api               | rest-api               | Provides a http / json adaptor over the zeromq protocol to allow clients to talk to the validator from within and also from the host machine|
| shell                  | sawtooth-shell-default | Provides a container with various commands in it which allows you to connect to the rest api from within the docker network | 
| settings-tp            | settings-tp            | A standard transaction processor that allows settings to be configured in the blockchainsd



To start a local instance of Sawtooth using the [devmode consensus engine](https://github.com/hyperledger/sawtooth-devmode), a single local Validator node and of course the Zenroom TP, run:



```
docker-compose up
```

To stop and remove the container images do:

```
docker-compose stop
docker-compose rm
```

## To develop the tp on OSX

https://github.com/ludbb/secp256k1-py#installation-with-compilation

```
brew install automake pkg-config libtool libffi gmp
python3 ./setup.py install
```

You will need an osx build of the zenroom-py module. 

```
. ./.sawtooth-tp.venv/bin/activate
pip uninstall zenroom
pip install ../zenroom-py/dist/zenroom-0.1.3.tar.gz 

cd zenroom_sawtooth
nosetests tests
```
 

## To run a sawtooth command

To run a command processed by the Sawtooth blockchain one needs to be logged into one of the nodes that have access to the `rest-api`, or `localhost` when connecting from the host machine running docker, using the port `8090`.

What is also needed is that a valid Sawtooth keypair is available for the client, to be generated with the command: `sawtooth keygen`. This command requires having sawtooth-core installed on the machine.

To verify the REST-API connectivity: `curl http://rest-api:8090/peers`

To use Sawtooth's CLI commands append the `--url http://rest-api:8090`

For instance:
```
sawtooth peer --url http://rest-api:8080 list 
```

## ssh to one of the containers, e.g. rest-api

```
docker-compose exec rest-api bash
```

See https://sawtooth.hyperledger.org/docs/core/releases/1.0/app_developers_guide/docker.html#logging-into-the-client-container

To see something happening:
```
docker-compose exec -it sawtooth-validator bash
```

# Acknowledgements

Copyright (C) 2019 by Dyne.org foundation, Amsterdam

Designed, written and maintained by Denis Roio <jaromil@dyne.org> and
Puria Nafisi Azizi <puria@dyne.org>

Zenroom-TP is Licensed under the terms of the Affero GNU Public
License as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

Small parts of Zenroom-TP are based upon example code that is
Copyright (C) 2015-2017 by Intel Corporation and licensed under the
Apache License, Version 2.0.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See [the License](LICENSE.txt).

