# ConsentiumThings
Python API to send and receive data for Consentium Cloud.

# Example usage

```python
from consentiumthings import consentiumthings

ct = consentiumthings("board_key")
ct.begin_send("send_key")
ct.send_data([1, 2, 3, 4], ['info1', 'info2', 'info3'])

ct.begin_receive("receive_key", recent=False)
print(ct.receive_data())
```
