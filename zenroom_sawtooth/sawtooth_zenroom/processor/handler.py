
import logging
import hashlib
import cbor

from zenroom import zenroom

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError


LOGGER = logging.getLogger(__name__)


VALID_VERBS = 'set', 'inc', 'dec', 'zenroom'

MIN_VALUE = 0
MAX_VALUE = 4294967295
MAX_NAME_LENGTH = 20

FAMILY_NAME = 'zenroom'

ZENROOM_ADDRESS_PREFIX = bytes.fromhex('7a656e') # str("zen"):hex()

def make_zenroom_address(name):
    return ZENROOM_ADDRESS_PREFIX + hashlib.sha512(
        name.encode('utf-8')).hexdigest()[-64:]


class ZenroomTransactionHandler(TransactionHandler):
    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['0.1']

    @property
    def namespaces(self):
        return [ZENROOM_ADDRESS_PREFIX]

    def apply(self, transaction, context):
        verb, name, value = _unpack_transaction(transaction)

        state = _get_state_data(name, context)

        updated_state = _do_zenroom(verb, name, value, state)

        _set_state_data(name, updated_state, context)


def _unpack_transaction(transaction):
    verb, name, value = _decode_transaction(transaction)

    _validate_verb(verb)
    _validate_name(name)

    return verb, name, value


def _decode_transaction(transaction):
    try:
        content = cbor.loads(transaction.payload)
    except:
        raise InvalidTransaction('Invalid payload serialization')

    try:
        verb = content['Verb']
    except AttributeError:
        raise InvalidTransaction('Verb is required')

    try:
        name = content['Name']
    except AttributeError:
        raise InvalidTransaction('Name is required')

    try:
        value = content['Value']
    except AttributeError:
        raise InvalidTransaction('Value is required')

    return verb, name, value


def _validate_verb(verb):
    if verb not in VALID_VERBS:
        raise InvalidTransaction('Verb must be "set", "inc", "dec" or "zenroom"')


def _validate_name(name):
    if not isinstance(name, str) or len(name) > MAX_NAME_LENGTH:
        raise InvalidTransaction(
            'Name must be a string of no more than {} characters'.format(
                MAX_NAME_LENGTH))


def _validate_value(value):
    if not isinstance(value, int) or value < 0 or value > MAX_VALUE:
        raise InvalidTransaction(
            'Value must be an integer '
            'no less than {i} and no greater than {a}'.format(
                i=MIN_VALUE,
                a=MAX_VALUE))


def _get_state_data(name, context):
    address = make_zenroom_address(name)

    state_entries = context.get_state([address])

    try:
        return cbor.loads(state_entries[0].data)
    except IndexError:
        return {}
    except:
        raise InternalError('Failed to load state data')


def _set_state_data(name, state, context):
    address = make_zenroom_address(name)

    encoded = cbor.dumps(state)

    addresses = context.set_state({address: encoded})

    if not addresses:
        raise InternalError('State error')


def _do_zenroom(verb, name, value, state):
    verbs = {
        'set': _do_set,
        'inc': _do_inc,
        'dec': _do_dec,
        'zenroom': _do_zenroom,
    }

    try:
        return verbs[verb](name, value, state)
    except KeyError:
        # This would be a programming error.
        raise InternalError('Unhandled verb: {}'.format(verb))


def _do_zenroom(name, value, state):
    msg = 'Executing a zenroom script: %s ' % value
    LOGGER.info(msg)
    result = zenroom.execute(value.encode()).decode()

    updated = {k: v for k, v in state.items()}
    updated[name] = result

    return updated


def _do_set(name, value, state):
    msg = 'Setting "{n}" to {v}'.format(n=name, v=value)
    LOGGER.debug(msg)

    if name in state:
        raise InvalidTransaction(
            'Verb is "set", but already exists: Name: {n}, Value {v}'.format(
                n=name,
                v=state[name]))

    updated = {k: v for k, v in state.items()}
    updated[name] = value

    return updated


def _do_inc(name, value, state):
    msg = 'Incrementing "{n}" by {v}'.format(n=name, v=value)
    LOGGER.debug(msg)

    if name not in state:
        raise InvalidTransaction(
            'Verb is "inc" but name "{}" not in state'.format(name))

    curr = state[name]
    incd = curr + value

    if incd > MAX_VALUE:
        raise InvalidTransaction(
            'Verb is "inc", but result would be greater than {}'.format(
                MAX_VALUE))

    updated = {k: v for k, v in state.items()}
    updated[name] = incd

    return updated


def _do_dec(name, value, state):
    msg = 'Decrementing "{n}" by {v}'.format(n=name, v=value)
    LOGGER.debug(msg)

    if name not in state:
        raise InvalidTransaction(
            'Verb is "dec" but name "{}" not in state'.format(name))

    curr = state[name]
    decd = curr - value

    if decd < MIN_VALUE:
        raise InvalidTransaction(
            'Verb is "dec", but result would be less than {}'.format(
                MIN_VALUE))

    updated = {k: v for k, v in state.items()}
    updated[name] = decd

    return updated
