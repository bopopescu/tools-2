#include <iostream>
#include <thread>
#include <unistd.h>

class CThread
{
public:
	//CThread():mThread(&CThread::start, this){} // don't know why can't define like this.
	CThread(void *arg):mThread(&CThread::start, this, arg){}
	virtual ~CThread(){
		mThread.join();
	}

	virtual void run(void *arg){
		argv = arg;
		std::cout << "CThread start running" << std::endl;
		int n = *(int*)argv;
		while(n <= 5){
			std::cout << "n = "  << n << std::endl;
			n++;
			sleep(1);
		}
	}
	static bool start(void *thread_obj, void *arg){
		CThread *pThread = (CThread *)thread_obj;
		pThread->run(arg);
	}
	//static bool start(void *thread_obj){
	//	CThread::start(thread_obj, 0);
	//}

protected:
	void *argv;
	std::thread mThread;

};

/*
class MyThread : public CThread
{
public:
	//MyThread(void *arg){}
	CThread(void *arg):mThread(&CThread::start, this, arg){}
	void run(void *arg)
	{
		std::cout << "I want do nothing." << std::endl;
	}
};
*/

int main()
{
	int n = 2;
	//CThread mthd1();
	CThread mthd2(&n);

	n = 3;
	MyThread mthd3(&n);
}

