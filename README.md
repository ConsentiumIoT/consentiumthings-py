# ConsentiumThings Python API

## Overview

`ConsentiumThings` is a Python library for sending and receiving IoT data from the **Consentium Cloud**. It provides an easy-to-use interface to interact with the Consentium IoT APIs, including sensor data ingestion (`/v2/updateData`) and retrieval (`/getData`).

## Installation

```bash
pip install consentiumthings
```

## Usage

### Importing ConsentiumThings

```python
from consentiumthings import ConsentiumThings
```

### Initializing ConsentiumThings

You need to provide your **board key** when creating a new instance:

```python
ct = ConsentiumThings("YOUR-BOARD-KEY")
```

---

### Sending Data

To send data, initialize with your **send key**, then call `send_data()`:

```python
ct.begin_send("YOUR-SEND-KEY")

response = ct.send_data(
    data_buff=[40.0, 90.0], 
    info_buff=["Temperature", "Humidity"]
)

print(response)
```

Example response (success):

```json
{
  "status": "success",
  "message": "Sensor data updated successfully"
}
```

Example response (MAC mismatch):

```json
{
  "message": "MAC mismatch"
}
```

---

### Receiving Data

To fetch data, initialize with your **receive key**, then call `receive_data()`.

* By default, it fetches the **full history**.
* Set `recents=True` to fetch only the most recent data.
* When fetching history, optionally provide `start_date_time` and/or
  `end_date_time` to retrieve a time slice.

```python
ct.begin_receive("YOUR-RECEIVE-KEY")

data = ct.receive_data(
    start_date_time="2026-09-28T10:19:46.681 05:30",
    end_date_time="2026-09-28T13:19:46.681 05:30"
)

print(data)
```

To fetch only the most recent data:

```python
ct.begin_receive("YOUR-RECEIVE-KEY", recents=True)
data = ct.receive_data()
```

Time slicing cannot be used when `recents=True`; `receive_data()` raises
`ValueError` if both options are used.

Example response (parsed into Python dicts):

```python
[
  {
    "updated_at": "2026-09-28T13:49:21.186+05:30",
    "Temperature": 40.0,
    "Humidity": 90.0
  }
]
```

---

## Methods

### `ConsentiumThings(board_key)`

Initialize the client.

* **Parameters**:

  * `board_key` (str): Unique key for your board.

### `begin_send(send_key)`

Set up the client for sending data.

* **Parameters**:

  * `send_key` (str): The key for authenticated send operations.

### `send_data(data_buff, info_buff)`

Send sensor data.

* **Parameters**:

  * `data_buff` (list): List of sensor values.
  * `info_buff` (list): Labels for each sensor value.
* **Returns**: Dict containing API response.

### `begin_receive(receive_key, recents=False)`

Set up the client for retrieving data.

* **Parameters**:

  * `receive_key` (str): Key for authenticated receive operations.
  * `recents` (bool): If True, fetch only the most recent entry. Default: False.

### `receive_data()`

Fetch data from the cloud, optionally restricted to a time range.

* **Parameters**:

  * `start_date_time` (str, optional): Start of the time slice.
  * `end_date_time` (str, optional): End of the time slice.
  * Time-slicing parameters cannot be used if `begin_receive()` was called with `recents=True`.

* **Returns**: List of dicts with parsed sensor data.

---

## Example

```python
from consentiumthings import ConsentiumThings

# Initialize client
ct = ConsentiumThings("YOUR-BOARD-KEY")

# Send data
ct.begin_send("YOUR-SEND-KEY")
print(ct.send_data([40.0, 90.0], ["Temperature", "Humidity"]))

# Receive a time slice from the history
ct.begin_receive("YOUR-RECEIVE-KEY")

print(ct.receive_data(
  start_date_time="2026-09-28T10:19:46.681 05:30",
  end_date_time="2026-09-28T13:19:46.681 05:30"
))

# Receive most recent data
ct.begin_receive("YOUR-RECEIVE-KEY", recents=True)
print(ct.receive_data())
```

---

## Error Handling

The API may return structured JSON errors. Common cases:

| Code  | Example Response                | Meaning                                     |
| ----- | ------------------------------- | ------------------------------------------- |
| `200` | `{"status":"success"}`          | Data sent/received successfully             |
| `422` | `{"message":"MAC mismatch"}`    | MAC address does not match registered board |
| `401` | `{"message":"Invalid key"}`     | Send/receive key invalid                    |
| `404` | `{"message":"Board not found"}` | Board key is invalid                        |

---

## Support

For any issues or questions regarding ConsentiumThings Python API, please contact **[official@consentiumiot.com](mailto:official@consentiumiot.com)**.

---

## License

This software is licensed under the MIT License. See the LICENSE file for details.
