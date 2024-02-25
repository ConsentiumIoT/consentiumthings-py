# ConsentiumThings
Python API to send and receive data for Consentium Cloud.

# Example usage

```python
ct = ConsentiumThings("board-key")
ct.begin_send("send-key")
ct.send_data([1, 2, 3, 4, 5], ['info1', 'info2', 'info3'])

ct.begin_receive("receive-key", recent=False)
print(ct.receive_data())
```
