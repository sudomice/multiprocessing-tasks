# multiprocessing and multithreading in Python

Simple code that explains how task queues can be used with multi processing + multi threading per process in python


## Usage

```
process = MultiProcessor(process,threads,threshold,func,(args,))
process.start_process()
```

It will divide threshold number of tasks between process & threads. Passing the args to the function provided each time.

```
process -> int
threads -> int
threshold -> int
func -> def
args -> Iterable
```

## Example Calls

##### **Input**

```
processObj = MultiProcessor(4,10,5,print,("your arguments go here",))
processObj.start_process()
```

##### **Output**

```
('your arguments go here',)
('your arguments go here',)
('your arguments go here',)
('your arguments go here',)
('your arguments go here',)
```
