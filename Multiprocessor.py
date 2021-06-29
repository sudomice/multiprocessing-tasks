import threading
import multiprocessing

def replace_with_your_function(*args):
    """this function is replaced by your function
    args could be anything defined during class construction
    """
    
    print(args[0])


class MultiProcessor:
    """
    Helps to run bulk tasks with multiprocessing and multithreading.

    ...

    Attributes
    ----------
    threads : int
        Number of thread for each process to run
    function : def
        The function to execute N number of times
    processes : int
        Number of processes to run to finish the task
    in_q : Queue
        The Queue containing threads to perform the task
    args : tuple
        Arguments to be passed to the function
    threshold: int
        Total number of times the function needs to be executed
    
    Methods
    ----------
    quit_process()
        Send sentinel for each thread worker to quit
    close_process()
        Wait for workers to terminate
    each_thread_worker(count,in_q = None,function = None)
        Executes the function by passing the args till Queue exists
    start_thread(count,threads = None, in_q = None)
        Starts a new thread for a process
    start_process()
        Starts N number of processes to run parallel
    """


    def __init__(self,processes, threads,threshold,function,args:None) -> None:
        """
        Parameters
        ----------
        threads : int
            Number of thread for each process to run
        function : def
            The function to execute N number of times
        processes : int
            Number of processes to run to finish the task
        in_q : Queue
            The Queue containing threads to perform the task
        args : tuple
            Arguments to be passed to the function
        threshold: int
            Total number of times the function needs to be executed
        """

        self.threads = threads
        self.function = function
        self.processes = processes
        self.process_workers = []
        self.in_q = multiprocessing.Queue()
        self.args = args
        self.threshold = threshold

    def __getstate__(self):
        # capture what is normally pickled
        state = self.__dict__.copy()
        # remove unpicklable/problematic variables 
        state['process_workers'] = None
        return state

    def quit_process(self):
        """Send sentinel for each thread worker to quit"""
        
        for _ in range(self.processes * self.threads):
            self.in_q.put(None)

    def close_process(self):
        """Wait for workers to terminate"""
        
        for w in self.process_workers:
            w.join()

    def each_thread_worker(self,count,in_q = None,function = None):
        """
        Parameters 
        ----------
        count : int
            process number 
        in_q : Queue 
            Queue containing the task to execute
        function : def
            Function to execute N number of times
        """
        
        if not self.args:
            raise ValueError("Provide args during Class initialization")
        # Each thread performs the actual work. 
        #converting this function in a generic function block.
        in_q = in_q or self.in_q
        function = function or self.function
        
        while True:
            task = in_q.get()
            if task is None:
                break
            try:
                function(self.args)
            except Exception as e:
                print(e,"WHILE EXECUTING GENERIC FUNCTION")
                continue

    def start_thread(self, count,threads = None, in_q = None)->None:
        """
        Parameters
        ----------
        count : int
            process number 
        threads : int
            Number of threads to create
        in_q : Queue 
            Queue containing the task to execute
        """
        
        in_q = in_q or self.in_q
        threads = threads or self.threads
        thread_workers = []
        
        for i in range(threads):
            w = threading.Thread(target=self.each_thread_worker, args=(str(i)+count,))
            w.start()
            thread_workers.append(w)

        # Wait for thread workers to terminate.
        for w in thread_workers:
            w.join()

    def start_process(self)->None:
        """Starts N number of processes to run parallel"""
        
        for count in range(self.processes):
            w = multiprocessing.Process(target=self.start_thread, args=( str(count),))
            w.start()
            self.process_workers.append(w)
        for _ in range(self.threshold):
            self.in_q.put(self.args)
        self.quit_process()
        self.close_process()

if __name__ == "__main__":
    #Test runs
    process = MultiProcessor(4,10,5,print,("your arguments go here",))
    process.start_process()