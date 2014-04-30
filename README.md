s3200
=====

A Python package for controlling the Fröling heating system with S3200 lambdatronic control over the maintenance interface.

State: Alpha - Reading actual values is working. 


Code Example:
```python
  from s3200.obj import S3200()
  
  s = S3200("/dev/ttyS0")
  
  temperature = s.get_value('boiler_1_temperature')
  print('Temperature: {0}'.format(str(temperature)))
  
  status = s.get_status()
  print('Status: {0}'.format(status))
```
  
  
Output:
```
  Temperature: 42.5
  Status: STÖRUNG
```
