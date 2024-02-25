## ConsentiumThings Python API Documentation

### Overview
ConsentiumThings is a Python API designed to facilitate sending and receiving data to and from Consentium Cloud. It provides an easy-to-use interface for developers to interact with Consentium Cloud services programmatically.

### Installation
You can install ConsentiumThings via pip:
```bash
pip install consentiumthings
```

### Usage

#### Importing ConsentiumThings
```python
from consentiumthings import consentiumthings
```

#### Initializing ConsentiumThings
To initialize ConsentiumThings, you need to provide your board key.
```python
ct = consentiumthings("board_key")
```

#### Sending Data
To send data to Consentium Cloud, use the `begin_send()` method followed by `send_data()`.
```python
ct.begin_send("send_key")
ct.send_data([1, 2, 3, 4], ['info1', 'info2', 'info3'])
```

#### Receiving Data
To receive data from Consentium Cloud, use the `begin_receive()` method followed by `receive_data()`.
```python
ct.begin_receive("receive_key", recent=False)
print(ct.receive_data())
```

### Methods

#### `consentiumthings(board_key)`
- **Parameters:**
    - `board_key` (str): The key associated with the board.

#### `begin_send(send_key)`
- **Parameters:**
    - `send_key` (str): The key associated with the send operation.

#### `send_data(data, info_list)`
- **Parameters:**
    - `data` (list): The data to be sent.
    - `info_list` (list): List of information associated with each data item.

#### `begin_receive(receive_key, recent=False)`
- **Parameters:**
    - `receive_key` (str): The key associated with the receive operation.
    - `recent` (bool, optional): If True, only the most recent data will be received. Default is False.

#### `receive_data()`
- **Returns:**
    - List of received data.

### Example
```python
from consentiumthings import consentiumthings

# Initialize ConsentiumThings
ct = consentiumthings("board_key")

# Send data
ct.begin_send("send_key")
ct.send_data([1, 2, 3, 4], ['info1', 'info2', 'info3'])

# Receive data
ct.begin_receive("receive_key", recent=False)
print(ct.receive_data())
```

### Support
For any issues or questions regarding ConsentiumThings Python API, please contact consentium.inc@gmail.com.

### License
This software is licensed under the MIT License. See the LICENSE file for details.